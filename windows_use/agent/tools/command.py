from pydantic import BaseModel, Field
from windows_use.tool.types import Tool, ToolResult, ToolInvocation, ToolExecutionMode


class CommandSchema(BaseModel):
    command: str = Field(..., description="PowerShell command to execute")
    timeout: int = Field(default=10, ge=1, le=300, description="Command timeout in seconds")


class CommandTool(Tool):
    def __init__(self, desktop):
        self.desktop = desktop
        super().__init__(
            name="execute_command",
            description="Execute a PowerShell command",
            schema=CommandSchema,
            execution_mode=ToolExecutionMode.Sequential,
            display_name="Execute Command",
        )

    async def execute(
        self, invocation: ToolInvocation, tool_execution_update_callback=None, signal=None
    ) -> ToolResult:
        try:
            params = CommandSchema.model_validate(invocation.params)
            output, status = self.desktop.execute_command(params.command, timeout=params.timeout)

            if status != 0:
                return ToolResult.error(
                    invocation.id,
                    f"Command failed (exit code {status}): {output}",
                )

            return ToolResult.ok(
                invocation.id,
                output or "Command executed successfully",
            )
        except Exception as e:
            return ToolResult.error(invocation.id, f"Execute command failed: {str(e)}")
