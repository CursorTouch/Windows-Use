from windows_use.agent.tools.service import (click_tool, type_tool, shell_tool, done_tool, multi_select_tool,memory_tool,
shortcut_tool, scroll_tool, drag_tool, move_tool, wait_tool, app_tool, scrape_tool, multi_edit_tool)
from windows_use.messages import SystemMessage, HumanMessage, AIMessage, ImageMessage
from windows_use.telemetry.views import AgentTelemetryEvent
from windows_use.telemetry.service import ProductTelemetry
from windows_use.agent.views import AgentResult,AgentStep
from windows_use.agent.registry.service import Registry
from windows_use.agent.registry.views import ToolResult
from windows_use.agent.utils import extract_agent_data
from windows_use.agent.desktop.service import Desktop
from windows_use.agent.desktop.views import Browser
from windows_use.agent.prompt.service import Prompt
from live_inspect.watch_cursor import WatchCursor
from windows_use.llms.base import BaseChatLLM
from contextlib import nullcontext
from rich.markdown import Markdown
from rich.console import Console
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Agent:
    def __init__(self,instructions:list[str]=[],browser:Browser=Browser.EDGE, llm: BaseChatLLM=None,max_consecutive_failures:int=3,max_steps:int=25,use_vision:bool=False,auto_minimize:bool=False):
        self.name='Windows Use'
        self.description='An agent that can interact with GUI elements on Windows OS' 
        self.registry = Registry([
            click_tool,type_tool, app_tool, shell_tool, done_tool, 
            shortcut_tool, scroll_tool, drag_tool, move_tool,memory_tool,
            wait_tool, scrape_tool, multi_select_tool, multi_edit_tool
        ])
        self.instructions=instructions
        self.browser=browser
        self.agent_step=AgentStep(max_steps=max_steps)
        self.max_consecutive_failures=max_consecutive_failures
        self.auto_minimize=auto_minimize
        self.use_vision=use_vision
        self.llm = llm
        self.telemetry=ProductTelemetry()
        self.watch_cursor = WatchCursor()
        self.desktop = Desktop()
        self.console=Console()

    def invoke(self,query: str)->AgentResult:
        """Invoke the agent with a query."""
        if query.strip()=='':
            return AgentResult(is_done=False, error="Query is empty. Please provide a valid query.")
        try:
            with (self.desktop.auto_minimize() if self.auto_minimize else nullcontext()):
                with self.watch_cursor:
                    desktop_state = self.desktop.get_state(use_vision=self.use_vision)
                    language=self.desktop.get_default_language()
                    tools_prompt = self.registry.get_tools_prompt()
                    observation="The desktop is ready to operate."
                    system_prompt=Prompt.system_prompt(desktop=self.desktop,
                        browser=self.browser,language=language,instructions=self.instructions,
                        tools_prompt=tools_prompt,max_steps=self.agent_step.max_steps
                    )
                    history = []
                    
                    while True:
                        if self.agent_step.steps>self.agent_step.max_steps:
                            # ... (telemetry and error return logic remains same) ...
                            self.telemetry.capture(AgentTelemetryEvent(
                                query=query,
                                error="Max steps reached",
                                steps=self.agent_step.steps,
                                max_steps=self.agent_step.max_steps,
                                use_vision=self.use_vision,
                                model=self.llm.model_name,
                                provider=self.llm.provider,
                                is_success=False
                            ))
                            return AgentResult(is_done=False, error="Max steps reached")
                        
                        # MDP: Construct messages fresh at every step
                        human_prompt=Prompt.observation_prompt(
                            query=query,
                            agent_step=self.agent_step,
                            tool_result=ToolResult(is_success=True, content=observation), 
                            desktop_state=desktop_state,
                            history=history
                        )
                        
                        messages=[
                            SystemMessage(content=system_prompt),
                            ImageMessage(content=human_prompt,image=desktop_state.screenshot,mime_type="image/png") 
                                if self.use_vision and desktop_state.screenshot else 
                            HumanMessage(content=human_prompt)
                        ]

                        for consecutive_failures in range(1,self.max_consecutive_failures+1):
                            try:
                                llm_response=self.llm.invoke(messages)
                                agent_data=extract_agent_data(llm_response)
                                break
                            except Exception as e:
                                logger.error(f"[LLM]: {e}. Retrying attempt {consecutive_failures+1}...")
                                if consecutive_failures==self.max_consecutive_failures:
                                    # ... (telemetry and error return) ...
                                    self.telemetry.capture(AgentTelemetryEvent(
                                        query=query,
                                        error=str(e),
                                        steps=self.agent_step.steps,
                                        max_steps=self.agent_step.max_steps,
                                        use_vision=self.use_vision,
                                        model=self.llm.model_name,
                                        provider=self.llm.provider,
                                        is_success=False
                                    ))
                                    return AgentResult(is_done=False, error=str(e))

                        logger.info(f"[Agent] 🎯 Step: {self.agent_step.steps}")
                        logger.info(f"[Agent] 📝 Evaluate: {agent_data.evaluate}")
                        logger.info(f"[Agent] 💭 Thought: {agent_data.thought}")

                        action=agent_data.action
                        action_name=action.name
                        params=action.params

                        # Update History
                        history_entry = f"Step {self.agent_step.steps}: Action={action_name}({', '.join(f'{k}={v}' for k, v in params.items())})"
                        
                        if action_name.startswith('Done'):
                            action_response=self.registry.execute(tool_name=action_name, desktop=None, **params)
                            answer=action_response.content
                            logger.info(f"[Agent] 📜 Final-Answer: {answer}\n")
                            # For Done tool, we don't need to loop again, just return
                            break
                        else:
                            logger.info(f"[Tool] 🔧 Action: {action_name}({', '.join(f'{k}={v}' for k, v in params.items())})")
                            action_response=self.registry.execute(tool_name=action_name, desktop=self.desktop, **params)
                            observation=action_response.content if action_response.is_success else action_response.error
                            logger.info(f"[Tool] 📝 Observation: {observation}\n")
                            
                            # Append result to history
                            history_entry += f" -> Observation={observation[:200]}..." # Truncate observation for history to save tokens
                            
                            desktop_state = self.desktop.get_state(use_vision=self.use_vision)
                            # Loop continues, regenerating messages with new history and state

                        history.append(history_entry)
                        self.agent_step.step_increment()
                
                self.telemetry.capture(AgentTelemetryEvent(
                    query=query,
                    steps=self.agent_step.steps,
                    max_steps=self.agent_step.max_steps,
                    answer=answer,
                    use_vision=self.use_vision,
                    model=self.llm.model_name,
                    provider=self.llm.provider,
                    is_success=True
                ))
            self.agent_step.reset()
            return AgentResult(is_done=True,content=answer)
        except KeyboardInterrupt:
            logger.warning("[Agent] ⚠️: Interrupted by user (Ctrl+C).")
            self.telemetry.flush()
            return AgentResult(is_done=False, error="Interrupted by user")
        
    def print_response(self,query: str):
        """Print the response from the agent."""
        response=self.invoke(query)
        self.console.print(Markdown(response.content or response.error))