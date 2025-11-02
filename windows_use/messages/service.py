from pydantic import BaseModel
from textwrap import shorten
from typing import Literal
from PIL.Image import Image
from io import BytesIO
import base64

class BaseMessage(BaseModel):
    role: Literal["system", "human", "ai"]
    content: str
    
    class Config:
        arbitrary_types_allowed = True

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
    image: Image|None
    mime_type: str="image/png"
    
    def image_to_base64(self) -> str:
        image_bytes = self.image_to_bytes()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        return base64_image
    
    def scale_image(self, scale: float=0.5) -> None:
        size=(int(self.image.width * scale), int(self.image.height * scale))
        self.image = self.image.resize(size=size)

    def image_to_bytes(self) -> bytes:
        buffered = BytesIO()
        format = self.mime_type.split("/")[-1]
        self.image.save(buffered, format=format,quality=80)
        return buffered.getvalue()

    def __repr__(self) -> str:
        return f"ImageMessage(content={self.content}, image={shorten(self.image, width=30, placeholder='...')}, mime_type={self.mime_type})"

class AIMessage(BaseMessage):
    role: Literal["ai"] = "ai"
    content: str

    def __repr__(self) -> str:
        return f"AIMessage(content={self.content})"