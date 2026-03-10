# tests/unit/agent/agent_prompt/test_agent_prompt_service.py

import pytest
from unittest.mock import MagicMock, patch
from windows_use.agent.context.service import Context
from windows_use.agent.desktop.views import DesktopState, Browser


class TestContext:
    """Tests the Context service class."""

    @pytest.fixture
    def context(self):
        return Context()

    @pytest.fixture
    def mock_desktop(self):
        mock = MagicMock()
        mock.get_windows_version.return_value = "Windows 11"
        mock.get_default_language.return_value = "English"
        mock.get_user_account_type.return_value = "Admin"
        mock.get_dpi_scaling.return_value = "100%"
        return mock

    @pytest.fixture
    def mock_desktop_state(self):
        mock = MagicMock(spec=DesktopState)
        mock.active_window_to_string.return_value = "Active App: Notepad"
        mock.windows_to_string.return_value = "Open Apps: [Notepad]"
        mock.active_desktop_to_string.return_value = "Desktop 1"
        mock.desktops_to_string.return_value = "Desktops: [1, 2]"
        mock.tree_state = MagicMock()
        mock.tree_state.interactive_elements_to_string.return_value = "Interactive elements"
        mock.tree_state.scrollable_elements_to_string.return_value = "Scrollable elements"
        return mock

    @patch("windows_use.agent.context.service._load_template")
    @patch("windows_use.agent.context.service.uia.GetScreenSize", return_value=(1920, 1080))
    def test_system_flash(self, mock_screen_size, mock_load_template, context, mock_desktop):
        mock_load_template.return_value = "Flash: {datetime} {os} {browser} {max_steps}"
        msg = context.system(
            mode="flash",
            desktop=mock_desktop,
            browser=Browser.EDGE,
            max_steps=25,
            instructions=[],
        )
        assert "Flash:" in msg.content
        assert "Windows 11" in msg.content
        assert "25" in msg.content

    @patch("windows_use.agent.context.service._load_template")
    @patch("windows_use.agent.context.service.uia.GetScreenSize", return_value=(1920, 1080))
    def test_system_normal(self, mock_screen_size, mock_load_template, context, mock_desktop):
        mock_load_template.return_value = (
            "Normal: {datetime} {instructions} {os} {language} {browser} "
            "{home_dir} {user} {resolution} {max_steps}"
        )
        msg = context.system(
            mode="normal",
            desktop=mock_desktop,
            browser=Browser.EDGE,
            max_steps=25,
            instructions=["Do something"],
        )
        assert "Normal:" in msg.content
        assert "Windows 11" in msg.content
        assert "English" in msg.content
        assert "25" in msg.content
        assert "Do something" in msg.content

    @patch("windows_use.agent.context.service._load_template")
    @patch("windows_use.agent.context.service.uia.GetCursorPos", return_value=(100, 200))
    def test_human(self, mock_cursor_pos, mock_load_template, context, mock_desktop, mock_desktop_state):
        mock_desktop_state.screenshot = None
        mock_desktop.desktop_state = mock_desktop_state
        mock_desktop.get_state.return_value = mock_desktop_state
        mock_desktop.use_accessibility = True
        mock_desktop.use_vision = False
        mock_load_template.return_value = (
            "Human: {steps} {max_steps} {active_window} {windows} {cursor_location} "
            "{interactive_elements} {scrollable_elements} {active_desktop} {desktops} {query}"
        )
        msg = context.human(
            query="test query",
            step=2,
            max_steps=10,
            desktop=mock_desktop,
        )
        assert "Human:" in msg.content
        assert "test query" in msg.content
        assert "(100,200)" in msg.content
        assert "Interactive elements" in msg.content