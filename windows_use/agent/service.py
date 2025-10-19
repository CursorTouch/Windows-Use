from windows_use.agent.tools.service import (click_tool, type_tool, shell_tool, done_tool, multi_select_tool,
shortcut_tool, scroll_tool, drag_tool, move_tool, wait_tool, app_tool, scrape_tool, multi_edit_tool)
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from windows_use.agent.utils import extract_agent_data, image_message
from langchain_core.language_models.chat_models import BaseChatModel
from windows_use.telemetry.views import AgentTelemetryEvent
from windows_use.telemetry.service import ProductTelemetry
from windows_use.agent.registry.service import Registry
from windows_use.agent.registry.views import ToolResult
from windows_use.agent.desktop.service import Desktop
from windows_use.agent.desktop.views import Browser
from windows_use.agent.prompt.service import Prompt
from live_inspect.watch_cursor import WatchCursor
from langgraph.graph import START,END,StateGraph
from windows_use.agent.views import AgentResult
from windows_use.agent.state import AgentState
from contextlib import nullcontext
from rich.markdown import Markdown
from rich.console import Console
from textwrap import shorten
from typing import cast
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Agent:
    '''
    Windows Use

    An agent that can interact with GUI elements on Windows

    Args:
        instructions (list[str], optional): Instructions for the agent. Defaults to [].
        browser (Browser, optional): Browser the agent should use (Make sure this browser is installed). Defaults to 'Edge'.
        additional_tools (list[BaseTool], optional): Additional tools for the agent. Defaults to [].
        llm (BaseChatModel): Language model for the agent. Defaults to None.
        consecutive_failures (int, optional): Maximum number of consecutive failures for the agent. Defaults to 3.
        max_steps (int, optional): Maximum number of steps for the agent. Defaults to 100.
        use_vision (bool, optional): Whether to use vision for the agent. Defaults to False.
        auto_minimize (bool, optional): Whether to automatically minimize the IDE while agent is working. Defaults to False.

    Returns:
        Agent
    '''
    def __init__(self,instructions:list[str]=[],browser:Browser=Browser.EDGE, llm: BaseChatModel=None,max_consecutive_failures:int=3,max_steps:int=25,use_vision:bool=False,auto_minimize:bool=False):
        self.name='Windows Use'
        self.description='An agent that can interact with GUI elements on Windows OS' 
        self.registry = Registry([
            click_tool,type_tool, app_tool, shell_tool, done_tool, 
            shortcut_tool, scroll_tool, drag_tool, move_tool,
            wait_tool, scrape_tool, multi_select_tool, multi_edit_tool
        ])
        self.instructions=instructions
        self.browser=browser
        self.max_steps=max_steps
        self.consecutive_failures=max_consecutive_failures
        self.auto_minimize=auto_minimize
        self.use_vision=use_vision
        self.llm = llm
        self.telemetry=ProductTelemetry()
        self.watch_cursor = WatchCursor()
        self.desktop = Desktop()
        self.console=Console()
        self.graph=self.create_graph()

    def reason(self,state:AgentState):
        '''
        Reason about the next action based on the current state of the agent.

        Args:
            state (AgentState): The current state of the agent.

        Returns:
            dict: The next state of the agent after reasoning.
        '''
        steps=state.get('steps')
        max_steps=state.get('max_steps')
        max_consecutive_failures=state.get('max_consecutive_failures')
        consecutive_failures=state.get('consecutive_failures')
        messages=state.get('messages')
        error=''
        
        while consecutive_failures<=max_consecutive_failures:
            message=self.llm.invoke(messages)
            try:
                agent_data = extract_agent_data(message=message)
                break
            except Exception as e:
                error=e
                print("=" * 50)
                print(f"[Retry {consecutive_failures}] Failed to extract agent data")
                print("=" * 50)
                print("LLM Response Content:")
                print(message.content)
                print("=" * 50)
                consecutive_failures+=1
        if consecutive_failures>max_consecutive_failures:
            error_msg = f"Failed to extract agent data after {max_consecutive_failures} retries.\nError:{error}"
            print(error_msg)
            return {**state,'agent_data':None,'error':error_msg}
        logger.info(f"[Agent]🎯: Step: {steps}")
        logger.info(f"[Agent]📝: Evaluate: {agent_data.evaluate}")
        logger.info(f"[Agent] 💭: Thought: {agent_data.thought}")

        last_message = state.get('messages').pop()
        if isinstance(last_message, HumanMessage):
            message=HumanMessage(content=Prompt.previous_observation_prompt(steps=steps,max_steps=max_steps,observation=state.get('previous_observation')))
            return {**state,'actions':[agent_data.action],'agent_data':agent_data,'messages':[message],'steps':steps+1}
        
    def action(self,state:AgentState):
        """
        Execute the action based on the current state of the agent.

        Args:
            state (AgentState): The current state of the agent.

        Returns:
            dict: The next state of the agent after executing the action.
        """
        steps=state.get('steps')
        max_steps=state.get('max_steps')
        agent_data=state.get('agent_data')
        name = agent_data.action.name
        params = agent_data.action.params
        logger.info(f"[Tool]🔧: Action: {name}({', '.join(f'{k}={v}' for k, v in params.items())})")
        ai_message = AIMessage(content=Prompt.action_prompt(agent_data=agent_data))
        tool_result = self.registry.execute(tool_name=name, desktop=self.desktop, **params)

        observation=tool_result.content if tool_result.is_success else tool_result.error
        previous_observation=observation
        logger.info(f"[Tool]🔭: Observation: {shorten(observation,500,placeholder='...')}\n")
        desktop_state = self.desktop.get_state(use_vision=self.use_vision)
        prompt=Prompt.observation_prompt(query=state.get('input'),steps=steps,max_steps=max_steps, tool_result=tool_result, desktop_state=desktop_state)
        human_message=image_message(prompt=prompt,image=desktop_state.screenshot) if self.use_vision and desktop_state.screenshot else HumanMessage(content=prompt)
        return {**state,'agent_data':None,'messages':[ai_message, human_message],'previous_observation':previous_observation}

    def answer(self,state:AgentState):
        """
        Finalize the answer based on the current state of the agent.

        This method is responsible for executing the final action based on the current state of the agent.
        If the maximum number of steps has been reached, it will return a failure.
        Otherwise, it will execute the action and return the result.

        Args:
            state (AgentState): The current state of the agent.

        Returns:
            dict: The next state of the agent after finalizing the answer.
        """
        steps=state.get('steps')
        max_steps=state.get('max_steps')
        agent_data=state.get('agent_data')
        name = agent_data.action.name
        params = agent_data.action.params
        if steps<max_steps:
            tool_result = self.registry.execute(tool_name=name, desktop=None, **params)
        else:
            tool_result=ToolResult(is_success=False,content="The agent has reached the maximum number of steps.")
        ai_message = AIMessage(content=Prompt.answer_prompt(agent_data=agent_data, tool_result=tool_result))
        logger.info(f"[Agent]📜: Final Answer: {shorten(tool_result.content,500,placeholder='...')}")
        return {**state,'agent_data':None,'messages':[ai_message],'previous_observation':None,'output':tool_result.content}

    def main_controller(self,state:AgentState):
        """
        The main controller of the agent.
        
        This method is responsible for deciding which action to take next based on the current state of the agent.
        
        If the agent has encountered an error, it will return END.
        If the agent has reached the maximum number of steps, it will return 'answer'.
        If the agent is currently executing a 'Done Tool' or 'Done' action, it will return 'answer'.
        Otherwise, it will return 'action'.
        """
        if state.get("error"):
            return END
        if state.get('steps')<state.get('max_steps'):
            agent_data=state.get('agent_data')
            action_name=agent_data.action.name
            if action_name not in set(['Done Tool','Done']):
                return 'action'
        return 'answer'    

    def create_graph(self):
        '''
        Compile the state graph of the agent.

        The state graph is a directed acyclic graph (DAG) that represents the
        possible states of the agent and the actions that it can take in each
        state. The graph is compiled from the nodes and edges defined in this
        method.

        Returns:
            A compiled StateGraph object.
        '''
        graph=StateGraph(AgentState)
        graph.add_node('reason',self.reason)
        graph.add_node('action',self.action)
        graph.add_node('answer',self.answer)

        graph.add_edge(START,'reason')
        graph.add_conditional_edges('reason',self.main_controller)
        graph.add_edge('action','reason')
        graph.add_edge('answer',END)

        return graph.compile(debug=False)
    
    def log_agent_telemetry(self, response:dict):
        agent_state=cast(AgentState,response)
        actions = agent_state.get('actions', [])
        self.telemetry.capture(AgentTelemetryEvent(**{
            'task': agent_state.get('input', ''),
            'use_vision': self.use_vision,
            'max_steps': agent_state.get('steps'),
            'error': agent_state.get('error', None),
            'result': agent_state.get('output', None),
            'actions': [action.to_dict() for action in actions] if actions else None
        }))

    def invoke(self,query: str)->AgentResult:
        """
        Invoke the agent to perform a task.

        Args:
            query (str): The instruction to the agent.

        Returns:
            AgentResult: The result of the agent's action, including the output and any error that occurred.
        """
        with (self.desktop.auto_minimize() if self.auto_minimize else nullcontext()):
            desktop_state = self.desktop.get_state(use_vision=self.use_vision)
            language=self.desktop.get_default_language()
            tools_prompt = self.registry.get_tools_prompt()
            system_prompt=Prompt.system_prompt(desktop=self.desktop,browser=self.browser,language=language,instructions=self.instructions,tools_prompt=tools_prompt,max_steps=self.max_steps)
            system_message=SystemMessage(content=system_prompt)
            human_prompt=Prompt.observation_prompt(query=query,steps=1,max_steps=self.max_steps,tool_result=ToolResult(is_success=True, content="The desktop is ready to operate."), desktop_state=desktop_state)
            human_message=image_message(prompt=human_prompt,image=desktop_state.screenshot) if self.use_vision and desktop_state.screenshot else HumanMessage(content=human_prompt)
            messages=[system_message,human_message]
            state={
                'input':query,
                'steps':1,
                'max_steps':self.max_steps,
                'output':'',
                'error':'',
                'consecutive_failures':1,
                'max_consecutive_failures':self.consecutive_failures,
                'agent_data':None,
                'actions':[],
                'messages':messages,
                'previous_observation':None
            }
            try:
                with self.watch_cursor:
                    response=self.graph.invoke(state,config={'recursion_limit':self.max_steps*10})  
                self.log_agent_telemetry(response) 
                      
            except Exception as error:
                response={
                    'output':None,
                    'error':f"Error: {error}"
                }
        return AgentResult(content=response['output'], error=response['error'])

    def print_response(self,query: str):
        """
        Print the response of the agent to the given query.

        Args:
            query (str): The instruction to the agent.

        Returns:
            None
        """
        response=self.invoke(query)
        self.console.print(Markdown(response.content or response.error))
