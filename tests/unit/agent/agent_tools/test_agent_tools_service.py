# tests/unit/agent/agent_tools/test_agent_tools_service.py

import pytest
from unittest.mock import MagicMock, patch, mock_open
from typing import Literal
from pathlib import Path

from windows_use.agent.tools.service import (
    done_tool,
    app_tool,
    shell_tool,
    click_tool,
    type_tool,
    scroll_tool,
    move_tool,
    shortcut_tool,
    wait_tool,
    scrape_tool,
    desktop_tool,
    memory_tool,
    multi_select_tool,
    multi_edit_tool
)
from windows_use.agent.desktop.service import Desktop

class TestAgentToolsService:
    """
    Tests for the tool functions in windows_use.agent.tools.service.
    Most tools delegate to the Desktop service, so we verify the delegation.
    """

    @pytest.fixture
    def mock_desktop(self):
        """
        Provides a mock Desktop instance.
        """
        mock = MagicMock(spec=Desktop)
        # Setup specific return values if needed
        mock.desktop_state = MagicMock()
        mock.desktop_state.tree_state = MagicMock()
        return mock

    def test_done_tool(self):
        """Test done_tool returns the response."""
        response = "Task done"
        assert done_tool.invoke(**{"answer": response}) == response

    @pytest.mark.parametrize("mode, name, loc, size", [
        ("launch", "notepad", None, None),
        ("switch", "chrome", None, None),
        ("resize", None, [0, 0], [100, 100]),
    ])
    def test_app_tool(self, mock_desktop, mode, name, loc, size):
        """Test app_tool delegation."""
        app_tool.invoke(**{"mode": mode, "name": name, "loc": loc, "size": size, "desktop": mock_desktop})
        mock_desktop.app.assert_called_once_with(mode, name, loc, size)

    def test_shell_tool(self, mock_desktop):
        """Test shell_tool delegation."""
        mock_desktop.execute_command.return_value = ("Output", 0)
        result = shell_tool.invoke(**{"command": "ls", "desktop": mock_desktop})
        mock_desktop.execute_command.assert_called_once_with("ls")
        assert "Output" in result
        assert "0" in result

    def test_click_tool(self, mock_desktop):
        """Test click_tool delegation."""
        click_tool.invoke(**{"loc": [10, 20], "button": "right", "clicks": 2, "desktop": mock_desktop})
        mock_desktop.click.assert_called_once_with([10, 20], "right", 2)

    def test_type_tool(self, mock_desktop):
        """Test type_tool delegation."""
        type_tool.invoke(**{"loc": [10, 20], "text": "hello", "clear": "true", "desktop": mock_desktop})
        mock_desktop.type.assert_called_once_with([10, 20], "hello", "true", "idle", "false")

    def test_scroll_tool(self, mock_desktop):
        """Test scroll_tool delegation."""
        # service.py: if response...
        mock_desktop.scroll.return_value = None 
        scroll_tool.invoke(**{"loc": [10, 20], "wheel_times": 3, "desktop": mock_desktop})
        mock_desktop.scroll.assert_called_once_with([10, 20], "vertical", "down", 3)

    def test_move_tool_drag(self, mock_desktop):
        """Test move_tool delegation (drag)."""
        move_tool.invoke(**{"loc": [10, 20], "drag": True, "desktop": mock_desktop})
        mock_desktop.drag.assert_called_once_with([10, 20])

    def test_move_tool_move(self, mock_desktop):
        """Test move_tool delegation (move)."""
        move_tool.invoke(**{"loc": [10, 20], "drag": False, "desktop": mock_desktop})
        mock_desktop.move.assert_called_once_with([10, 20])

    def test_shortcut_tool(self, mock_desktop):
        """Test shortcut_tool delegation."""
        shortcut_tool.invoke(**{"shortcut": "ctrl+c", "desktop": mock_desktop})
        mock_desktop.shortcut.assert_called_once_with("ctrl+c")

    def test_multi_select_tool(self, mock_desktop):
        """Test multi_select_tool delegation."""
        elements = [[10, 10], [20, 20]]
        multi_select_tool.invoke(**{"elements": elements, "press_ctrl": "true", "desktop": mock_desktop})
        mock_desktop.multi_select.assert_called_once_with("true", elements)

    def test_multi_edit_tool(self, mock_desktop):
        """Test multi_edit_tool delegation."""
        elements = [[10, 10, "text"]]
        multi_edit_tool.invoke(**{"elements": elements, "desktop": mock_desktop})
        mock_desktop.multi_edit.assert_called_once_with(elements)

    @patch("windows_use.agent.tools.service.sleep")
    def test_wait_tool(self, mock_sleep, mock_desktop):
        """Test wait_tool calls sleep."""
        wait_tool.invoke(**{"duration": 5, "desktop": mock_desktop})
        mock_sleep.assert_called_once_with(5)

    def test_scrape_tool(self, mock_desktop):
        """Test scrape_tool fetches text from visual tree."""
        # Setup mock tree state
        mock_node = MagicMock()
        mock_node.text = "Visual Content"
        mock_desktop.desktop_state.tree_state.dom_informative_nodes = [mock_node]
        mock_desktop.desktop_state.tree_state.dom_node = MagicMock(vertical_scroll_percent=0)
        
        result = scrape_tool.invoke(**{"url": "http://test", "desktop": mock_desktop})
        assert "Visual Content" in result
        assert "Reached top" in result

    @patch("windows_use.agent.tools.service.vdm_create")
    def test_desktop_tool_create(self, mock_create, mock_desktop):
        """Test desktop_tool create."""
        mock_create.return_value = "NewDesktop"
        result = desktop_tool.invoke(**{"action": "create", "desktop_name": "NewDesktop", "desktop": mock_desktop})
        mock_create.assert_called_once_with("NewDesktop")
        assert "Created desktop: 'NewDesktop'" in result

    def test_memory_tool_write(self):
        """Test memory_tool write mode."""
        # memory_tool uses Path.cwd() / '.memories'
        # We should patch Path to avoid real file I/O
        with patch("pathlib.Path.mkdir"), \
             patch("pathlib.Path.write_text") as mock_write:
             
            # We need to mock Path objects returned by / operator
            # This is tricky with simple mocks.
            # Alternatively, since it writes to .memories, we can use fs mock or just verify logic if possible.
            # Easier to check what it returns or if it errors.
            
            # Let's simple check if it runs without error and calls write_text on a path
            with patch("windows_use.agent.tools.service.memory_path") as mock_mem_path:
                mock_file = MagicMock()
                mock_mem_path.__truediv__.return_value = mock_file
                mock_file.name = "test.md"
                mock_file.parent = MagicMock()
                mock_file.parent.relative_to.return_value = Path("rel/path")
                
                result = memory_tool.invoke(**{"mode": "write", "path": "test.md", "content": "data"})
                
                mock_file.write_text.assert_called_once_with("data", encoding='utf-8')
                assert "test.md created" in result
