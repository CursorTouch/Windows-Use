from windows_use.agent.tools.service import (click_tool, type_tool, shell_tool, done_tool, multi_select_tool,memory_tool,
shortcut_tool, scroll_tool, drag_tool, move_tool, wait_tool, app_tool, scrape_tool, multi_edit_tool)
from windows_use.messages import SystemMessage, HumanMessage, AIMessage, ImageMessage
from windows_use.telemetry.views import AgentTelemetryEvent
from windows_use.telemetry.service import ProductTelemetry
from windows_use.agent.registry.service import Registry
from windows_use.agent.registry.views import ToolResult
from windows_use.agent.utils import extract_agent_data
from windows_use.agent.desktop.service import Desktop
from windows_use.agent.desktop.views import Browser
from windows_use.agent.prompt.service import Prompt
from live_inspect.watch_cursor import WatchCursor
from windows_use.agent.views import AgentResult
from windows_use.llms.base import BaseChatLLM
from windows_use.exceptions import (
    WindowsUseError, LLMError, DesktopInteractionError, 
    ToolExecutionError, ValidationError, TimeoutError
)
from contextlib import nullcontext
from rich.markdown import Markdown
from rich.console import Console
from typing import Optional, List
from windows_use.logging import get_logger
import logging
import time

logger = get_logger("windows_use.agent")

class Agent:
    def __init__(
        self,
        instructions: List[str] = None,
        browser: Browser = Browser.EDGE, 
        llm: Optional[BaseChatLLM] = None,
        max_consecutive_failures: int = 3,
        max_steps: int = 25,
        use_vision: bool = False,
        auto_minimize: bool = False
    ) -> None:
        self.name='Windows Use'
        self.description='An agent that can interact with GUI elements on Windows OS' 
        self.registry = Registry([
            click_tool,type_tool, app_tool, shell_tool, done_tool, 
            shortcut_tool, scroll_tool, drag_tool, move_tool,memory_tool,
            wait_tool, scrape_tool, multi_select_tool, multi_edit_tool
        ])
        self.instructions = instructions or []
        self.browser=browser
        self.max_steps=max_steps
        self.max_consecutive_failures=max_consecutive_failures
        self.auto_minimize=auto_minimize
        self.use_vision=use_vision
        self.llm = llm
        self.telemetry=ProductTelemetry()
        self.watch_cursor = WatchCursor()
        self.desktop = Desktop()
        self.console=Console()

    def invoke(self, query: str) -> AgentResult:
        if query.strip()=='':
            raise ValidationError(
                "Query cannot be empty", 
                field="query", 
                value=query, 
                expected="non-empty string"
            )
        try:
            with (self.desktop.auto_minimize() if self.auto_minimize else nullcontext()):
                with self.watch_cursor:
                    desktop_state = self.desktop.get_state(use_vision=self.use_vision)
                    language=self.desktop.get_default_language()
                    tools_prompt = self.registry.get_tools_prompt()
                    observation="The desktop is ready to operate."
                    system_prompt=Prompt.system_prompt(desktop=self.desktop,
                        browser=self.browser,language=language,instructions=self.instructions,
                        tools_prompt=tools_prompt,max_steps=self.max_steps
                    )
                    human_prompt=Prompt.observation_prompt(query=query,steps=0,max_steps=self.max_steps,
                        tool_result=ToolResult(is_success=True, content=observation), desktop_state=desktop_state
                    )
                    agent_log=[]
                    messages=[
                        SystemMessage(content=system_prompt),
                        ImageMessage(content=human_prompt,image=desktop_state.screenshot,mime_type="image/png") 
                            if self.use_vision and desktop_state.screenshot else 
                        HumanMessage(content=human_prompt)
                    ]
                    for steps in range(1,self.max_steps+1):
                        if steps==self.max_steps:
                            timeout_error = TimeoutError(
                                f"Agent reached maximum steps limit ({self.max_steps})",
                                timeout_seconds=None,
                                operation="agent_execution",
                                details={"max_steps": self.max_steps, "query": query}
                            )
                            self.telemetry.capture(AgentTelemetryEvent(
                                query=query,
                                error=str(timeout_error),
                                use_vision=self.use_vision,
                                model=self.llm.model_name,
                                provider=self.llm.provider,
                                agent_log=agent_log
                            ))
                            return AgentResult(is_done=False, error=str(timeout_error))
                        
                        for consecutive_failures in range(1,self.max_consecutive_failures+1):
                            try:
                                start_time = time.time()
                                llm_response=self.llm.invoke(messages)
                                response_time = time.time() - start_time
                                
                                logger.log_llm_interaction(
                                    provider=self.llm.provider,
                                    model=self.llm.model_name,
                                    response_time=response_time
                                )
                                
                                agent_data=extract_agent_data(llm_response)
                                break
                            except Exception as e:
                                logger.error(
                                    f"LLM invocation failed (attempt {consecutive_failures}/{self.max_consecutive_failures})",
                                    provider=self.llm.provider,
                                    model=self.llm.model_name,
                                    attempt=consecutive_failures,
                                    error=str(e),
                                    exc_info=True
                                )
                                if consecutive_failures==self.max_consecutive_failures:
                                    llm_error = LLMError(
                                        f"LLM failed after {self.max_consecutive_failures} attempts: {str(e)}",
                                        provider=self.llm.provider,
                                        model=self.llm.model_name,
                                        details={"original_error": str(e), "attempts": consecutive_failures}
                                    )
                                    self.telemetry.capture(AgentTelemetryEvent(
                                        query=query,
                                        error=str(llm_error),
                                        use_vision=self.use_vision,
                                        model=self.llm.model_name,
                                        provider=self.llm.provider,
                                        agent_log=agent_log
                                    ))
                                    return AgentResult(is_done=False, error=str(llm_error))

                        logger.log_agent_step(
                            step=steps,
                            action=agent_data.action.name if agent_data.action else "unknown",
                            thought=agent_data.thought,
                            observation=agent_data.evaluate
                        )

                        messages.pop() #Remove previous Desktop State Human Message
                        human_prompt=Prompt.previous_observation_prompt(steps=steps-1,max_steps=self.max_steps,observation=observation)
                        human_message=HumanMessage(content=human_prompt)
                        messages.append(human_message)

                        ai_prompt=Prompt.action_prompt(agent_data=agent_data)
                        ai_message=AIMessage(content=ai_prompt)
                        messages.append(ai_message)

                        action=agent_data.action
                        action_name=action.name
                        params=action.params

                        if action_name.startswith('Done'):
                            start_time = time.time()
                            action_response=self.registry.execute(tool_name=action_name, desktop=None, **params)
                            execution_time = time.time() - start_time
                            
                            answer=action_response.content
                            logger.log_tool_execution(
                                tool_name=action_name,
                                parameters=params,
                                result=answer,
                                success=action_response.is_success,
                                execution_time=execution_time
                            )
                            logger.info(f"📜 Task completed: {answer}")
                            agent_data.observation=answer
                            agent_log.append(agent_data.model_dump_json())
                            human_prompt=Prompt.answer_prompt(agent_data=agent_data,tool_result=action_response)
                            break
                        else:
                            start_time = time.time()
                            action_response=self.registry.execute(tool_name=action_name, desktop=self.desktop, **params)
                            execution_time = time.time() - start_time
                            
                            observation=action_response.content if action_response.is_success else action_response.error
                            
                            logger.log_tool_execution(
                                tool_name=action_name,
                                parameters=params,
                                result=observation,
                                success=action_response.is_success,
                                execution_time=execution_time
                            )
                            
                            agent_data.observation=observation
                            agent_log.append(agent_data.model_dump_json())

                            desktop_state = self.desktop.get_state(use_vision=self.use_vision)
                            human_prompt=Prompt.observation_prompt(query=query,steps=steps,max_steps=self.max_steps,
                                tool_result=action_response,desktop_state=desktop_state
                            )
                            human_message=ImageMessage(content=human_prompt,image=desktop_state.screenshot,mime_type="image/png") if self.use_vision and desktop_state.screenshot else HumanMessage(content=human_prompt)
                            messages.append(human_message)
                
                self.telemetry.capture(AgentTelemetryEvent(
                    query=query,
                    answer=answer,
                    use_vision=self.use_vision,
                    model=self.llm.model_name,
                    provider=self.llm.provider,
                    agent_log=agent_log
                ))
            return AgentResult(is_done=True,content=answer)
        except KeyboardInterrupt:
            logger.warning("[Agent] ⚠️: Interrupted by user (Ctrl+C).")
            self.telemetry.flush()
            return AgentResult(is_done=False, error="Interrupted by user")
        
    def print_response(self,query: str):
        response=self.invoke(query)
        self.console.print(Markdown(response.content or response.error))