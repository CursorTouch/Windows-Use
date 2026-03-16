from pydantic import BaseModel, ValidationError
from dataclasses import dataclass,field
from typing import Any
from abc import ABC
import asyncio
import logging

EXCLUDED_PROPERTIES = ["title"]

MAX_TOOL_OUTPUT_LENGTH = 10000

logger = logging.getLogger(__name__)

@dataclass
class ToolResult:
    success: bool=False
    output:str|None=None
    error:str|None=None
    metadata:dict[str,Any]=field(default_factory=dict)

    @classmethod
    def success_result(cls,output:str,metadata:dict[str,Any]=None) -> "ToolResult":
        return cls(success=True,output=output,metadata=metadata)
    
    @classmethod
    def error_result(cls,error:str,metadata:dict[str,Any]=None) -> "ToolResult":
        return cls(success=False,error=error,metadata=metadata)

class Tool(ABC):
    def __init__(self, name: str|None=None, description: str|None=None, model: BaseModel|None=None):
        self.name = name
        self.description = description
        self.model = model
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
            "required": required,
        }

        return {
            "name": self.name,
            "description": self.description,
            "parameters": parameters,
        }

    def validate_params(self, args: dict[str,Any])->list[str]:
        try:
            self.model(**args)
            return []
        except ValidationError as e:
            errors=[]
            for error in e.errors():
                field = "".join([str(loc) for loc in error["loc"]])
                msg = error["msg"]
                errors.append(f"{field}:{msg}")
            return errors
        except Exception as e:
            return [str(e)]

    def __call__(self, function):
        if self.name is None:
            self.name = function.__name__
        if self.description is None:
            self.description = function.__doc__
        self.function = function
        return self

    def invoke(self, *args, **kwargs):
        """Synchronous invocation. Use ainvoke for async tools."""
        try:
            result = self.function(*args, **kwargs)
            if asyncio.iscoroutine(result):
                return asyncio.run(result)
            return result
        except Exception as e:
            logger.error(f"Error invoking tool {self.name}: {e}")
            raise

    async def ainvoke(self, *args, **kwargs):
        """Asynchronous invocation. Awaits if the tool function is a coroutine."""
        try:
            if asyncio.iscoroutinefunction(self.function):
                return await self.function(*args, **kwargs)
            return self.function(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error invoking tool {self.name}: {e}")
            raise
