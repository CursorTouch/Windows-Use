from pydantic import BaseModel, Field
from windows_use.tool.types import Tool, ToolResult, ToolInvocation, ToolExecutionMode


class DragSchema(BaseModel):
    x: int = Field(..., description="Target X coordinate")
    y: int = Field(..., description="Target Y coordinate")


class DragTool(Tool):
    def __init__(self, desktop):
        self.desktop = desktop
        super().__init__(
            name="drag",
            description="Drag from current cursor position to target coordinates",
            schema=DragSchema,
            execution_mode=ToolExecutionMode.Sequential,
            display_name="Drag",
        )

    async def execute(
        self, invocation: ToolInvocation, tool_execution_update_callback=None, signal=None
    ) -> ToolResult:
        try:
            params = DragSchema.model_validate(invocation.params)
            self.desktop.drag((params.x, params.y))
            return ToolResult.ok(
                invocation.id,
                f"Dragged to ({params.x}, {params.y})",
            )
        except Exception as e:
            return ToolResult.error(invocation.id, f"Drag failed: {str(e)}")
