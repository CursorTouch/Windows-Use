from __future__ import annotations

import base64
import io
from pathlib import Path

from PIL import Image


_PIL_MIME: dict[str, str] = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
    "GIF": "image/gif",
    "WEBP": "image/webp",
}

_AUDIO_MIME: dict[bytes, str] = {
    b"ID3": "audio/mpeg",
    b"\xff\xfb": "audio/mpeg",
    b"\xff\xf3": "audio/mpeg",
    b"\xff\xf2": "audio/mpeg",
    b"OggS": "audio/ogg",
    b"fLaC": "audio/flac",
    b"RIFF": "audio/wav",
}


def detect_image_mime(data: bytes) -> str:
    """Detect image MIME type from magic bytes; default to PNG if unknown.

    Args:
        data: Binary image data to detect.

    Returns:
        The MIME type string (e.g., 'image/jpeg', 'image/png').
    """
    if data[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if data[:4] == b"RIFF" and len(data) >= 12 and data[8:12] == b"WEBP":
        return "image/webp"
    return "image/png"


def detect_audio_mime(data: bytes) -> str:
    """Detect audio MIME type from magic bytes; default to MP3 if unknown.

    Args:
        data: Binary audio data to detect.

    Returns:
        The MIME type string (e.g., 'audio/mpeg', 'audio/wav', 'audio/ogg').
    """
    for magic, mime in _AUDIO_MIME.items():
        if data[:len(magic)] == magic:
            # WAV files use RIFF container with WAVE format code
            if magic == b"RIFF" and len(data) >= 12 and data[8:12] == b"WAVE":
                return "audio/wav"
            elif magic != b"RIFF":
                return mime
    return "audio/mpeg"


def image_to_base64(img: str | Image.Image | bytes) -> tuple[str, str]:
    """Convert image to (base64_data, mime_type); URL strings passed through with empty mime.

    Args:
        img: A PIL Image, base64 string, raw bytes, or URL.

    Returns:
        A tuple of (base64_string, mime_type_string).
    """
    if isinstance(img, str):
        # URLs are passed through as-is
        if img.startswith("http"):
            return img, ""
        # Detect MIME type from base64 string magic bytes
        try:
            mime = detect_image_mime(base64.b64decode(img[:16] + "=="))
        except Exception:
            mime = "image/png"
        return img, mime
    if isinstance(img, Image.Image):
        # Serialize PIL Image with format detection
        fmt = (img.format or "PNG").upper()
        buf = io.BytesIO()
        img.save(buf, format=fmt)
        mime = _PIL_MIME.get(fmt, "image/png")
        return base64.b64encode(buf.getvalue()).decode(), mime
    # Raw bytes: detect MIME from magic bytes
    mime = detect_image_mime(img)
    return base64.b64encode(img).decode(), mime


def audio_to_base64(item: bytes | str) -> tuple[str, str]:
    """Convert audio to (base64_data, mime_type); accepts bytes, base64, or 'file:' paths.

    Args:
        item: Raw audio bytes, base64-encoded string, or 'file:/path/to/audio'.

    Returns:
        A tuple of (base64_string, mime_type_string).
    """
    if isinstance(item, bytes):
        # Raw bytes: detect MIME from magic bytes
        mime = detect_audio_mime(item)
        return base64.b64encode(item).decode(), mime
    if item.startswith("file:"):
        # Load file from disk and encode
        data = Path(item[5:]).read_bytes()
        mime = detect_audio_mime(data)
        return base64.b64encode(data).decode(), mime
    # Assume base64 string; detect MIME from magic bytes
    try:
        mime = detect_audio_mime(base64.b64decode(item[:16] + "=="))
    except Exception:
        mime = "audio/mpeg"
    return item, mime


def filter_empty_assistant_messages(messages: list) -> list:
    """Remove assistant messages with no usable content (prevents provider 400 errors).

    Empty assistant messages (e.g. from persisted API errors) produce invalid {"role": "assistant"}
    with no content or tool_calls, causing all providers to reject the request.

    Args:
        messages: List of LLM messages.

    Returns:
        Filtered list with empty assistant messages removed.
    """
    from operator_use.message.types import Role, TextContent, ToolCallContent, ThinkingContent
    result = []
    for msg in messages:
        if getattr(msg, 'role', None) == Role.ASSISTANT:
            contents = getattr(msg, 'contents', [])
            # Check for at least one usable content type
            has_usable = any(
                isinstance(c, (TextContent, ToolCallContent, ThinkingContent))
                for c in contents
            )
            if not has_usable:
                continue
        result.append(msg)
    return result


def strip_unusable_trailing_assistant(messages: list) -> list:
    """Return messages with trailing assistant turns removed if unusable.

    Non-destructive (copy of input list). Drops from end:
    - error/abort assistant turns (stop_reason != Stop)
    - empty assistant turns (no text content)
    - unanswered tool calls (no tool result follows)

    Keeps trailing assistant with real text and successful stop (legitimately completed turn).

    Args:
        messages: List of LLM messages.

    Returns:
        Filtered list with unusable trailing assistant messages removed.
    """
    from operator_use.message.types import Role, TextContent, ToolCallContent
    from operator_use.inference.types import StopReason

    msgs = list(messages)
    while msgs:
        last = msgs[-1]
        if getattr(last, "role", None) != Role.ASSISTANT:
            break
        # Drop error/abort turns
        stop_reason = getattr(last, "stop_reason", StopReason.Stop)
        if stop_reason != StopReason.Stop:
            msgs.pop()
            continue
        contents = getattr(last, "contents", [])
        # Check for real text content and unanswered tool calls
        has_text = any(
            isinstance(c, TextContent) and c.content.strip() for c in contents
        )
        has_tool_calls = any(isinstance(c, ToolCallContent) for c in contents)
        # Drop empty turns or dangling tool calls
        if has_tool_calls or not has_text:
            msgs.pop()
            continue
        break
    return msgs
