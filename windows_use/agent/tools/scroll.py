from typing import Literal, Optional
from pydantic import BaseModel, Field
from windows_use.tool.types import Tool, ToolResult, ToolInvocation, ToolExecutionMode


class ScrollSchema(BaseModel):
    x: Optional[int] = Field(None, description="X coordinate to move to before scrolling")
    y: Optional[int] = Field(None, description="Y coordinate to move to before scrolling")
    direction: Literal["up", "down", "left", "right"] = Field(
        default="down", description="Scroll direction"
    )
    type: Literal["vertical", "horizontal"] = Field(
        default="vertical", description="Scroll type"
    )
    wheel_times: int = Field(default=1, ge=1, le=10, description="Number of scroll wheel turns")


class ScrollTool(Tool):
    def __init__(self, desktop):
        self.desktop = desktop
        super().__init__(
            name="scroll",
            description="Scroll in specified direction",
            schema=ScrollSchema,
            execution_mode=ToolExecutionMode.Sequential,
            display_name="Scroll",
        )

    async def execute(
        self, invocation: ToolInvocation, tool_execution_update_callback=None, signal=None
    ) -> ToolResult:
        try:
            params = ScrollSchema.model_validate(invocation.params)
            loc = None
            if params.x is not None and params.y is not None:
                loc = (params.x, params.y)

            error = self.desktop.scroll(
                loc=loc,
                type=params.type,
                direction=params.direction,
                wheel_times=params.wheel_times,
            )

            if error:
                return ToolResult.error(invocation.id, error)

            return ToolResult.ok(
                invocation.id,
                f"Scrolled {params.direction} ({params.wheel_times} times) in {params.type} direction",
            )
        except Exception as e:
            return ToolResult.error(invocation.id, f"Scroll failed: {str(e)}")
