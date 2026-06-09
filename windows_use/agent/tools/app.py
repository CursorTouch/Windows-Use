from typing import Literal, Optional
from pydantic import BaseModel, Field
from windows_use.tool.types import Tool, ToolResult, ToolInvocation, ToolExecutionMode


class AppSchema(BaseModel):
    mode: Literal["launch", "switch", "resize"] = Field(
        ..., description="Application operation mode"
    )
    name: str = Field(..., description="Application name or title")
    size: Optional[tuple[int, int]] = Field(
        None, description="Size (width, height) for resize mode"
    )
    loc: Optional[tuple[int, int]] = Field(
        None, description="Location (x, y) for resize mode"
    )


class AppTool(Tool):
    def __init__(self, desktop):
        self.desktop = desktop
        super().__init__(
            name="app",
            description="Launch, switch to, or resize an application",
            schema=AppSchema,
            execution_mode=ToolExecutionMode.Sequential,
            display_name="App Control",
        )

    async def execute(
        self, invocation: ToolInvocation, tool_execution_update_callback=None, signal=None
    ) -> ToolResult:
        try:
            params = AppSchema.model_validate(invocation.params)
            result = self.desktop.app(
                mode=params.mode,
                name=params.name,
                size=params.size,
                loc=params.loc,
            )

            # Check if result looks like an error message
            if any(
                error_phrase in result.lower()
                for error_phrase in ["failed", "error", "not found", "not detected"]
            ):
                return ToolResult.error(invocation.id, result)

            return ToolResult.ok(invocation.id, result)
        except Exception as e:
            return ToolResult.error(invocation.id, f"App control failed: {str(e)}")
