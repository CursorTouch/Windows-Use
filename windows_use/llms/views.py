from windows_use.messages import AIMessage,ToolMessage
from pydantic import BaseModel

class ChatLLMUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    image_tokens: int|None = None

class ChatLLMResponse(BaseModel):
    content: AIMessage|ToolMessage|BaseModel
    thinking: str|None = None
    usage: ChatLLMUsage|None = None

class ModelMetadata(BaseModel):
    name: str
    context_window: int
    owned_by: str