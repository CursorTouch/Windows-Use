from typing import Protocol, runtime_checkable, overload, Optional, Union
from windows_use.llms.views import ChatLLMResponse
from windows_use.messages import BaseMessage
from pydantic import BaseModel

@runtime_checkable
class BaseChatLLM(Protocol):
    """Protocol for chat-based language model implementations."""

    @property
    def model_name(self) -> str:
        """Return the name of the model being used."""
        ...

    @property
    def provider(self) -> str:
        """Return the name of the LLM provider (e.g., 'openai', 'google', 'anthropic')."""
        ...

    @overload
    def invoke(
        self, 
        messages: list[BaseMessage], 
        structured_output: Optional[BaseModel] = None
    ) -> ChatLLMResponse:
        """Invoke the LLM with a list of messages and optional structured output schema."""
        ...



    