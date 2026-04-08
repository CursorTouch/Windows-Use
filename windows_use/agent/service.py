from windows_use.messages import SystemMessage, HumanMessage, AIMessage, ImageMessage, ToolMessage
from windows_use.agent.events import AgentEvent, Event, EventType, ConsoleEventSubscriber, FileEventSubscriber
from windows_use.agent.tools import BUILTIN_TOOLS, EXPERIMENTAL_TOOLS
from windows_use.agent.views import AgentResult, AgentState
from windows_use.telemetry.service import ProductTelemetry
from windows_use.telemetry.views import AgentTelemetryEvent
from windows_use.agent.registry.service import Registry
from windows_use.agent.watchdog.service import WatchDog
from windows_use.agent.desktop.service import Desktop
from windows_use.agent.desktop.views import Browser
from windows_use.agent.loop import LoopGuard
from windows_use.providers.events import LLMEventType
from typing import Callable, Literal, TYPE_CHECKING
from windows_use.agent.context import Context
from windows_use.agent.base import BaseAgent
from contextlib import nullcontext
from rich.console import Console
from itertools import chain
import logging
import time

if TYPE_CHECKING:
    from windows_use.providers.base import BaseChatLLM

logger = logging.getLogger("windows_use")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

_NON_TOOL_PARAMS = {"thought"}


class Agent(BaseAgent):
    def __init__(
        self,
        mode: Literal["flash", "normal"] = "normal",
        instructions: list[str] | None = None,
        browser: Browser = Browser.EDGE,
        use_annotation: bool = False,
        use_accessibility: bool = True,
        secrets: dict[str, str] = {},
        llm: "BaseChatLLM" = None,
        max_consecutive_failures: int = 3,
        max_steps: int = 25,
        use_vision: bool = False,
        auto_minimize: bool = False,
        log_to_file: bool = False,
        log_to_console: bool = True,
        event_subscriber: Callable[[AgentEvent], None] | None = None,
        experimental: bool = False,
        disable_loop_detection: bool = False,
    ):
        """Initialize the Agent.

        The Agent is the core component that orchestrates interactions with the Windows GUI.
        It uses an LLM to process instructions, analyze the desktop state (via UI automation
        and optionally vision), and execute tools to achieve the desired goals.

        Args:
            mode: Agent mode - "flash" for lightweight prompts, "normal" for full prompts.
            instructions: A list of additional instructions or goals for the agent to execute.
            browser: The target web browser for web-related tasks. Defaults to Browser.EDGE.
            use_annotation: Whether to overlay UI element annotations on screenshots before
                providing to the LLM. Defaults to False.
            use_accessibility: Whether to use the accessibility tree. Defaults to True.
            llm: The Large Language Model instance used for decision making.
            max_consecutive_failures: Maximum number of consecutive failures before giving up.
            max_steps: Maximum number of steps allowed in the agent's execution.
            use_vision: Whether to provide screenshots to the LLM. Defaults to False.
            auto_minimize: Whether to automatically minimize the current window before agent
                proceeds. Defaults to False.
            log_to_file: Whether to write agent events to a log file. Defaults to False.
            log_to_console: Whether to show intermediate steps (thoughts, tool calls)
                in the console. Defaults to True.
            event_subscriber: Optional callback invoked for each agent event (thought, tool call,
                tool result, done, error). Enables event-driven observation.
            experimental: Whether to include experimental tools. Defaults to False.
            disable_loop_detection: Whether to disable loop detection. Defaults to False.
        """
        self.name = "Windows Use"
        self.description = "An agent that can interact with GUI elements on Windows OS"
        self.mode = mode
        self.secrets = secrets
        self.registry = Registry(
            BUILTIN_TOOLS + EXPERIMENTAL_TOOLS if experimental else BUILTIN_TOOLS
        )
        self.instructions = instructions or []
        self.browser = browser
        self.auto_minimize = auto_minimize
        if use_annotation and not use_vision:
            logger.warning("use_vision is set to True if use_annotation is True.")
        if use_annotation and not use_accessibility:
            logger.warning("use_accessibility is set to True if use_annotation is True.")
        self.desktop = Desktop(
            use_vision=True if use_annotation else use_vision,
            use_annotation=use_annotation,
            use_accessibility=True if use_annotation else use_accessibility,
        )
        self.state = AgentState(
            max_consecutive_failures=max_consecutive_failures,
            max_steps=max_steps,
        )
        self.telemetry = ProductTelemetry()
        self.watchdog = WatchDog()
        self.console = Console()
        self.context = Context()
        self.log_to_file = log_to_file
        self.log_to_console = log_to_console
        self.llm = llm
        self.disable_loop_detection = disable_loop_detection
        self._loop_guard = LoopGuard()

        self.event = Event()
        if event_subscriber is not None:
            self.event.add_subscriber(event_subscriber)
        if log_to_console:
            self.event.add_subscriber(ConsoleEventSubscriber())
        if log_to_file:
            self.event.add_subscriber(FileEventSubscriber())

        self._cached_system_message: SystemMessage | None = None

    @property
    def system_message(self) -> SystemMessage:
        if self._cached_system_message is not None:
            return self._cached_system_message
        self._cached_system_message = self.context.system(
            mode=self.mode,
            desktop=self.desktop,
            browser=self.browser,
            max_steps=self.state.max_steps,
            instructions=self.instructions,
        )
        return self._cached_system_message
    
    @property
    def task_message(self) -> HumanMessage:
        return self.context.task(task=self.state.task)

    @property
    def tools(self):
        return self.registry.get_tools()

    @property
    def state_message(self) -> HumanMessage | ImageMessage:
        return self.context.state(
            query=self.state.task,
            step=self.state.step,
            max_steps=self.state.max_steps,
            desktop=self.desktop)

    def loop(self) -> AgentResult:
        """Run the main agent loop.

        Iterates up to max_steps, calling the LLM and executing tools each step.
        Tracks consecutive tool failures and aborts if the threshold is reached.

        Returns:
            AgentResult with the final answer or an error/timeout indication.
        """
        self.state.messages.insert(0, self.system_message)
        self.state.messages.append(self.task_message)
        consecutive_failures = 0
        self._loop_guard.reset()

        for step in range(self.state.max_steps):
            self.state.step = step

            # Check for loops and build state message with nudge
            nudge = None if self.disable_loop_detection else self._loop_guard.check()
            state_msg = self.context.state(
                query=self.state.task,
                step=step,
                max_steps=self.state.max_steps,
                desktop=self.desktop,
                nudge=nudge or "",
            )
            if nudge:
                self.event.emit(
                    AgentEvent(type=EventType.ERROR, data={"step": step, "error": f"Loop detected: {nudge}"})
                )
            self.state.messages.append(state_msg)

            # Record current desktop state for loop detection
            if not self.disable_loop_detection:
                self._loop_guard.record_state(self.desktop.desktop_state)

            # Reason: call LLM, retry on failure, return ToolMessage
            message: ToolMessage | None = None
            last_error: Exception | None = None
            for attempt in range(self.state.max_consecutive_failures):
                try:
                    messages = list(chain(self.state.messages, self.state.error_messages))
                    llm_event = self.llm.invoke(messages=messages, tools=self.tools)
                    match llm_event.type:
                        case LLMEventType.TOOL_CALL:
                            message = ToolMessage(
                                id=llm_event.tool_call.id,
                                name=llm_event.tool_call.name,
                                params=llm_event.tool_call.params,
                            )
                            break
                        case LLMEventType.TEXT:
                            ai_message = AIMessage(content=llm_event.content)
                            human_message = HumanMessage(
                                content="Response rejected, please use the `done_tool` to respond to the user."
                            )
                            self.state.error_messages.extend([ai_message, human_message])
                            continue
                except Exception as e:
                    last_error = e
                    if attempt < self.state.max_consecutive_failures - 1:
                        wait_time = 2 ** (attempt + 1)
                        logger.error(
                            f"Failed to get response from {self.llm.provider} "
                            f"for {self.llm.model_name}.\n"
                            f"Retrying...({attempt + 1}/{self.state.max_consecutive_failures})"
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(
                            f"Failed to get response from {self.llm.provider} "
                            f"for {self.llm.model_name}.\n"
                            f"All {self.state.max_consecutive_failures} attempts exhausted."
                        )

            if message is None:
                error = f"Agent failed after exhausting retries: {last_error}"
                self.event.emit(
                    AgentEvent(type=EventType.ERROR, data={"step": step, "error": error})
                )
                return AgentResult(is_done=False, error=error)

            self.state.messages.pop()  # Remove the previous state message

            tool_name = message.name
            tool_params = message.params

            thought = tool_params.get("thought", "")
            self.event.emit(
                AgentEvent(
                    type=EventType.THOUGHT,
                    data={"step": step, "thought": thought},
                )
            )

            if tool_name != "done_tool":
                self.event.emit(
                    AgentEvent(
                        type=EventType.TOOL_CALL,
                        data={
                            "step": step,
                            "tool_name": tool_name,
                            "tool_params": {
                                k: v
                                for k, v in tool_params.items()
                                if k not in _NON_TOOL_PARAMS
                            },
                        },
                    )
                )

            # Act: execute tool via registry
            tool_result = self.registry.execute(tool_name=tool_name, tool_params=tool_params, desktop=self.desktop)

            # Record action for loop detection
            if not self.disable_loop_detection:
                self._loop_guard.record_action(tool_name, tool_params, tool_result.is_success)

            if tool_result.is_success:
                content = tool_result.content
                message.content = content
                self.state.messages.append(message)
            else:
                content = tool_result.error
                message.content = content
                self.state.error_messages.append(message)

            if tool_name != "done_tool":
                self.event.emit(
                    AgentEvent(
                        type=EventType.TOOL_RESULT,
                        data={
                            "step": step,
                            "tool_name": tool_name,
                            "is_success": tool_result.is_success,
                            "content": content,
                        },
                    )
                )

            if not tool_result.is_success:
                consecutive_failures += 1
                if consecutive_failures >= self.state.max_consecutive_failures:
                    error = (
                        f"Agent aborted after {self.state.max_consecutive_failures} "
                        f"consecutive tool failures. Last error: {content}"
                    )
                    self.event.emit(
                        AgentEvent(type=EventType.ERROR, data={"step": step, "error": error})
                    )
                    return AgentResult(is_done=False, error=error)
            else:
                consecutive_failures = 0

            if tool_name == "done_tool":
                content = tool_params.get("answer", "")
                self.event.emit(
                    AgentEvent(type=EventType.DONE, data={"step": step, "content": content})
                )
                return AgentResult(content=content, is_done=True)

        error = f"Agent reached the maximum number of steps ({self.state.max_steps}) without completing."
        self.event.emit(
            AgentEvent(type=EventType.ERROR, data={"step": self.state.max_steps, "error": error})
        )
        return AgentResult(is_done=False, error=error)

    def invoke(self, task: str) -> AgentResult:
        self.state.reset()
        self.state.task = task
        try:
            with self.desktop.auto_minimize() if self.auto_minimize else nullcontext():
                self.watchdog.set_focus_callback(self.desktop.tree.on_focus_change)
                with self.watchdog:
                    result = self.loop()
            self.telemetry.capture(AgentTelemetryEvent(
                query=task,
                steps=self.state.step,
                max_steps=self.state.max_steps,
                model=self.llm.model_name,
                provider=self.llm.provider,
                use_vision=self.desktop.use_vision,
                answer=result.content,
                error=result.error,
                is_success=result.is_done,
            ))
            self.telemetry.flush()
            return result
        except Exception as e:
            self.event.emit(
                AgentEvent(
                    type=EventType.ERROR,
                    data={"step": self.state.step, "error": str(e)},
                )
            )
            self.telemetry.capture(AgentTelemetryEvent(
                query=task,
                steps=self.state.step,
                max_steps=self.state.max_steps,
                model=self.llm.model_name,
                provider=self.llm.provider,
                use_vision=self.desktop.use_vision,
                error=str(e),
                is_success=False,
            ))
            self.telemetry.flush()

    async def aloop(self) -> AgentResult:
        """Run the main agent loop asynchronously."""
        import asyncio
        self.state.messages.insert(0, self.system_message)
        self.state.messages.append(self.task_message)
        consecutive_failures = 0
        self._loop_guard.reset()

        for step in range(self.state.max_steps):
            self.state.step = step

            # Check for loops and build state message with nudge
            nudge = None if self.disable_loop_detection else self._loop_guard.check()
            state_msg = self.context.state(
                query=self.state.task,
                step=step,
                max_steps=self.state.max_steps,
                desktop=self.desktop,
                nudge=nudge or "",
            )
            if nudge:
                self.event.emit(
                    AgentEvent(type=EventType.ERROR, data={"step": step, "error": f"Loop detected: {nudge}"})
                )
            self.state.messages.append(state_msg)

            # Record current desktop state for loop detection
            if not self.disable_loop_detection:
                self._loop_guard.record_state(self.desktop.desktop_state)

            message: ToolMessage | None = None
            last_error: Exception | None = None
            for attempt in range(self.state.max_consecutive_failures):
                try:
                    messages = list(chain(self.state.messages, self.state.error_messages))
                    llm_event = await self.llm.ainvoke(messages=messages, tools=self.tools)
                    match llm_event.type:
                        case LLMEventType.TOOL_CALL:
                            message = ToolMessage(
                                id=llm_event.tool_call.id,
                                name=llm_event.tool_call.name,
                                params=llm_event.tool_call.params,
                            )
                            break
                        case LLMEventType.TEXT:
                            ai_message = AIMessage(content=llm_event.content)
                            human_message = HumanMessage(
                                content="Response rejected, please use the `done_tool` to respond to the user."
                            )
                            self.state.error_messages.extend([ai_message, human_message])
                            continue
                except Exception as e:
                    last_error = e
                    if attempt < self.state.max_consecutive_failures - 1:
                        wait_time = 2 ** (attempt + 1)
                        logger.error(
                            f"Failed to get response from {self.llm.provider} "
                            f"for {self.llm.model_name}.\n"
                            f"Retrying...({attempt + 1}/{self.state.max_consecutive_failures})"
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(
                            f"Failed to get response from {self.llm.provider} "
                            f"for {self.llm.model_name}.\n"
                            f"All {self.state.max_consecutive_failures} attempts exhausted."
                        )

            if message is None:
                error = f"Agent failed after exhausting retries: {last_error}"
                self.event.emit(
                    AgentEvent(type=EventType.ERROR, data={"step": step, "error": error})
                )
                return AgentResult(is_done=False, error=error)

            self.state.messages.pop()  # Remove the previous state message

            tool_name = message.name
            tool_params = message.params

            thought = tool_params.get("thought", "")
            self.event.emit(
                AgentEvent(
                    type=EventType.THOUGHT,
                    data={"step": step, "thought": thought},
                )
            )

            if tool_name != "done_tool":
                self.event.emit(
                    AgentEvent(
                        type=EventType.TOOL_CALL,
                        data={
                            "step": step,
                            "tool_name": tool_name,
                            "tool_params": {
                                k: v
                                for k, v in tool_params.items()
                                if k not in _NON_TOOL_PARAMS
                            },
                        },
                    )
                )

            # Act: execute tool via registry asynchronously
            tool_result = await self.registry.aexecute(tool_name=tool_name, tool_params=tool_params, desktop=self.desktop)

            # Record action for loop detection
            if not self.disable_loop_detection:
                self._loop_guard.record_action(tool_name, tool_params, tool_result.is_success)

            if tool_result.is_success:
                content = tool_result.content
                message.content = content
                self.state.messages.append(message)
            else:
                content = tool_result.error
                message.content = content
                self.state.error_messages.append(message)

            if tool_name != "done_tool":
                self.event.emit(
                    AgentEvent(
                        type=EventType.TOOL_RESULT,
                        data={
                            "step": step,
                            "tool_name": tool_name,
                            "is_success": tool_result.is_success,
                            "content": content,
                        },
                    )
                )

            if not tool_result.is_success:
                consecutive_failures += 1
                if consecutive_failures >= self.state.max_consecutive_failures:
                    error = (
                        f"Agent aborted after {self.state.max_consecutive_failures} "
                        f"consecutive tool failures. Last error: {content}"
                    )
                    self.event.emit(
                        AgentEvent(type=EventType.ERROR, data={"step": step, "error": error})
                    )
                    return AgentResult(is_done=False, error=error)
            else:
                consecutive_failures = 0

            if tool_name == "done_tool":
                content = tool_params.get("answer", "")
                self.event.emit(
                    AgentEvent(type=EventType.DONE, data={"step": step, "content": content})
                )
                return AgentResult(content=content, is_done=True)

        error = f"Agent reached the maximum number of steps ({self.state.max_steps}) without completing."
        self.event.emit(
            AgentEvent(type=EventType.ERROR, data={"step": self.state.max_steps, "error": error})
        )
        return AgentResult(is_done=False, error=error)

    async def ainvoke(self, task: str) -> AgentResult:
        self.state.reset()
        self.state.task = task
        try:
            with self.desktop.auto_minimize() if self.auto_minimize else nullcontext():
                self.watchdog.set_focus_callback(self.desktop.tree.on_focus_change)
                with self.watchdog:
                    result = await self.aloop()
            self.telemetry.capture(AgentTelemetryEvent(
                query=task,
                steps=self.state.step,
                max_steps=self.state.max_steps,
                model=self.llm.model_name,
                provider=self.llm.provider,
                use_vision=self.desktop.use_vision,
                answer=result.content,
                error=result.error,
                is_success=result.is_done,
            ))
            self.telemetry.flush()
            return result
        except Exception as e:
            self.event.emit(
                AgentEvent(
                    type=EventType.ERROR,
                    data={"step": self.state.step, "error": str(e)},
                )
            )
            self.telemetry.capture(AgentTelemetryEvent(
                query=task,
                steps=self.state.step,
                max_steps=self.state.max_steps,
                model=self.llm.model_name,
                provider=self.llm.provider,
                use_vision=self.desktop.use_vision,
                error=str(e),
                is_success=False,
            ))
            self.telemetry.flush()
