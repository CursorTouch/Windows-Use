from typing import Protocol,runtime_checkable,overload
from windows_use.llms.views import ChatLLMResponse, ModelMetadata
from windows_use.messages import BaseMessage
from pydantic import BaseModel
from windows_use.tool import Tool

@runtime_checkable
class BaseChatLLM(Protocol):

    @property
    def model_name(self) -> str:
        ...

    @property
    def provider(self) -> str:
        ...

    @overload
    def invoke(self, messages: list[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel|None=None, json_mode:bool=False) -> ChatLLMResponse:
        ...

    @overload
    async def ainvoke(self, messages: list[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel|None=None, json_mode:bool=False) -> ChatLLMResponse:
        ...

    @overload
    def stream(self, messages: list[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel|None=None, json_mode:bool=False) -> ChatLLMResponse:
        ...

    @overload
    async def astream(self, messages: list[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel|None=None, json_mode:bool=False) -> ChatLLMResponse:
        ...

    @overload
    def get_model_specification(self) -> ModelMetadata:
        ...

    