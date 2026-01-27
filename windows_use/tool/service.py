from pydantic import BaseModel, ValidationError
from typing import Any
import logging
import json

EXCLUDED_PROPERTIES=["title"]

logger = logging.getLogger(__name__)

class Tool:
    def __init__(self, name: str|None=None, description: str|None=None, model:BaseModel|None=None):
        self.name = name
        self.description = description
        self.model=model
        self.function = None
        
    @property
    def json_schema(self) -> dict:
        schema = self.model.model_json_schema(mode="serialization")
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        def exclude_properties(obj):
            if isinstance(obj, dict):
                return {
                    k: exclude_properties(v) 
                    for k, v in obj.items() 
                    if k not in EXCLUDED_PROPERTIES
                }
            elif isinstance(obj, list):
                return [exclude_properties(item) for item in obj]
            return obj

        parameters = {
            "type": "object",
            "properties": exclude_properties(properties),
            "required": required
        }
        
        return {
            "name": self.name,
            "description": self.description,
            "parameters": parameters
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
            logger.warning(f"Validation errors for tool {self.name}: {errors}")
        return errors

    def __call__(self, function):
        if self.name is None:
            self.name = function.__name__
        if self.description is None:
            self.description = function.__doc__
        self.function = function
        return self
    
    def invoke(self, *args, **kwargs):
        try:
            return self.function(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error invoking tool {self.name}: {e}")
            return str(e)