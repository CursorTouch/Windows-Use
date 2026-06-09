from pydantic import BaseModel, Field
from windows_use.tool.types import Tool, ToolResult, ToolInvocation, ToolExecutionMode


class MoveSchema(BaseModel):
    x: int = Field(..., description="X coordinate")
    y: int = Field(..., description="Y coordinate")


class MoveTool(Tool):
    def __init__(self, desktop):
        self.desktop = desktop
        super().__init__(
            name="move",
            description="Move mouse to specified coordinates",
            schema=MoveSchema,
            execution_mode=ToolExecutionMode.Sequential,
            display_name="Move",
        )

    async def execute(
        self, invocation: ToolInvocation, tool_execution_update_callback=None, signal=None
    ) -> ToolResult:
        try:
            params = MoveSchema.model_validate(invocation.params)
            self.desktop.move((params.x, params.y))
            return ToolResult.ok(
                invocation.id,
                f"Moved mouse to ({params.x}, {params.y})",
            )
        except Exception as e:
            return ToolResult.error(invocation.id, f"Move failed: {str(e)}")
