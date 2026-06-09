from typing import Literal
from pydantic import BaseModel, Field
from windows_use.tool.types import Tool, ToolResult, ToolInvocation, ToolExecutionMode


class TypeSchema(BaseModel):
    x: int = Field(..., description="X coordinate to click before typing")
    y: int = Field(..., description="Y coordinate to click before typing")
    text: str = Field(..., description="Text to type")
    caret_position: Literal["start", "end", "none"] = Field(
        default="none", description="Move caret to start or end before typing"
    )
    clear: Literal["true", "false"] = Field(
        default="false", description="Clear field before typing"
    )
    press_enter: Literal["true", "false"] = Field(
        default="false", description="Press Enter after typing"
    )


class TypeTool(Tool):
    def __init__(self, desktop):
        self.desktop = desktop
        super().__init__(
            name="type",
            description="Click at coordinates and type text",
            schema=TypeSchema,
            execution_mode=ToolExecutionMode.Sequential,
            display_name="Type",
        )

    async def execute(
        self, invocation: ToolInvocation, tool_execution_update_callback=None, signal=None
    ) -> ToolResult:
        try:
            params = TypeSchema.model_validate(invocation.params)
            self.desktop.type(
                (params.x, params.y),
                text=params.text,
                caret_position=params.caret_position,
                clear=params.clear,
                press_enter=params.press_enter,
            )
            return ToolResult.ok(
                invocation.id,
                f"Typed text at ({params.x}, {params.y})",
            )
        except Exception as e:
            return ToolResult.error(invocation.id, f"Type failed: {str(e)}")
