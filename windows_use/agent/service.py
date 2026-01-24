from windows_use.agent.tools.service import (click_tool, type_tool, shell_tool, done_tool,
shortcut_tool, scroll_tool, move_tool, wait_tool, app_tool, scrape_tool, desktop_tool)
from windows_use.messages import SystemMessage, HumanMessage, AIMessage, ImageMessage
from windows_use.telemetry.views import AgentTelemetryEvent
from windows_use.telemetry.service import ProductTelemetry
from windows_use.agent.registry.service import Registry
from windows_use.agent.watchdog.service import WatchDog
from windows_use.agent.registry.views import ToolResult
from windows_use.agent.desktop.service import Desktop
from windows_use.agent.desktop.views import Browser
from windows_use.agent.prompt.service import Prompt
from windows_use.agent.views import AgentResult
from windows_use.agent.utils import json_parser
from windows_use.llms.base import BaseChatLLM
from windows_use.uia import Control
from contextlib import nullcontext
from rich.markdown import Markdown
from rich.console import Console
from typing import Literal
import logging
import time

logger = logging.getLogger("windows_use")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Agent:
    def __init__(self,mode:Literal["flash","full"]="full",instructions:list[str]=[],browser:Browser=Browser.EDGE, use_annotation:bool=False, llm: BaseChatLLM=None,max_consecutive_failures:int=3,max_steps:int=25,use_vision:bool=False,auto_minimize:bool=False):
        '''
        Initialize the Windows Use Agent.

        The Agent is the core component that orchestrates interactions with the Windows GUI.
        It uses an LLM to process instructions, analyze the desktop state (via UI automation 
        and optionally vision), and execute tools to achieve the desired goals.

        Args:
            instructions (list[str]): A list of additional instructions or goals for the agent to execute.
            browser (Browser): The target web browser for web-related tasks. Defaults to Browser.EDGE.
            use_annotation (bool): Whether to overlay UI element annotations on screenshots before providing to the LLM. Defaults to False.
            llm (BaseChatLLM): The Large Language Model instance used for decision making.
            max_consecutive_failures (int): Maximum number of consecutive failures before giving up.
            max_steps (int): Maximum number of steps allowed in the agent's execution.
            use_vision (bool): Whether to provide screenshots to the LLM. Defaults to False.
            auto_minimize (bool): Whether to automatically minimize the current window before agent proceeds. Defaults to False.
        '''
        self.name='Windows Use'
        self.description='An agent that can interact with GUI elements on Windows OS'
        self.mode=mode
        self.registry = Registry([
            click_tool,type_tool, app_tool, shell_tool, done_tool, 
            shortcut_tool, scroll_tool, move_tool,wait_tool,
            scrape_tool, desktop_tool
        ])
        self.instructions=instructions
        self.browser=browser
        self.max_steps=max_steps
        self.max_consecutive_failures=max_consecutive_failures
        self.auto_minimize=auto_minimize
        self.use_annotation=use_annotation
        if self.use_annotation and not use_vision:
            logger.warning("use_vision is set to True if use_annotation is True.")
        self.use_vision=True if use_annotation else use_vision
        self.llm = llm
        self.telemetry=ProductTelemetry()
        self.watchdog = WatchDog()
        self.desktop = Desktop()
        self.console=Console()

    def invoke(self,query: str)->AgentResult:
        """
        Executes a natural language query by orchestrating interactions with the Windows GUI.

        This method serves as the primary entry point for the agent. It captures the current 
        desktop state, initializes monitoring via the watchdog, and manages a multi-step 
        execution loop where the LLM analyzes the environment and selects tools to 
        fulfill the user's request.

        Args:
            query (str): The natural language instruction or task for the agent to perform.

        Returns:
            AgentResult: The final result of the execution, indicating success or failure 
                        and providing a summary of the actions taken.
        """
        if query.strip()=='':
            return AgentResult(is_done=False, error="Query is empty. Please provide a valid query.")
        self.console.clear()
        try:
            task_start_time = time.time()
            with (self.desktop.auto_minimize() if self.auto_minimize else nullcontext()):
                self.watchdog.set_focus_callback(self.desktop.tree.on_focus_change)
                with self.watchdog:
                    desktop_state = self.desktop.get_state(use_annotation=self.use_annotation,use_vision=self.use_vision)
                    language=self.desktop.get_default_language()
                    observation="The desktop is ready to operate."
                    system_prompt=Prompt.system_prompt(mode=self.mode,desktop=self.desktop,
                        browser=self.browser,language=language,instructions=self.instructions,
                        max_steps=self.max_steps
                    )
                    
                    step = 0
                    human_prompt=Prompt.observation_prompt(query=query,step=step, max_steps=self.max_steps,
                        tool_result=ToolResult(is_success=True, content=observation), desktop_state=desktop_state
                    )
                    tools=self.registry.get_tools()
                    messages=[
                        SystemMessage(content=system_prompt),
                        ImageMessage(content=human_prompt,image=desktop_state.screenshot,mime_type="image/png") 
                            if self.use_vision and desktop_state.screenshot else 
                        HumanMessage(content=human_prompt)
                    ]
                    while step < self.max_steps:
                        step_start_time = time.time()
                        step += 1
                        
                        logger.info(f"[Agent] 🎯 Step: {step}/{self.max_steps}")
                        
                        error_messages=[]

                        # Retry logic for LLM failures
                        for consecutive_failures in range(1, self.max_consecutive_failures + 1):
                            try:
                                llm_response = self.llm.invoke(messages+error_messages,tools=tools, json_mode=False)
                                agent_data = json_parser(llm_response)
                                break
                            except ValueError as e:
                                error_messages.clear()
                                error_messages.append(llm_response.content)
                                error_messages.append(HumanMessage(content=f"Response rejected, invalid response format\nError: {e}\nAdhere to the format specified in <output_contract>"))
                                logger.warning(f"[LLM]: Invalid response format, Retrying attempt {consecutive_failures}/{self.max_consecutive_failures}...\nResponse: {llm_response.content}")
                                if consecutive_failures == self.max_consecutive_failures:
                                    self.telemetry.capture(AgentTelemetryEvent(
                                        query=query,
                                        error=str(e),
                                        steps=step,
                                        max_steps=self.max_steps,
                                        use_vision=self.use_vision,
                                        model=self.llm.model_name,
                                        provider=self.llm.provider,
                                        is_success=False
                                    ))
                                    return AgentResult(is_done=False, error=str(e))
                            except Exception as e:
                                logger.error(f"[LLM]: Failed to generate response. Retrying attempt {consecutive_failures}/{self.max_consecutive_failures}...\nError: {e}")
                                if consecutive_failures == self.max_consecutive_failures:
                                    self.telemetry.capture(AgentTelemetryEvent(
                                        query=query,
                                        error=str(e),
                                        steps=step,
                                        max_steps=self.max_steps,
                                        use_vision=self.use_vision,
                                        model=self.llm.model_name,
                                        provider=self.llm.provider,
                                        is_success=False
                                    ))
                                    return AgentResult(is_done=False, error=str(e))

                        logger.info(f"[Agent] 📝 Evaluate: {agent_data.evaluate}")
                        logger.info(f"[Agent] 💭 Thought: {agent_data.thought}")

                        # Remove previous Desktop State Human Message
                        messages.pop()
                        human_prompt = Prompt.previous_observation_prompt(query=query,step=step,max_steps=self.max_steps, observation=observation)
                        human_message = HumanMessage(content=human_prompt)
                        messages.append(human_message)

                        ai_prompt = Prompt.action_prompt(agent_data=agent_data)
                        ai_message = AIMessage(content=ai_prompt)
                        messages.append(ai_message)

                        action = agent_data.action
                        action_name = action.name
                        params = action.params

                        if action_name.lower().startswith('done_tool'):
                            action_response = self.registry.execute(tool_name=action_name, desktop=None, **params)
                            answer = action_response.content
                            logger.info(f"[Agent] 📜 Final-Answer: {answer}\n")
                            agent_data.observation = answer

                            step_end_time = time.time()
                            step_duration = step_end_time - step_start_time
                            logger.info(f"[Agent] ⌛ Step {step} took {step_duration:.2f} seconds")

                            task_duration = time.time() - task_start_time
                            logger.info(f"[Agent] 🏁 Task completed in {task_duration:.2f} seconds")
                            
                            human_prompt = Prompt.answer_prompt(agent_data=agent_data, tool_result=action_response)
                            break  # Exit the while loop successfully
                        else:
                            logger.info(f"[Tool] 🔧 Action: {action_name}({', '.join(f'{k}={v}' for k, v in params.items())})")
                            action_response = self.registry.execute(tool_name=action_name, desktop=self.desktop, **params)
                            observation = action_response.content if action_response.is_success else action_response.error
                            logger.info(f"[Tool] 📝 Observation: {observation}\n")
                            agent_data.observation = observation

                            step_end_time = time.time()
                            step_duration = step_end_time - step_start_time
                            logger.info(f"[Agent] ⌛ Step {step} took {step_duration:.2f} seconds")

                            desktop_state = self.desktop.get_state(use_annotation=self.use_annotation,use_vision=self.use_vision)
                            human_prompt = Prompt.observation_prompt(query=query, step=step, max_steps=self.max_steps,
                                tool_result=action_response, desktop_state=desktop_state
                            )
                            human_message = ImageMessage(content=human_prompt, image=desktop_state.screenshot, mime_type="image/png") if self.use_vision and desktop_state.screenshot else HumanMessage(content=human_prompt)
                            messages.append(human_message)

                
                # Check if max steps reached (loop exited without Done action)
                if step >= self.max_steps:
                    self.telemetry.capture(AgentTelemetryEvent(
                        query=query,
                        error="Max steps reached",
                        steps=step,
                        max_steps=self.max_steps,
                        use_vision=self.use_vision,
                        model=self.llm.model_name,
                        provider=self.llm.provider,
                        is_success=False
                    ))
                    task_duration = time.time() - task_start_time
                    logger.info(f"[Agent] 🛑 Task failed (max steps) in {task_duration:.2f} seconds")
                    return AgentResult(is_done=False, error="Max steps reached")
                
                self.telemetry.capture(AgentTelemetryEvent(
                    query=query,
                    steps=step,
                    max_steps=self.max_steps,
                    answer=answer,
                    use_vision=self.use_vision,
                    model=self.llm.model_name,
                    provider=self.llm.provider,
                    is_success=True
                ))

            return AgentResult(is_done=True,content=answer)
        except KeyboardInterrupt:
            logger.warning("[Agent] ⚠️: Interrupted by user (Ctrl+C).")
            self.telemetry.flush()
            return AgentResult(is_done=False, error="Interrupted by user")
        
    def print_response(self,query: str):
        """Print the response from the agent."""
        response=self.invoke(query)
        self.console.print(Markdown(response.content or response.error))