from pydantic import BaseModel
from typing import Any

class Tool:
    def __init__(self, name: str|None=None, description: str|None=None, args_schema:BaseModel|None=None):
        self.name = name
        self.description = description
        self.args_schema = self.preprocess_schema(args_schema)
        self.function = None

    def preprocess_schema(self, args_schema:BaseModel):
        schema=args_schema.model_json_schema()
        properties={k:{term:content for term,content in v.items() if term not in ['title']} for k,v in schema.get('properties').items() if k not in ['title']}
        required=[name for name, field in args_schema.model_fields.items() if field.is_required()]
        return {
            'type': 'object',
            'properties': properties,
            'required': required
        }

    def __call__(self, function):
        if self.name is None:
            self.name = function.__name__
        if self.description is None:
            self.description = function.__doc__
        self.function = function
        return self
    
    def invoke(self, *args, **kwargs):
        return self.function(*args, **kwargs)