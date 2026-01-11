# tests/unit/agent/agent_tools/test_agent_tools_service.py

import pytest
from unittest.mock import MagicMock, patch
from typing import Literal
from pydantic import ValidationError
from textwrap import dedent

from windows_use.agent.tools.service import (
    done_tool,
    launch_tool,
    shell_tool,
    clipboard_tool,
    switch_tool,
    click_tool,
    type_tool,
    scroll_tool,
    drag_tool,
    move_tool,
    shortcut_tool,
    key_tool,
    wait_tool,
    scrape_tool,
)
from windows_use.desktop.service import Desktop
from windows_use.agent.tools.views import (
    Click,
    Type,
    Launch,
    Scroll,
    Drag,
    Move,
    Shortcut,
    Key,
    Wait,
    Scrape,
    Done,
    Clipboard,
    Shell,
    Switch,
)
import uiautomation as uia
import pyperclip as pc
import pyautogui as pg
import requests
from markdownify import markdownify

class TestAgentToolsService:
    """
    Tests for the tool functions in windows_use.agent.tools.service.
    """

    @pytest.fixture(autouse=True)
    def setup_pyautogui_mocks(self):
        """
        Mocks pyautogui functions globally for all tests in this class.
        """
        with patch("pyautogui.sleep"), \
             patch("pyautogui.position"), \
             patch("pyautogui.size"), \
             patch("pyautogui.screenshot"), \
             patch("pyautogui.mouseDown"), \
             patch("pyautogui.click"), \
             patch("pyautogui.mouseUp"), \
             patch("pyautogui.press"), \
             patch("pyautogui.hotkey"), \
             patch("pyautogui.typewrite"), \
             patch("pyautogui.keyDown"), \
             patch("pyautogui.keyUp"):
            yield

    @pytest.fixture
    def mock_desktop(self):
        """
        Provides a mock Desktop instance for tool functions.
        """
        mock = MagicMock(spec=Desktop)
        mock.get_element_under_cursor.return_value = MagicMock(
            Name="MockElement", ControlTypeName="MockControl"
        )
        return mock

    @pytest.fixture
    def mock_cursor(self):
        """
        Provides a mock SystemCursor instance.
        """
        with patch("windows_use.agent.tools.service.cursor") as mock:
            yield mock

    def test_done_tool(self, mock_desktop):
        """
        Test `done_tool` returns the provided answer.
        """
        answer = "Task completed successfully."
        result = done_tool.run({"answer": answer, "desktop": mock_desktop})
        assert result == answer

    @pytest.mark.parametrize(
        "app_name, launch_status, expected_output",
        [
            ("notepad", 0, "Launched Notepad."),
            ("chrome", 0, "Launched Chrome."),
            ("nonexistent", 1, "Failed to launch Nonexistent."),
        ],
    )
    @patch("windows_use.agent.tools.service.pg.sleep")
    def test_launch_tool(self, mock_sleep, mock_desktop, app_name, launch_status, expected_output):
        """
        Test `launch_tool` for successful and failed application launches.
        """
        mock_desktop.launch_app.return_value = (None, launch_status)
        result = launch_tool.run({"name": app_name, "desktop": mock_desktop})
        mock_desktop.launch_app.assert_called_once_with(app_name)
        mock_sleep.assert_called_once_with(1.25)
        assert result == expected_output

    @pytest.mark.parametrize(
        "command, response, status, expected_output",
        [
            ("Get-Process", "Process list", 0, "Status Code: 0\nResponse: Process list"),
            ("Invalid-Command", "Error output", 1, "Status Code: 1\nResponse: Error output"),
        ],
    )
    def test_shell_tool(self, mock_desktop, command, response, status, expected_output):
        """
        Test `shell_tool` executes PowerShell commands and returns output.
        """
        mock_desktop.execute_command.return_value = (response, status)
        result = shell_tool.run({"command": command, "desktop": mock_desktop})
        mock_desktop.execute_command.assert_called_once_with(command)
        assert result == expected_output

    @pytest.mark.parametrize(
        "mode, text, expected_pc_call, expected_result, raises_error",
        [
            pytest.param("copy", "hello", "copy", 'Copied "hello" to clipboard', False, id="copy-success"),
            pytest.param("paste", None, "paste", 'Clipboard Content: "mock_clipboard_content"', False, id="paste-success"),
            pytest.param("copy", None, None, "must be provided for 'copy' mode", True, id="copy-fail-no-text"),
            pytest.param("paste", "hi", None, "must not be provided for 'paste' mode", True, id="paste-fail-with-text"),
        ],
    )
    @patch("windows_use.agent.tools.service.pc")
    def test_clipboard_tool(
        self, mock_pc, mock_desktop, mode, text, expected_pc_call, expected_result, raises_error
    ):
        """
        Test `clipboard_tool` for copy and paste operations, including error cases.
        """
        mock_pc.paste.return_value = "mock_clipboard_content"

        tool_input = {"mode": mode, "desktop": mock_desktop}
        if text is not None:
            tool_input["text"] = text

        if raises_error:
            # Pydantic validation happens inside the tool.run(), which raises ValidationError
            with pytest.raises(ValidationError, match=expected_result):
                clipboard_tool.run(tool_input)
        else:
            result = clipboard_tool.run(tool_input)
            if expected_pc_call == "copy":
                mock_pc.copy.assert_called_once_with(text)
            elif expected_pc_call == "paste":
                mock_pc.paste.assert_called_once()
            assert result == expected_result

    @pytest.mark.parametrize(
        "app_name, switch_status, expected_output",
        [
            ("notepad", 0, "Switched to Notepad window."),
            ("chrome", 0, "Switched to Chrome window."),
            ("nonexistent", 1, "Failed to switch to Nonexistent window."),
        ],
    )
    def test_switch_tool(self, mock_desktop, app_name, switch_status, expected_output):
        """
        Test `switch_tool` for successful and failed application switches.
        """
        mock_desktop.switch_app.return_value = (None, switch_status)
        result = switch_tool.run({"name": app_name, "desktop": mock_desktop})
        mock_desktop.switch_app.assert_called_once_with(app_name)
        assert result == expected_output

    @pytest.mark.parametrize(
        "loc, button, clicks, expected_output_part",
        [
            ((100, 200), "left", 1, "Single left Clicked on MockElement Element with ControlType MockControl at (100,200)."),
            ((50, 50), "right", 2, "Double right Clicked on MockElement Element with ControlType MockControl at (50,50)."),
            ((10, 10), "middle", 3, "Triple middle Clicked on MockElement Element with ControlType MockControl at (10,10)."),
        ],
    )
    def test_click_tool(self, mock_desktop, mock_cursor, loc, button, clicks, expected_output_part):
        """
        Test `click_tool` performs correct mouse actions and returns expected message.
        """
        result = click_tool.run({"loc": loc, "button": button, "clicks": clicks, "desktop": mock_desktop})
        mock_cursor.move_to.assert_called_once_with(loc)
        mock_desktop.get_element_under_cursor.assert_called_once()
        pg.mouseDown.assert_called_once()
        pg.click.assert_called_once_with(button=button, clicks=clicks)
        pg.mouseUp.assert_called_once()
        pg.sleep.assert_called_once_with(1.0)
        assert result == expected_output_part

    @pytest.mark.parametrize(
        "loc, text, clear, caret_position, expected_pg_calls, expected_output_part",
        [
            ((100, 100), "test text", "false", "idle", ["typewrite"], "Typed test text on MockElement Element with ControlType MockControl at (100,100)."),
            ((100, 100), "test text", "true", "idle", ["hotkey", "press", "typewrite"], "Typed test text on MockElement Element with ControlType MockControl at (100,100)."),
            ((100, 100), "test text", "false", "start", ["press", "typewrite"], "Typed test text on MockElement Element with ControlType MockControl at (100,100)."),
            ((100, 100), "test text", "false", "end", ["press", "typewrite"], "Typed test text on MockElement Element with ControlType MockControl at (100,100)."),
        ],
    )
    def test_type_tool(
        self,
        mock_desktop,
        mock_cursor,
        loc,
        text,
        clear,
        caret_position,
        expected_pg_calls,
        expected_output_part,
    ):
        """
        Test `type_tool` performs correct typing actions based on parameters.
        """
        result = type_tool.run(
            {"loc": loc, "text": text, "clear": clear, "caret_position": caret_position, "desktop": mock_desktop}
        )
        mock_cursor.click_on.assert_called_once_with(loc)
        mock_desktop.get_element_under_cursor.assert_called_once()

        if "hotkey" in expected_pg_calls:
            pg.hotkey.assert_called_once_with("ctrl", "a")
        if "press" in expected_pg_calls:
            if caret_position == "start":
                pg.press.assert_any_call("home")
            elif caret_position == "end":
                pg.press.assert_any_call("end")
            if clear == "true":
                pg.press.assert_any_call("backspace")
        pg.typewrite.assert_called_once_with(text, interval=0.1)
        assert result == expected_output_part

    @pytest.mark.parametrize(
        "loc, scroll_type, direction, wheel_times, expected_uia_call, expected_pg_calls, expected_output, raises_error, exception_type",
        [
            # Success cases
            (None, "vertical", "up", 1, "WheelUp", [], "Scrolled vertical up by 1 wheel times.", False, None),
            (None, "vertical", "down", 2, "WheelDown", [], "Scrolled vertical down by 2 wheel times.", False, None),
            (None, "horizontal", "left", 1, "WheelUp", ["keyDown", "sleep", "keyUp"], "Scrolled horizontal left by 1 wheel times.", False, None),
            (None, "horizontal", "right", 2, "WheelDown", ["keyDown", "sleep", "keyUp"], "Scrolled horizontal right by 2 wheel times.", False, None),
            ((10, 10), "vertical", "up", 1, "WheelUp", [], "Scrolled vertical up by 1 wheel times.", False, None),
            # Schema validation errors (Pydantic)
            (None, "vertical", "invalid", 1, None, [], "Input should be 'up', 'down', 'left' or 'right'", True, ValidationError),
            (None, "invalid", "up", 1, None, [], "Input should be 'horizontal' or 'vertical'", True, ValidationError),
        ],
    )
    @patch("windows_use.agent.tools.service.uia")
    def test_scroll_tool(
        self,
        mock_uia,
        mock_desktop,
        mock_cursor,
        loc,
        scroll_type,
        direction,
        wheel_times,
        expected_uia_call,
        expected_pg_calls,
        expected_output,
        raises_error,
        exception_type,
    ):
        """
        Test `scroll_tool` performs correct scrolling actions and handles invalid inputs.
        """
        tool_input = {
            "type": scroll_type,
            "direction": direction,
            "wheel_times": wheel_times,
            "desktop": mock_desktop
        }
        # Only add 'loc' if it's not None, which is the default
        if loc is not None:
            tool_input["loc"] = loc

        if raises_error:
            with pytest.raises(exception_type, match=expected_output):
                scroll_tool.run(tool_input)
            return # End the test here for error cases

        # The rest of the assertions only run for successful cases
        result = scroll_tool.run(tool_input)
        assert result == expected_output

        if loc:
            mock_cursor.move_to.assert_called_once_with(loc)
        else:
            mock_cursor.move_to.assert_not_called()

        if expected_uia_call == "WheelUp":
            mock_uia.WheelUp.assert_called_once_with(wheel_times)
        elif expected_uia_call == "WheelDown":
            mock_uia.WheelDown.assert_called_once_with(wheel_times)

        if "keyDown" in expected_pg_calls:
            pg.keyDown.assert_called_once_with("Shift")
            pg.keyUp.assert_called_once_with("Shift")
        else:
            pg.keyDown.assert_not_called()
            pg.keyUp.assert_not_called()

    def test_drag_tool(self, mock_desktop, mock_cursor):
        """
        Test `drag_tool` performs drag and drop and returns expected message.
        """
        from_loc = (10, 20)
        to_loc = (100, 200)
        result = drag_tool.run({"from_loc": from_loc, "to_loc": to_loc, "desktop": mock_desktop})
        mock_desktop.get_element_under_cursor.assert_called_once()
        mock_cursor.drag_and_drop.assert_called_once_with(from_loc, to_loc)
        assert result == "Dragged the MockElement element with ControlType MockControl from (10,20) to (100,200)."

    def test_move_tool(self, mock_desktop, mock_cursor):
        """
        Test `move_tool` moves the mouse cursor and returns expected message.
        """
        to_loc = (150, 250)
        result = move_tool.run({"to_loc": to_loc, "desktop": mock_desktop})
        mock_cursor.move_to.assert_called_once_with(to_loc)
        assert result == "Moved the mouse pointer to (150,250)."

    @pytest.mark.parametrize(
        "shortcut, expected_output",
        [
            (["ctrl", "c"], "Pressed ctrl+c."),
            (["alt", "f4"], "Pressed alt+f4."),
            (["win", "r"], "Pressed win+r."),
        ],
    )
    def test_shortcut_tool(self, mock_desktop, shortcut, expected_output):
        """
        Test `shortcut_tool` executes keyboard shortcuts.
        """
        result = shortcut_tool.run({"shortcut": shortcut, "desktop": mock_desktop})
        pg.hotkey.assert_called_once_with(*shortcut)
        assert result == expected_output

    @pytest.mark.parametrize(
        "key, expected_output",
        [
            ("enter", "Pressed the key enter."),
            ("escape", "Pressed the key escape."),
            ("tab", "Pressed the key tab."),
        ],
    )
    def test_key_tool(self, mock_desktop, key, expected_output):
        """
        Test `key_tool` presses individual keyboard keys.
        """
        result = key_tool.run({"key": key, "desktop": mock_desktop})
        pg.press.assert_called_once_with(key)
        assert result == expected_output

    @pytest.mark.parametrize(
        "duration, expected_output",
        [
            (1, "Waited for 1 seconds."),
            (5, "Waited for 5 seconds."),
        ],
    )
    def test_wait_tool(self, mock_desktop, duration, expected_output):
        """
        Test `wait_tool` pauses execution for the specified duration.
        """
        result = wait_tool.run({"duration": duration, "desktop": mock_desktop})
        pg.sleep.assert_called_once_with(duration)
        assert result == expected_output

    @patch("windows_use.agent.tools.service.requests")
    @patch("windows_use.agent.tools.service.markdownify")
    def test_scrape_tool_success(self, mock_markdownify, mock_requests, mock_desktop):
        """
        Test `scrape_tool` successfully fetches and converts webpage content.
        """
        mock_response = MagicMock()
        mock_response.text = "<html><body><h1>Hello</h1></body></html>"
        mock_requests.get.return_value = mock_response
        mock_markdownify.return_value = "# Hello"

        url = "https://example.com"
        result = scrape_tool.run({"url": url, "desktop": mock_desktop})

        mock_requests.get.assert_called_once_with(url, timeout=10)
        mock_markdownify.assert_called_once_with(html=mock_response.text)
        assert result == "Scraped the contents of the entire webpage:\n# Hello"

    @patch("windows_use.agent.tools.service.requests")
    @patch("windows_use.agent.tools.service.markdownify")
    def test_scrape_tool_request_exception(self, mock_markdownify, mock_requests, mock_desktop):
        """
        Test `scrape_tool` handles request exceptions.
        """
        mock_requests.get.side_effect = requests.exceptions.RequestException("Network error")

        url = "https://example.com"
        with pytest.raises(requests.exceptions.RequestException, match="Network error"):
            scrape_tool.run({"url": url, "desktop": mock_desktop})

        mock_requests.get.assert_called_once_with(url, timeout=10)
        mock_markdownify.assert_not_called()
