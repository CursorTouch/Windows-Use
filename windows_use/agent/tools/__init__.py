from windows_use.agent.tools.service import (
    app_tool,
    click_tool,
    desktop_tool,
    done_tool,
    file_tool,
    memory_tool,
    move_tool,
    multi_edit_tool,
    multi_select_tool,
    scrape_tool,
    scroll_tool,
    shell_tool,
    shortcut_tool,
    type_tool,
    wait_tool,
)
from windows_use.tools import Tool

BUILTIN_TOOLS = [
    click_tool,
    type_tool,
    app_tool,
    shell_tool,
    done_tool,
    shortcut_tool,
    scroll_tool,
    move_tool,
    wait_tool,
    scrape_tool,
    desktop_tool,
]

EXPERIMENTAL_TOOLS = [
    multi_select_tool,
    multi_edit_tool,
    file_tool,
    memory_tool,
]

__all__ = [
    "BUILTIN_TOOLS",
    "EXPERIMENTAL_TOOLS",
    "Tool",
]
