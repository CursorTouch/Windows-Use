from pydantic import BaseModel

class ToolResult(BaseModel):
    is_success: bool
    content: str | None = None
    error: str | None = None
    confidence: float | None = None
    evidence: dict | None = None