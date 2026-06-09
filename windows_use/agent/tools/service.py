from windows_use.tool.types import Tool, LoadToolsResult, ToolError
from windows_use.agent.tools.click import ClickTool
from windows_use.agent.tools.type import TypeTool
from windows_use.agent.tools.scroll import ScrollTool
from windows_use.agent.tools.move import MoveTool
from windows_use.agent.tools.wait import WaitTool
from windows_use.agent.tools.drag import DragTool
from windows_use.agent.tools.shortcut import ShortcutTool
from windows_use.agent.tools.command import CommandTool
from windows_use.agent.tools.app import AppTool


class AgentToolsService:
    """Service for loading and managing agent tools."""

    def __init__(self, desktop):
        """Initialize tools service with desktop automation instance.

        Args:
            desktop: Windows Desktop automation service instance.
        """
        self.desktop = desktop
        self._tools: dict[str, Tool] = {}

    def load_tools(self) -> LoadToolsResult:
        """Load all essential agent tools.

        Returns:
            LoadToolsResult containing list of loaded tools and any errors.
        """
        result = LoadToolsResult()

        # Essential tools for desktop automation
        tools_to_load = [
            (ClickTool(self.desktop), "click"),
            (TypeTool(self.desktop), "type"),
            (ScrollTool(self.desktop), "scroll"),
            (MoveTool(self.desktop), "move"),
            (WaitTool(), "wait"),
            (DragTool(self.desktop), "drag"),
            (ShortcutTool(self.desktop), "shortcut"),
            (CommandTool(self.desktop), "command"),
            (AppTool(self.desktop), "app"),
        ]

        for tool, tool_id in tools_to_load:
            try:
                self._tools[tool.name] = tool
                result.tools.append(tool)
            except Exception as e:
                result.errors.append(
                    ToolError(
                        path=f"windows_use.agent.tools.{tool_id}",
                        error=str(e),
                    )
                )

        return result

    def get_tool(self, name: str) -> Tool | None:
        """Get a tool by name.

        Args:
            name: Tool name.

        Returns:
            Tool instance or None if not found.
        """
        return self._tools.get(name)

    def get_all_tools(self) -> list[Tool]:
        """Get all loaded tools.

        Returns:
            List of all loaded tools.
        """
        return list(self._tools.values())
