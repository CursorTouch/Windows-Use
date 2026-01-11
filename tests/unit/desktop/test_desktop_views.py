import pytest
from typing import Literal, Optional
from dataclasses import dataclass, field
from unittest.mock import MagicMock

from windows_use.desktop.views import App, Size, DesktopState
from windows_use.tree.views import TreeState, TreeElementNode, TextElementNode, ScrollElementNode, BoundingBox, Center

class TestDesktopViews:
    """
    Tests for the data models and view-related classes in windows_use.desktop.views.
    """

    def test_app_initialization(self):
        """
        Test App dataclass initialization.
        """
        size = Size(width=100, height=200)
        app = App(name="TestApp", depth=0, status="Normal", size=size, handle=123)
        assert app.name == "TestApp"
        assert app.depth == 0
        assert app.status == "Normal"
        assert app.size == size
        assert app.handle == 123

    def test_app_to_string(self):
        """
        Test App.to_string method.
        """
        size = Size(width=100, height=200)
        app = App(name="TestApp", depth=0, status="Normal", size=size, handle=123)
        expected_string = "Name: TestApp|Depth: 0|Status: Normal|Size: (100,200) Handle: 123"
        assert app.to_string() == expected_string

    def test_size_initialization(self):
        """
        Test Size dataclass initialization.
        """
        size = Size(width=100, height=200)
        assert size.width == 100
        assert size.height == 200

    def test_size_to_string(self):
        """
        Test Size.to_string method.
        """
        size = Size(width=100, height=200)
        assert size.to_string() == "(100,200)"

    def test_desktop_state_initialization(self):
        """
        Test DesktopState dataclass initialization.
        """
        mock_tree_state = MagicMock(spec=TreeState)
        state = DesktopState(apps=[], active_app=None, screenshot=None, tree_state=mock_tree_state)
        assert state.apps == []
        assert state.active_app is None
        assert state.screenshot is None
        assert state.tree_state == mock_tree_state

    @pytest.mark.parametrize(
        "active_app, expected_string",
        [
            (None, "No active app"),
            (App(name="ActiveApp", depth=0, status="Normal", size=Size(100, 100), handle=123), "Name: ActiveApp|Depth: 0|Status: Normal|Size: (100,100) Handle: 123"),
        ],
    )
    def test_active_app_to_string(self, active_app, expected_string):
        """
        Test DesktopState.active_app_to_string method.
        """
        mock_tree_state = MagicMock(spec=TreeState)
        state = DesktopState(apps=[], active_app=active_app, screenshot=None, tree_state=mock_tree_state)
        assert state.active_app_to_string() == expected_string

    @pytest.mark.parametrize(
        "apps, expected_string",
        [
            ([], "No apps opened"),
            ([App(name="App1", depth=0, status="Normal", size=Size(100, 100), handle=1),
              App(name="App2", depth=1, status="Minimized", size=Size(50, 50), handle=2)],
             "Name: App1|Depth: 0|Status: Normal|Size: (100,100) Handle: 1\n"
             "Name: App2|Depth: 1|Status: Minimized|Size: (50,50) Handle: 2"),
        ],
    )
    def test_apps_to_string(self, apps, expected_string):
        """
        Test DesktopState.apps_to_string method.
        """
        mock_tree_state = MagicMock(spec=TreeState)
        state = DesktopState(apps=apps, active_app=None, screenshot=None, tree_state=mock_tree_state)
        assert state.apps_to_string() == expected_string
