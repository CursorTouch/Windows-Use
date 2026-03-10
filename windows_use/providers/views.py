from pydantic import BaseModel


class TokenUsage(BaseModel):
    """Token usage information from LLM responses."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    image_tokens: int | None = None
    thinking_tokens: int | None = None
    cache_creation_input_tokens: int | None = None
    cache_read_input_tokens: int | None = None


class Metadata(BaseModel):
    name: str
    context_window: int
    owned_by: str
