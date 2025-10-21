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
    
    def image_to_base64(self) -> str:
        buffered = BytesIO()
        self.image.save(buffered, format="PNG")
        base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{base64_image}"
    
    def image_to_bytes(self) -> bytes:
        buffered = BytesIO()
        self.image.save(buffered, format="PNG")
        return buffered.getvalue()

    def __repr__(self) -> str:
        return f"ImageMessage(content={self.content}, image={shorten(self.image, width=30, placeholder='...')})"

class AIMessage(BaseMessage):
    role: Literal["ai"] = "ai"
    content: str

    def __repr__(self) -> str:
        return f"AIMessage(content={self.content})"