from pydantic import BaseModel, Field
from windows_use.tool.types import Tool, ToolResult, ToolInvocation, ToolExecutionMode


class ShortcutSchema(BaseModel):
    keys: str = Field(
        ...,
        description="Keyboard shortcut (e.g., 'ctrl+c', 'alt+tab', 'shift+ctrl+s'). Use '+' to separate keys.",
    )


class ShortcutTool(Tool):
    def __init__(self, desktop):
        self.desktop = desktop
        super().__init__(
            name="shortcut",
            description="Execute keyboard shortcut",
            schema=ShortcutSchema,
            execution_mode=ToolExecutionMode.Sequential,
            display_name="Shortcut",
        )

    async def execute(
        self, invocation: ToolInvocation, tool_execution_update_callback=None, signal=None
    ) -> ToolResult:
        try:
            params = ShortcutSchema.model_validate(invocation.params)
            self.desktop.shortcut(params.keys)
            return ToolResult.ok(
                invocation.id,
                f"Executed shortcut: {params.keys}",
            )
        except Exception as e:
            return ToolResult.error(invocation.id, f"Shortcut failed: {str(e)}")
