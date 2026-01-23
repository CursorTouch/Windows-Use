from pydantic import BaseModel,ConfigDict
from textwrap import shorten
from typing import Literal
from PIL.Image import Image
from io import BytesIO
import base64

class BaseMessage(BaseModel):
    role: Literal["system", "human", "ai", "tool"]
    content: str | None = None
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class SystemMessage(BaseMessage):
    role: Literal["system"] = "system"
    content: str

    def __repr__(self) -> str:
        return f"SystemMessage(content={self.content})"

class HumanMessage(BaseMessage):
    role: Literal["user"] = "human"
    content: str

    def __repr__(self) -> str:
        return f"HumanMessage(content={self.content})"
    
class ImageMessage(BaseMessage):
    role: Literal["human"] = "human"
    content: str
    image: Image|None = None
    images: list[Image] = []
    mime_type: str="image/png"
    
    def image_to_base64(self) -> str:
        image_bytes = self.image_to_bytes()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        return base64_image
    
    def scale_image(self, scale: float=0.5) -> None:
        if self.image:
            size=(int(self.image.width * scale), int(self.image.height * scale))
            self.image = self.image.resize(size=size)

    def scale_images(self, scale: float=0.5) -> None:
        if self.image:
            self.scale_image(scale)
        for i in range(len(self.images)):
            size=(int(self.images[i].width * scale), int(self.images[i].height * scale))
            self.images[i] = self.images[i].resize(size=size)

    def image_to_bytes(self) -> bytes:
        buffered = BytesIO()
        format = self.mime_type.split("/")[-1]
        self.image.save(buffered, format=format,quality=80)
        return buffered.getvalue()

    def convert_images(self, format: str="base64") -> list[str|bytes]:
        results = []
        target_images = self.images if self.images else ([self.image] if self.image else [])
        for img in target_images:
            buffered = BytesIO()
            img_format = self.mime_type.split("/")[-1]
            img.save(buffered, format=img_format, quality=80)
            if format == "base64":
                results.append(base64.b64encode(buffered.getvalue()).decode("utf-8"))
            else:
                results.append(buffered.getvalue())
        return results

    def __repr__(self) -> str:
        img_desc = shorten(str(self.image), width=30) if self.image else f"{len(self.images)} images"
        return f"ImageMessage(content={self.content}, image={img_desc}, mime_type={self.mime_type})"

class AIMessage(BaseMessage):
    role: Literal["ai"] = "ai"
    content: str | None = None

    def __repr__(self) -> str:
        return f"AIMessage(content={self.content})"

class ToolMessage(BaseMessage):
    role: Literal["tool"] = "tool"
    id: str  # Tool call id
    name: str # Tool name
    params: dict = {} # Tool parameters
    content: str | None = None # Tool result

    def __repr__(self) -> str:
        return f"ToolMessage(name={self.name}, params={self.params}, content={self.content})"