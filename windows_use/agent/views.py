from pydantic import BaseModel,Field
    
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
