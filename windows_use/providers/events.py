from enum import Enum
from pydantic import BaseModel
from typing import Optional, Any

from windows_use.providers.views import TokenUsage

class LLMStreamEventType(str, Enum):
    TEXT_START = "text_start"
    TEXT_DELTA = "text_delta"
    TEXT_END = "text_end"
    TOOL_CALL = "tool_call"
    THINK_START = "think_start"
    THINK_DELTA = "think_delta"
    THINK_END = "think_end"

class LLMEventType(str, Enum):
    TEXT = "text"
    TOOL_CALL = "tool_call"

class Thinking(BaseModel):
    """Thinking/reasoning content with optional cryptographic signature (Anthropic)."""

    content: str | None = None
    signature: str | bytes | None = None

class ToolCall(BaseModel):
    id: str
    name: str
    params: dict

class LLMStreamEvent(BaseModel):
    type: LLMStreamEventType
    thinking: Thinking | None = None
    content: str | None = None
    tool_call: ToolCall | None = None
    usage: TokenUsage | None = None


class LLMEvent(BaseModel):
    type: LLMEventType
    thinking: Thinking | None = None
    content: str | None = None
    tool_call: ToolCall | None = None
    usage: TokenUsage | None = None
