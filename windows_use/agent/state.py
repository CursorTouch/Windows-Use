from windows_use.messages import BaseMessage
from windows_use.agent.views import AgentData, Action
from typing import TypedDict,Annotated
from operator import add

class AgentState(TypedDict):
    steps:int
    max_steps: int
    input:str
    output:str
    error:str
    max_consecutive_failures: int
    messages:Annotated[list[BaseMessage],add]
    previous_observation: str|None
    agent_data:AgentData|None