from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Any, Optional, cast
from enum import Enum
from PIL import Image
from windows_use.inference.types import StopReason
from windows_use.message.utils import image_to_base64, audio_to_base64


@dataclass
class TextContent:
    """Plain text content (system/user/assistant messages)."""
    type: Literal["text"] = "text"
    content: str = ""


@dataclass
class ImageContent:
    """Image content (PIL images, bytes, URLs, or base64 strings)."""
    type: Literal["image"] = "image"
    images: list[str | Image.Image | bytes] = field(default_factory=list)

    def to_base64(self) -> list[tuple[str, str]]:
        """Convert all images to (base64_data, mime_type) pairs.

        Returns:
            List of (base64_string, mime_type) tuples.
        """
        return [image_to_base64(img) for img in self.images]

    @classmethod
    def from_file(cls, path: str | Path) -> ImageContent:
        """Load image from a file path.

        Args:
            path: Path to the image file.

        Returns:
            An ImageContent instance with the loaded image bytes.
        """
        return cls(images=[Path(path).read_bytes()])

    @classmethod
    def from_url(cls, url: str) -> ImageContent:
        """Create ImageContent from a URL.

        Args:
            url: The image URL.

        Returns:
            An ImageContent instance with the URL.
        """
        return cls(images=[url])


@dataclass
class AudioContent:
    """Audio content (bytes, base64 strings, or 'file:' paths)."""
    type: Literal["audio"] = "audio"
    # Each item is raw bytes, a base64 string, or a file path string prefixed with "file:"
    audio: list[bytes | str] = field(default_factory=list)

    def to_base64(self) -> list[tuple[str, str]]:
        """Convert all audio to (base64_data, mime_type) pairs.

        Returns:
            List of (base64_string, mime_type) tuples.
        """
        return [audio_to_base64(item) for item in self.audio]

    @classmethod
    def from_file(cls, path: str | Path) -> AudioContent:
        """Load audio from a file path.

        Args:
            path: Path to the audio file.

        Returns:
            An AudioContent instance with the loaded audio bytes.
        """
        return cls(audio=[Path(path).read_bytes()])

    @classmethod
    def from_base64(cls, data: str, mime_type: str | None = None) -> AudioContent:
        """Create AudioContent from a base64-encoded string.

        Args:
            data: Base64-encoded audio data.
            mime_type: Optional MIME type hint (not currently used).

        Returns:
            An AudioContent instance with the base64 data.
        """
        return cls(audio=[data])


@dataclass
class ThinkingContent:
    """Extended thinking content from Claude models with thinking enabled."""
    type: Literal["thinking"] = "thinking"
    content: str = ""
    signature: str = ""


@dataclass
class ToolCallContent:
    """Tool invocation from assistant with args, semantic kind, and call id."""
    type: Literal["tool_call"] = "tool_call"
    id: str = ""
    name: str = ""
    args: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResultContent:
    """Tool execution result paired with ToolCallContent by id."""
    type: Literal["tool_result"] = "tool_result"
    id: str = ""
    content: str = ""
    is_error: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
    terminate: bool = False
    terminate_message: str | None = None


Content = TextContent | ImageContent | AudioContent | ThinkingContent | ToolCallContent | ToolResultContent

# Per-role content constraints (for type hints and documentation).
SystemContent = TextContent
UserContent = TextContent | ImageContent | AudioContent | ToolResultContent
AssistantContent = TextContent | ThinkingContent | ToolCallContent
ToolContent = ToolResultContent


@dataclass
class UsageCost:
    """Monetized costs in USD for input, output, cache operations, and total."""
    input: float = 0.0
    output: float = 0.0
    cache_read: float = 0.0
    cache_write: float = 0.0
    total: float = 0.0


@dataclass
class Usage:
    """Token counts and costs for a single LLM completion."""
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    cost: UsageCost = field(default_factory=UsageCost)


class Role(str, Enum):
    """Message roles in the conversation history."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    COMPACTION = "compaction"


@dataclass
class BaseMessage:
    """Common fields for all message types (contents, id, timestamp)."""
    contents: list[Content] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)


@dataclass
class SystemMessage(BaseMessage):
    """System context and instructions for the LLM."""
    role: Literal[Role.SYSTEM] = field(default=Role.SYSTEM, init=False)

    @classmethod
    def text(cls, content: str) -> SystemMessage:
        """Construct SystemMessage from plain text.

        Args:
            content: The system message text.

        Returns:
            A SystemMessage with the text content.
        """
        return cls(contents=[TextContent(content=content)])


@dataclass
class UserMessage(BaseMessage):
    """User input containing text, images, audio, and/or tool results."""
    role: Literal[Role.USER] = field(default=Role.USER, init=False)

    @classmethod
    def text(cls, content: str) -> UserMessage:
        """Construct UserMessage from plain text.

        Args:
            content: The user message text.

        Returns:
            A UserMessage with the text content.
        """
        return cls(contents=[TextContent(content=content)])

    @classmethod
    def with_images(cls, content: str, images: list[str | Image.Image | bytes]) -> UserMessage:
        """Construct UserMessage with text and images.

        Args:
            content: The user message text.
            images: List of PIL Images, image bytes, or image URLs.

        Returns:
            A UserMessage with text and image content.
        """
        return cls(contents=[TextContent(content=content), ImageContent(images=images)])

    @classmethod
    def with_audio(cls, content: str, audio: list[bytes | str]) -> UserMessage:
        """Construct UserMessage with text and audio.

        Args:
            content: The user message text.
            audio: List of audio bytes, base64 strings, or 'file:' paths.

        Returns:
            A UserMessage with text and audio content.
        """
        return cls(contents=[TextContent(content=content), AudioContent(audio=audio)])


@dataclass
class AssistantMessage(BaseMessage):
    """LLM response with text, thinking, tool calls, usage, and stop reason."""
    role: Literal[Role.ASSISTANT] = field(default=Role.ASSISTANT, init=False)
    usage: Usage = field(default_factory=Usage)
    stop_reason: StopReason = StopReason.Stop
    error: str = ""

    @classmethod
    def text(cls, content: str) -> 'AssistantMessage':
        """Create an AssistantMessage with a single TextContent block."""
        return cls(contents=[TextContent(content=content)])

    def text_content(self) -> str:
        """Concatenate all TextContent items.

        Returns:
            The concatenated text from all text content blocks.
        """
        return "".join(c.content for c in self.contents if isinstance(c, TextContent))

    def tool_calls(self) -> list[ToolCallContent]:
        """Extract all ToolCallContent items.

        Returns:
            List of all tool calls in this message.
        """
        return [c for c in self.contents if isinstance(c, ToolCallContent)]

    def thinking(self) -> list[ThinkingContent]:
        """Extract all ThinkingContent items.

        Returns:
            List of all extended thinking blocks in this message.
        """
        return [c for c in self.contents if isinstance(c, ThinkingContent)]


@dataclass
class ToolMessage(BaseMessage):
    """Tool execution results responding to ToolCallContent."""
    role: Literal[Role.TOOL] = field(default=Role.TOOL, init=False)

    @classmethod
    def from_results(cls, results: list[ToolResultContent]) -> ToolMessage:
        """Construct ToolMessage from multiple tool results.

        Args:
            results: List of tool execution results.

        Returns:
            A ToolMessage containing all the tool results.
        """
        return cls(contents=list(results))  # type: ignore[arg-type]

    @classmethod
    def from_result(cls, result: ToolResultContent) -> ToolMessage:
        """Construct ToolMessage from a single tool result.

        Args:
            result: A single tool execution result.

        Returns:
            A ToolMessage containing the tool result.
        """
        return cls(contents=[result])  # type: ignore[arg-type]


LLMMessage = SystemMessage | UserMessage | AssistantMessage | ToolMessage

@dataclass
class CompactionMessage:
    """Context compaction summary recorded when history is summarized."""
    role: Literal[Role.COMPACTION] = field(default=Role.COMPACTION, init=False)
    summary: str
    tokens_before: int
    timestamp: float


AgentMessage = LLMMessage | CompactionMessage