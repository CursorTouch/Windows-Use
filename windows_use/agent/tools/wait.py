import asyncio
from pydantic import BaseModel, Field
from windows_use.tool.types import Tool, ToolResult, ToolInvocation, ToolExecutionMode


class WaitSchema(BaseModel):
    seconds: float = Field(..., ge=0.1, le=60, description="Seconds to wait")


class WaitTool(Tool):
    def __init__(self):
        super().__init__(
            name="wait",
            description="Wait for specified number of seconds",
            schema=WaitSchema,
            execution_mode=ToolExecutionMode.Sequential,
            display_name="Wait",
        )

    async def execute(
        self, invocation: ToolInvocation, tool_execution_update_callback=None, signal=None
    ) -> ToolResult:
        try:
            params = WaitSchema.model_validate(invocation.params)
            await asyncio.sleep(params.seconds)
            return ToolResult.ok(
                invocation.id,
                f"Waited {params.seconds} second(s)",
            )
        except Exception as e:
            return ToolResult.error(invocation.id, f"Wait failed: {str(e)}")
