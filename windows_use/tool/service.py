from pydantic import BaseModel, ValidationError
from typing import Any
import json

class Tool:
    def __init__(self, name: str|None=None, description: str|None=None, model:BaseModel|None=None):
        self.name = name
        self.description = description
        self.model=model
        self.function = None
        
    @property
    def json_schema(self)->dict:
        schema=self.model.model_json_schema(mode="serialization")
        properties=schema.get("properties",{})
        required=schema.get("required",[])
        return {
                "name":self.name,
                "description":self.description,
                "parameters":{
                    "type":"object",
                    "properties":properties,
                    "required":required
                }
            } 

    def validate(self,args:dict):
        errors:list[str]=[]
        try:
            self.model(**args)
        except ValidationError as e:
            for error in e.errors():
                field="".join([str(loc) for loc in error['loc']])
                msg=error['msg']
                errors.append(f"{field}:{msg}")
        return errors

    def __call__(self, function):
        if self.name is None:
            self.name = function.__name__
        if self.description is None:
            self.description = function.__doc__
        self.function = function
        return self
    
    def invoke(self, *args, **kwargs):
        return self.function(*args, **kwargs)