from pydantic import BaseModel
from typing import Any, Union

class Tool:
    def __init__(self, name: str|None=None, description: str|None=None, args_schema:BaseModel|None=None):
        self.name = name
        self.description = description
        self.model=args_schema
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
        result = self.function(*args, **kwargs)
        # Normalize and validate result to ToolResult when possible
        if isinstance(result, dict):
            try:
                return ToolResult.parse_obj(result)
            except Exception:
                return ToolResult(status="error", evidence={"raw": result}, confidence=0.0, details="invalid tool result schema")
        if isinstance(result, ToolResult):
            return result
        # Wrap arbitrary return values
        return ToolResult(status="ok", evidence={"result": result}, confidence=1.0)


class ToolResult(BaseModel):
    status: str
    evidence: dict | None = None
    confidence: float = 1.0
    details: Union[str, dict, None] = None