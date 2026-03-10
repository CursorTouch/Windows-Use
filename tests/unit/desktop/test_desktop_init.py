# tests/unit/desktop/test_desktop_init.py

import pytest
from unittest.mock import MagicMock, patch
from windows_use.agent.desktop.service import Desktop
from windows_use.agent.desktop.views import DesktopState, Window, Size, Status
from windows_use.agent.tree.views import BoundingBox

class TestDesktopService:
    @pytest.fixture
    def desktop(self):
        # Patching dependencies in __init__
        with patch("windows_use.agent.desktop.service.uia.GetVirtualScreenSize", return_value=(1920, 1080)), \
             patch("windows_use.agent.desktop.service.Tree"):
            return Desktop()

    def test_init(self, desktop):
        assert desktop.desktop_state is None
        assert desktop.get_screen_size().width == 1920

    @patch("windows_use.agent.desktop.service.win32gui.EnumWindows")
    @patch("windows_use.agent.desktop.service.win32gui.IsWindowVisible")
    @patch("windows_use.agent.desktop.service.win32gui.GetWindowText")
    def test_get_controls_handles(self, mock_text, mock_visible, mock_enum, desktop):
        mock_visible.return_value = True
        mock_text.return_value = "Some Window"
        
        def side_effect(callback, lparam):
            callback(12345, lparam)
            return True
        mock_enum.side_effect = side_effect
        
        handles = desktop.get_controls_handles()
        assert 12345 in handles

    def test_get_state(self, desktop):
        # Mock dependencies of get_state
        mock_window = Window(
            name="Notepad", is_browser=False, depth=0, status=Status.NORMAL,
            bounding_box=BoundingBox(0,0,100,100,100,100), handle=123, process_id=456
        )
        
        with patch.object(desktop, 'get_controls_handles', return_value={123, 456}), \
             patch.object(desktop, 'get_windows', return_value=([mock_window], {123})), \
             patch.object(desktop, 'get_active_window', return_value=mock_window), \
             patch.object(desktop.tree, 'get_state', return_value=MagicMock()), \
             patch("windows_use.agent.desktop.service.get_current_desktop", return_value={"name": "Desktop 1"}), \
             patch("windows_use.agent.desktop.service.get_all_desktops", return_value=[{"name": "Desktop 1"}]):
             
             state = desktop.get_state(use_vision=False)
             
        assert isinstance(state, DesktopState)
        assert state.active_window.handle == 123
        assert len(state.windows) == 0 