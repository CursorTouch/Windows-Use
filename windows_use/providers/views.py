from pydantic import BaseModel


class TokenUsage(BaseModel):
    """Token usage information from LLM responses."""

    prompt_tokens: int=0
    completion_tokens: int=0
    total_tokens: int=0
    image_tokens: int=0
    thinking_tokens: int=0
    cache_creation_input_tokens: int=0
    cache_read_input_tokens: int=0


class Metadata(BaseModel):
    name: str
    context_window: int
    owned_by: str
