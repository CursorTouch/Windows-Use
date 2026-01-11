# tests/unit/desktop/test_desktop_init.py

import pytest
from unittest.mock import MagicMock, patch
from PIL.Image import Image as PILImage
from PIL import Image
from io import BytesIO
import base64
import subprocess
import csv
import io
from fuzzywuzzy import process
from time import sleep

from windows_use.desktop.service import Desktop
from windows_use.desktop.views import DesktopState, App, Size
from windows_use.desktop.config import EXCLUDED_APPS, AVOIDED_APPS
# No need to import Tree here, as we will patch its source
from windows_use.tree.views import TreeState
import uiautomation as uia
import pyautogui

class TestDesktop:
    """
    Tests for the Desktop class in windows_use.desktop.__init__.py.
    """

    @pytest.fixture(autouse=True)
    def setup_mocks(self):
        """
        Mocks global dependencies for Desktop tests.
        """
        # --- FIX: Patch 'Tree' at its source module 'windows_use.tree' ---
        with patch("windows_use.desktop.pyautogui") as mock_pyautogui, \
             patch("windows_use.desktop.GetScreenSize") as mock_get_screen_size, \
             patch("windows_use.desktop.GetRootControl") as mock_get_root_control, \
             patch("windows_use.desktop.ControlFromCursor") as mock_control_from_cursor, \
             patch("windows_use.desktop.SetWindowTopmost") as mock_set_window_topmost, \
             patch("windows_use.desktop.subprocess.run") as mock_subprocess_run, \
             patch("windows_use.desktop.csv") as mock_csv, \
             patch("windows_use.desktop.io") as mock_io, \
             patch("windows_use.desktop.process") as mock_process, \
             patch("windows_use.desktop.sleep") as mock_sleep, \
             patch("windows_use.tree.Tree") as MockTree:

            self.mock_pyautogui = mock_pyautogui
            self.mock_get_screen_size = mock_get_screen_size
            self.mock_get_root_control = mock_get_root_control
            self.mock_control_from_cursor = mock_control_from_cursor
            self.mock_set_window_topmost = mock_set_window_topmost
            self.mock_subprocess_run = mock_subprocess_run
            self.mock_csv = mock_csv
            self.mock_io = mock_io
            self.mock_process = mock_process
            self.mock_sleep = mock_sleep
            self.MockTree = MockTree
            yield

    @pytest.fixture
    def desktop_instance(self):
        """
        Provides a Desktop instance for testing.
        """
        return Desktop()

    @pytest.fixture
    def mock_control(self):
        """
        Provides a mock uiautomation.Control instance.
        """
        mock = MagicMock(spec=uia.Control)
        mock_rect = MagicMock()
        mock_rect.isempty.return_value = False
        mock_rect.width.return_value = 100
        mock_rect.height.return_value = 100
        mock.BoundingRectangle = mock_rect
        mock.Name = "MockControl"
        mock.ControlTypeName = "PaneControl"
        mock.NativeWindowHandle = 12345
        mock.GetChildren.return_value = []
        mock.IsControlElement = True
        mock.IsOffscreen = False
        mock.IsEnabled = True
        return mock

    @pytest.fixture
    def mock_tree_state(self):
        """
        Provides a mock TreeState instance.
        """
        mock = MagicMock(spec=TreeState)
        mock.interactive_nodes = []
        mock.informative_nodes = []
        mock.scrollable_nodes = []
        return mock

    def test_init(self, desktop_instance):
        """
        Test Desktop initialization.
        """
        assert desktop_instance.desktop_state is None

    @pytest.mark.parametrize(
        "use_vision", [True, False]
    )
    def test_get_state(self, desktop_instance, mock_tree_state, use_vision):
        """
        Test `get_state` method correctly retrieves and sets desktop state.
        """
        desktop_instance.get_apps = MagicMock(return_value=[
            App(name="ActiveApp", depth=0, status="Normal", size=Size(100, 100), handle=1),
            App(name="OtherApp", depth=1, status="Normal", size=Size(100, 100), handle=2)
        ])
        desktop_instance.screenshot_in_bytes = MagicMock(return_value="base64_screenshot")

        mock_tree_instance = self.MockTree.return_value
        mock_tree_instance.get_state.return_value = mock_tree_state
        mock_tree_instance.annotated_screenshot.return_value = MagicMock(spec=PILImage)

        state = desktop_instance.get_state(use_vision=use_vision)

        self.MockTree.assert_called_once_with(desktop_instance)
        mock_tree_instance.get_state.assert_called_once()
        desktop_instance.get_apps.assert_called_once()

        if use_vision:
            mock_tree_instance.annotated_screenshot.assert_called_once_with(
                mock_tree_state.interactive_nodes, scale=0.5
            )
            desktop_instance.screenshot_in_bytes.assert_called_once_with(
                mock_tree_instance.annotated_screenshot.return_value
            )
            assert state.screenshot == "base64_screenshot"
        else:
            mock_tree_instance.annotated_screenshot.assert_not_called()
            desktop_instance.screenshot_in_bytes.assert_not_called()
            assert state.screenshot is None

        assert state.apps == [App(name="OtherApp", depth=1, status="Normal", size=Size(100, 100), handle=2)]
        assert state.active_app == App(name="ActiveApp", depth=0, status="Normal", size=Size(100, 100), handle=1)
        assert state.tree_state == mock_tree_state
        assert desktop_instance.desktop_state == state

    # The rest of the tests in this file should now pass without changes...
    def test_get_taskbar(self, desktop_instance, mock_control):
        mock_root = MagicMock(spec=uia.Control)
        mock_root.GetFirstChildControl.return_value = mock_control
        self.mock_get_root_control.return_value = mock_root
        taskbar = desktop_instance.get_taskbar()
        self.mock_get_root_control.assert_called_once()
        assert taskbar == mock_control

    @pytest.mark.parametrize(
        "is_empty, window_width, window_height, taskbar_height, expected_status",
        [
            (True, 0, 0, 40, "Minimized"),
            (False, 1920, 1040, 40, "Maximized"),
            (False, 800, 600, 40, "Normal"),
        ],
    )
    def test_get_app_status(self, desktop_instance, mock_control, is_empty, window_width, window_height, taskbar_height, expected_status):
        mock_control.BoundingRectangle.isempty.return_value = is_empty
        mock_control.BoundingRectangle.width.return_value = window_width
        mock_control.BoundingRectangle.height.return_value = window_height
        self.mock_get_screen_size.return_value = (1920, 1080)
        mock_taskbar = MagicMock()
        mock_taskbar.BoundingRectangle.height.return_value = taskbar_height
        desktop_instance.get_taskbar = MagicMock(return_value=mock_taskbar)
        status = desktop_instance.get_app_status(mock_control)
        assert status == expected_status