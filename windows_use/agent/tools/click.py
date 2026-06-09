from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from windows_use.tool.types import Tool, ToolResult, ToolInvocation, ToolExecutionMode


class ClickSchema(BaseModel):
    x: int = Field(..., description="X coordinate")
    y: int = Field(..., description="Y coordinate")
    button: Literal["left", "right", "middle"] = Field(
        default="left", description="Mouse button to click"
    )
    clicks: int = Field(default=1, ge=1, le=3, description="Number of clicks (1=single, 2=double, 3=triple)")


class ClickTool(Tool):
    def __init__(self, desktop):
        self.desktop = desktop
        super().__init__(
            name="click",
            description="Click at specified coordinates on screen",
            schema=ClickSchema,
            execution_mode=ToolExecutionMode.Sequential,
            display_name="Click",
        )

    async def execute(
        self, invocation: ToolInvocation, tool_execution_update_callback=None, signal=None
    ) -> ToolResult:
        try:
            params = ClickSchema.model_validate(invocation.params)
            self.desktop.click((params.x, params.y), button=params.button, clicks=params.clicks)
            return ToolResult.ok(
                invocation.id,
                f"Clicked {params.button} button at ({params.x}, {params.y}) {params.clicks} time(s)",
            )
        except Exception as e:
            return ToolResult.error(invocation.id, f"Click failed: {str(e)}")
