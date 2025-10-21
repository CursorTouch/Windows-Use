from typing import Protocol,runtime_checkable,overload
from windows_use.llms.views import ChatLLMResponse
from windows_use.messages import BaseMessage
from pydantic import BaseModel

@runtime_checkable
class BaseChatLLM(Protocol):

    @property
    def model_name(self) -> str:
        ...

    @property
    def provider(self) -> str:
        ...

    @overload
    def invoke(self, messages: list[BaseMessage],structured_output:BaseModel|None=None) -> ChatLLMResponse:
        ...



    