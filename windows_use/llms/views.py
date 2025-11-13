from pydantic import BaseModel

class ChatLLMUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    image_tokens: int|None = None

class ChatLLMResponse(BaseModel):
    content: str|BaseModel| None=None
    thinking: str|None = None
    usage: ChatLLMUsage|None = None