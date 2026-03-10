"""Message models (BaseModel from views)."""

from pydantic import BaseModel, ConfigDict
from textwrap import shorten
from typing import Any, Literal
from PIL.Image import Image
from io import BytesIO
import base64

class Usage(BaseModel):
    """Token usage information from LLM responses."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    image_tokens: int | None = None
    thinking_tokens: int | None = None
    cache_creation_input_tokens: int | None = None
    cache_read_input_tokens: int | None = None


class BaseMessage(BaseModel):
    role: Literal["system", "human", "ai", "tool"]
    content: str | None = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-serializable dict."""
        d = self.model_dump(mode="json")
        if "role" not in d:
            d["role"] = self.role
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "BaseMessage":
        """Deserialize a message from a dict. Dispatches by role to the correct subclass."""
        role = d.get("role", "human")
        msg_cls = {
            "system": SystemMessage,
            "human": HumanMessage,
            "ai": AIMessage,
            "tool": ToolMessage,
        }.get(role, HumanMessage)
        return msg_cls.model_validate(d)


class SystemMessage(BaseMessage):
    role: Literal["system"] = "system"
    content: str

    def __repr__(self) -> str:
        return f"SystemMessage(content={shorten(self.content, width=80, placeholder='...')})"


class HumanMessage(BaseMessage):
    role: Literal["human"] = "human"
    content: str

    def __repr__(self) -> str:
        return f"HumanMessage(content={shorten(self.content, width=80, placeholder='...')})"


class ImageMessage(BaseMessage):
    role: Literal["human"] = "human"
    content: str
    images: list[Any] = []
    mime_type: str = "image/png"

    _MAX_IMAGE_BYTES: int = 4_800_000

    @staticmethod
    def _compress_image(img, mime_type: str, max_bytes: int = 4_800_000) -> tuple[bytes, str]:
        if Image is None:
            raise ImportError("Pillow is required for ImageMessage. Install with: pip install pillow")
        from PIL.Image import Image as PILImage

        def _save(image, fmt: str, quality: int) -> bytes:
            buf = BytesIO()
            save_img = image.convert("RGB") if fmt.upper() == "JPEG" else image
            save_img.save(buf, format=fmt, quality=quality)
            return buf.getvalue()

        img_format = mime_type.split("/")[-1].upper()
        if img_format == "JPG":
            img_format = "JPEG"
        original_mime = mime_type

        data = _save(img, img_format, 85)
        if len(data) <= max_bytes:
            return data, original_mime

        img_format = "JPEG"
        actual_mime = "image/jpeg"

        for quality in (80, 60, 40, 25):
            data = _save(img, img_format, quality)
            if len(data) <= max_bytes:
                return data, actual_mime

        current = img
        for _ in range(5):
            new_w = max(current.width // 2, 320)
            new_h = max(current.height // 2, 240)
            current = current.resize((new_w, new_h), resample=3)
            data = _save(current, img_format, 50)
            if len(data) <= max_bytes:
                return data, actual_mime

        return data, actual_mime

    def scale_images(self, scale: float = 0.5) -> None:
        for i in range(len(self.images)):
            size = (int(self.images[i].width * scale), int(self.images[i].height * scale))
            self.images[i] = self.images[i].resize(size=size)

    def convert_images(self, format: str = "base64") -> list[str | bytes]:
        results = []
        actual_mime = self.mime_type
        for img in self.images:
            data, actual_mime = self._compress_image(img, self.mime_type, self._MAX_IMAGE_BYTES)
            if format == "base64":
                results.append(base64.b64encode(data).decode("utf-8"))
            else:
                results.append(data)
        self.mime_type = actual_mime
        return results

    def to_dict(self) -> dict[str, Any]:
        """Serialize for persistence. Drops image data; content is preserved for history."""
        return {"role": "human", "content": self.content or ""}

    def __repr__(self) -> str:
        return f"ImageMessage(content={shorten(self.content, width=80, placeholder='...')}, images={len(self.images)}, mime_type={self.mime_type})"


class AIMessage(BaseMessage):
    role: Literal["ai"] = "ai"
    thinking: str | None = None
    thinking_signature: str | bytes | None = None
    content: str | dict | None = None
    usage: Usage | None = None

    def __repr__(self) -> str:
        return f"AIMessage(content={self.content}, thinking={shorten(str(self.thinking), width=50, placeholder='...')})"


class ToolMessage(BaseMessage):
    role: Literal["tool"] = "tool"
    thinking: str | None = None
    thinking_signature: str | bytes | None = None
    id: str
    name: str
    params: dict = {}
    content: str | None = None
    usage: Usage | None = None

    def __repr__(self) -> str:
        return f"ToolMessage(name={self.name}, id={self.id}, params={self.params}, content={shorten(self.content or '', width=80, placeholder='...')}, thinking={shorten(str(self.thinking), width=50, placeholder='...')})"
