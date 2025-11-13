from pydantic import BaseModel,Field

class AgentStep(BaseModel):
    steps:int=0
    max_steps:int

    def step_increment(self):
        self.steps+=1

    def reset(self):
        self.steps=0
    
class AgentResult(BaseModel):
    is_done:bool
    content:str|None=None
    error:str|None=None

class Action(BaseModel):
    name:str
    params: dict=Field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'params': self.params
        }

class AgentData(BaseModel):
    evaluate: str|None=None
    thought: str|None=None
    action: Action|None=None
    observation: str|None=None
