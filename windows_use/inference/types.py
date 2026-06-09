from __future__ import annotations
from dataclasses import dataclass, field
from datetime import timedelta
from enum import Enum
from typing import Any, Callable, Optional, TYPE_CHECKING
import asyncio
import time
from copy import deepcopy

from pydantic import BaseModel

if TYPE_CHECKING:
    from windows_use.message.types import LLMMessage, TextContent, ThinkingContent, ToolCallContent, ImageContent
    from windows_use.tool.types import Tool


# ── Shared enums ──────────────────────────────────────────────────────────────

class Transport(str, Enum):
    """Wire transport protocol used to reach the provider endpoint."""

    Auto = "auto"
    HTTP = "http"
    WEBSOCKET = "websocket"
    SSE = "sse"


class AuthType(str, Enum):
    """Authentication mechanism used by a provider."""

    ApiKey = "api_key"
    OAuth = "oauth"


class StopReason(str, Enum):
    """Normalised reason a model generation stopped."""

    Stop = "stop"
    Length = "length"
    ToolCalls = "tool_calls"
    ContentFilter = "content_filter"
    Abort = "abort"
    Error = "error"


class ThinkingLevel(str, Enum):
    """Ordered thinking/reasoning intensity levels mapped to provider budgets."""

    Off = "off"
    Minimal = "minimal"
    Low = "low"
    Medium = "medium"
    High = "high"
    XHigh = "xhigh"
    Max = "max"


@dataclass
class ThinkingBudgets:
    """Token budgets for providers that map ThinkingLevel to budget_tokens."""
    minimal: Optional[int] = 1024
    low: Optional[int] = 2048
    medium: Optional[int] = 4096
    high: Optional[int] = 8192
    xhigh: Optional[int] = 16384
    max: Optional[int] = 32768

    def get(self, level: ThinkingLevel) -> int:
        """Return the budget_tokens value for the given ThinkingLevel, falling back to built-in defaults."""
        _defaults = {
            "minimal": 1024, "low": 2048, "medium": 4096,
            "high": 8192, "xhigh": 16384, "max": 32768,
        }
        value = getattr(self, level.value, None)
        return value if value is not None else _defaults[level.value]


# ── LLM types ─────────────────────────────────────────────────────────────────

class LLMEventType(str, Enum):
    """Discriminant tag carried by every LLMEvent dataclass."""

    Start = "start"
    Error = "error"
    End = "end"
    TextStart = "text_start"
    TextDelta = "text_delta"
    TextEnd = "text_end"
    ThinkingStart = "thinking_start"
    ThinkingDelta = "thinking_delta"
    ThinkingEnd = "thinking_end"
    ToolCallStart = "tool_call_start"
    ToolCallDelta = "tool_call_delta"
    ToolCallEnd = "tool_call_end"


AbortSignal = asyncio.Event
PayloadCallback = Callable[[dict[str, Any]], Optional[dict[str, Any]]]
ResponseCallback = Callable[[Any], None]


@dataclass
class LLMOptions:
    """Runtime configuration passed to every BaseLLMAPI constructor and stream() call."""

    api_key: Optional[str] = None
    base_url: Optional[str] = None
    headers: Optional[dict[str, str]] = None
    max_retries: int = 3
    timeout: timedelta = field(default_factory=lambda: timedelta(seconds=60))
    temperature: float = 1.0
    max_tokens: Optional[int] = None
    transport: Transport = Transport.HTTP
    thinking_level: Optional[ThinkingLevel] = None
    thinking_budgets: Optional[ThinkingBudgets] = None
    signal: Optional[AbortSignal] = None
    on_payload: Optional[PayloadCallback] = None
    on_response: Optional[ResponseCallback] = None


@dataclass
class StructuredResponseFormat:
    """Normalised structured output spec (JSON schema + name + strict flag)."""

    schema: dict[str, Any]
    name: str = "response"
    strict: bool = True


StructuredResponseInput = StructuredResponseFormat | type[Any] | dict[str, Any]


def normalize_structured_response_format(response_format: StructuredResponseInput | None) -> StructuredResponseFormat | None:
    """Coerce any supported response_format shape into a StructuredResponseFormat, or None."""
    if response_format is None:
        return None

    if isinstance(response_format, StructuredResponseFormat):
        return response_format

    if isinstance(response_format, type) and issubclass(response_format, BaseModel):
        return StructuredResponseFormat(
            name=response_format.__name__,
            schema=response_format.model_json_schema(),
        )

    if isinstance(response_format, dict):
        schema = deepcopy(response_format)
        if isinstance(schema.get("format"), dict):
            schema = deepcopy(schema["format"])
        if isinstance(schema.get("json_schema"), dict):
            schema = deepcopy(schema["json_schema"])
        name = str(schema.get("name") or schema.get("title") or "response")
        strict = bool(schema.pop("strict", True))
        if "schema" in schema and isinstance(schema["schema"], dict):
            name = str(schema.pop("name", name))
            schema = deepcopy(schema["schema"])
        return StructuredResponseFormat(name=name, schema=schema, strict=strict)

    raise TypeError("response_format must be a Pydantic model class, JSON schema dict, or StructuredResponseFormat")


@dataclass
class LLMContext:
    """All inputs required to execute one LLM turn: messages, tools, and optional overrides."""

    messages: list["LLMMessage"]
    tools: list["Tool"] = field(default_factory=list)
    system_prompt: Optional[str] = None
    response_format: Optional[StructuredResponseInput] = None
    num_ephemeral: int = 0  # how many tail messages are ephemeral (screenshots etc.) — skip when placing cache markers


def _default_text_event_data():
    """Return an empty TextContent; used as a field default_factory to avoid mutable defaults."""
    from windows_use.message.types import TextContent
    return TextContent(content="")


@dataclass
class TextEventData:
    """Mixin carrying a TextContent payload for text-phase events."""

    text: "TextContent" = field(default_factory=_default_text_event_data)


@dataclass
class ThinkingEventData:
    """Mixin carrying an optional ThinkingContent payload for thinking-phase events."""

    thinking: Optional["ThinkingContent"] = None


@dataclass
class ToolCallEventData:
    """Mixin carrying an optional ToolCallContent payload for tool-call-phase events."""

    tool_call: Optional["ToolCallContent"] = None


@dataclass
class StartEvent:
    """Emitted once at the very beginning of a stream before any content."""

    type: LLMEventType = field(default=LLMEventType.Start, init=False)


@dataclass
class ErrorEvent:
    """Emitted when the stream terminates due to an error or cancellation."""

    type: LLMEventType = field(default=LLMEventType.Error, init=False)
    reason: StopReason = StopReason.Stop
    error: str = ""


@dataclass
class EndEvent:
    """Emitted once at the end of a stream carrying token usage and the stop reason."""

    type: LLMEventType = field(default=LLMEventType.End, init=False)
    reason: StopReason = StopReason.Stop
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0


@dataclass
class TextStartEvent:
    """Signals the opening of a new text content block."""

    type: LLMEventType = field(default=LLMEventType.TextStart, init=False)
    text: "TextContent"


@dataclass
class TextDeltaEvent:
    """Carries an incremental text chunk within the active text block."""

    type: LLMEventType = field(default=LLMEventType.TextDelta, init=False)
    text: "TextContent"


@dataclass
class TextEndEvent:
    """Signals the close of a text block, carrying the fully accumulated text."""

    type: LLMEventType = field(default=LLMEventType.TextEnd, init=False)
    text: "TextContent"


@dataclass
class ThinkingStartEvent:
    """Signals the opening of a thinking/reasoning content block."""

    type: LLMEventType = field(default=LLMEventType.ThinkingStart, init=False)
    thinking: Optional["ThinkingContent"] = None


@dataclass
class ThinkingDeltaEvent:
    """Carries an incremental chunk of thinking/reasoning text."""

    type: LLMEventType = field(default=LLMEventType.ThinkingDelta, init=False)
    thinking: "ThinkingContent"


@dataclass
class ThinkingEndEvent:
    """Signals the close of a thinking block, carrying the fully accumulated text."""

    type: LLMEventType = field(default=LLMEventType.ThinkingEnd, init=False)
    thinking: "ThinkingContent"


@dataclass
class ToolCallStartEvent:
    """Signals that the model has started emitting a tool call (id and name known)."""

    type: LLMEventType = field(default=LLMEventType.ToolCallStart, init=False)
    tool_call: "ToolCallContent"


@dataclass
class ToolCallDeltaEvent:
    """Carries a partial JSON arguments chunk for an in-progress tool call."""

    type: LLMEventType = field(default=LLMEventType.ToolCallDelta, init=False)
    tool_call: "ToolCallContent"


@dataclass
class ToolCallEndEvent:
    """Signals the completion of a tool call with the final parsed arguments."""

    type: LLMEventType = field(default=LLMEventType.ToolCallEnd, init=False)
    tool_call: "ToolCallContent"


LLMEvent = (
    StartEvent
    | ErrorEvent
    | EndEvent
    | TextStartEvent
    | TextDeltaEvent
    | TextEndEvent
    | ThinkingStartEvent
    | ThinkingDeltaEvent
    | ThinkingEndEvent
    | ToolCallStartEvent
    | ToolCallDeltaEvent
    | ToolCallEndEvent
)


# ── Image types ───────────────────────────────────────────────────────────────

class ImageStopReason(str, Enum):
    """Normalised reason an image generation run stopped."""

    Stop = "stop"
    Error = "error"
    Abort = "abort"


@dataclass
class ImageOptions:
    """Runtime configuration for image generation API calls."""

    api_key: Optional[str] = None
    base_url: Optional[str] = None
    headers: Optional[dict[str, str]] = None
    timeout: timedelta = field(default_factory=lambda: timedelta(seconds=120))
    max_retries: int = 3
    on_payload: Optional[PayloadCallback] = None
    on_response: Optional[ResponseCallback] = None


@dataclass
class ImageContext:
    """Inputs for a single image generation request."""

    contents: list["TextContent | ImageContent"]
    size: Optional[str] = None
    quality: Optional[str] = None
    n: int = 1


@dataclass
class GeneratedImage:
    """Result of a completed image generation call."""

    model_id: str
    provider: str
    output: list["TextContent | ImageContent"]
    stop_reason: ImageStopReason
    usage: Any = field(default_factory=lambda: __import__("operator_use.message.types", fromlist=["Usage"]).Usage())
    error: str = ""
    timestamp: float = field(default_factory=time.time)


# ── Video types ───────────────────────────────────────────────────────────────

class VideoFormat(str, Enum):
    """Container format for generated video output."""

    MP4  = "mp4"
    WEBM = "webm"
    MOV  = "mov"
    GIF  = "gif"


class VideoStopReason(str, Enum):
    """Normalised reason a video generation job stopped."""

    Stop    = "stop"
    Error   = "error"
    Abort   = "abort"
    Timeout = "timeout"


@dataclass
class VideoOptions:
    """Runtime configuration for video generation API calls."""

    api_key: Optional[str] = None
    base_url: Optional[str] = None
    headers: Optional[dict[str, str]] = None
    timeout: timedelta = field(default_factory=lambda: timedelta(seconds=600))
    poll_interval: float = 3.0
    max_retries: int = 3
    on_payload: Optional[PayloadCallback] = None
    on_response: Optional[ResponseCallback] = None


@dataclass
class VideoContext:
    """Inputs for a single video generation request."""

    prompt: str
    image: Optional[bytes] = None
    duration: Optional[float] = None
    aspect_ratio: Optional[str] = None
    resolution: Optional[str] = None


@dataclass
class GeneratedVideo:
    """Result of a completed video generation job."""

    model_id: str
    provider: str
    url: Optional[str] = None
    video: Optional[bytes] = None
    format: VideoFormat = VideoFormat.MP4
    duration: Optional[float] = None
    stop_reason: VideoStopReason = VideoStopReason.Stop
    usage: Any = None
    error: str = ""
    timestamp: float = field(default_factory=time.time)


# ── Audio types ───────────────────────────────────────────────────────────────

class AudioFormat(str, Enum):
    """Audio codec/container format for TTS output or STT input."""

    MP3 = "mp3"
    WAV = "wav"
    OPUS = "opus"
    AAC = "aac"
    FLAC = "flac"
    PCM = "pcm"


class AudioStopReason(str, Enum):
    """Normalised reason an audio synthesis or transcription call stopped."""

    Stop = "stop"
    Error = "error"
    Abort = "abort"


class TimestampGranularity(str, Enum):
    """Level of timestamp detail requested in a transcription response."""

    Word = "word"
    Segment = "segment"


@dataclass
class AudioOptions:
    """Runtime configuration for TTS and STT API calls."""

    api_key: Optional[str] = None
    base_url: Optional[str] = None
    headers: Optional[dict[str, str]] = None
    timeout: timedelta = field(default_factory=lambda: timedelta(seconds=120))
    max_retries: int = 3
    on_payload: Optional[PayloadCallback] = None
    on_response: Optional[ResponseCallback] = None


@dataclass
class TTSContext:
    """Inputs for a single text-to-speech synthesis request."""

    input: str
    voice: str
    speed: float = 1.0
    response_format: AudioFormat = AudioFormat.MP3
    language: Optional[str] = None
    instructions: Optional[str] = None


@dataclass
class WordTimestamp:
    """Timing information for a single word in a transcription."""

    word: str
    start: float
    end: float


@dataclass
class SegmentTimestamp:
    """Timing information for a sentence-level segment in a transcription."""

    id: int
    text: str
    start: float
    end: float


@dataclass
class STTContext:
    """Inputs for a single speech-to-text transcription request."""

    audio: bytes
    format: AudioFormat = AudioFormat.MP3
    language: Optional[str] = None
    temperature: float = 0.0
    timestamp_granularities: list[TimestampGranularity] = field(default_factory=list)
    prompt: Optional[str] = None


@dataclass
class SynthesizedAudio:
    """Result of a completed TTS synthesis call."""

    model_id: str
    provider: str
    audio: bytes
    format: AudioFormat
    stop_reason: AudioStopReason
    usage: Any = None
    error: str = ""
    timestamp: float = field(default_factory=time.time)


@dataclass
class TranscribedAudio:
    """Result of a completed STT transcription call."""

    model_id: str
    provider: str
    text: str
    language: Optional[str] = None
    duration: Optional[float] = None
    words: list[WordTimestamp] = field(default_factory=list)
    segments: list[SegmentTimestamp] = field(default_factory=list)
    stop_reason: AudioStopReason = AudioStopReason.Stop
    usage: Any = None
    error: str = ""
    timestamp: float = field(default_factory=time.time)
