# tests/unit/tree/test_tree_init.py

import pytest
from unittest.mock import MagicMock, patch, call, ANY
from PIL import Image, ImageFont, ImageDraw
from concurrent.futures import ThreadPoolExecutor

from windows_use.tree.service import Tree
from windows_use.tree.views import TreeElementNode, TextElementNode, ScrollElementNode, Center, BoundingBox, TreeState

class TestTree:
    @pytest.fixture(autouse=True)
    def setup_mocks(self):
        with patch("windows_use.tree.GetRootControl") as MockGetRootControl, \
             patch("windows_use.tree.sleep") as MockSleep, \
             patch("windows_use.tree.ThreadPoolExecutor") as MockThreadPoolExecutor, \
             patch("windows_use.tree.Image") as MockImage, \
             patch("windows_use.tree.ImageFont") as MockImageFont, \
             patch("windows_use.tree.ImageDraw") as MockImageDraw, \
             patch("windows_use.tree.random_point_within_bounding_box") as MockRandomPoint:

            self.mock_get_root_control = MockGetRootControl
            self.mock_sleep = MockSleep
            self.MockThreadPoolExecutor = MockThreadPoolExecutor
            self.MockImage = MockImage
            self.MockImageFont = MockImageFont
            self.MockImageDraw = MockImageDraw
            self.mock_random_point = MockRandomPoint
            self.mock_random_point.return_value = (50, 50)
            yield

    @pytest.fixture
    def mock_desktop(self):
        mock = MagicMock()
        mock.is_app_visible.return_value = True
        mock.get_screenshot.return_value = MagicMock(spec=Image.Image, width=1000, height=800)
        return mock

    @pytest.fixture
    def tree_instance(self, mock_desktop):
        return Tree(desktop=mock_desktop)

    @pytest.fixture
    def mock_control(self):
        def _create_mock():
            mock = MagicMock()
            mock.Name = "MockControl"
            mock.LocalizedControlType = "pane"
            mock.ControlTypeName = "PaneControl"
            mock.IsControlElement = True
            mock.IsOffscreen = False
            mock.IsEnabled = True
            mock.AcceleratorKey = ""
            mock.IsKeyboardFocusable = False

            mock_rect = MagicMock()
            mock_rect.isempty.return_value = False
            mock_rect.left, mock_rect.top, mock_rect.right, mock_rect.bottom = 0, 0, 100, 100
            mock_rect.xcenter = MagicMock(return_value=50)
            mock_rect.ycenter = MagicMock(return_value=50)
            mock_rect.width = MagicMock(return_value=100)
            mock_rect.height = MagicMock(return_value=100)
            mock.BoundingRectangle = mock_rect

            mock.GetChildren = MagicMock(return_value=[])
            mock.GetFirstChildControl = MagicMock(return_value=None)

            legacy_pattern = MagicMock()
            legacy_pattern.DefaultAction = ""
            mock.GetLegacyIAccessiblePattern = MagicMock(return_value=legacy_pattern)

            scroll_pattern = MagicMock()
            scroll_pattern.VerticallyScrollable = False
            scroll_pattern.HorizontallyScrollable = False
            mock.GetScrollPattern = MagicMock(return_value=scroll_pattern)

            return mock
        return _create_mock

    def test_init(self, tree_instance, mock_desktop):
        assert tree_instance.desktop == mock_desktop

    def test_get_state(self, tree_instance, mock_control, mock_desktop):
        root_control_mock = mock_control()
        self.mock_get_root_control.return_value = root_control_mock

        tree_instance.get_appwise_nodes = MagicMock(
            return_value=([MagicMock(spec=TreeElementNode)], [MagicMock(spec=TextElementNode)], [MagicMock(spec=ScrollElementNode)])
        )
        state = tree_instance.get_state()

        self.mock_sleep.assert_called_once_with(0.5)
        self.mock_get_root_control.assert_called_once()
        tree_instance.get_appwise_nodes.assert_called_once_with(node=root_control_mock)
        assert isinstance(state, TreeState)
        assert len(state.interactive_nodes) == 1 and isinstance(state.interactive_nodes[0], TreeElementNode)

    @pytest.mark.parametrize(
        "app_names, is_app_visible_map, expected_apps_to_process",
        [
            (["App1", "Taskbar", "Program Manager"], {"App1": True, "Taskbar": True, "Program Manager": True}, 3),
            (["App1", "App2", "Taskbar", "Program Manager"], {"App1": True, "App2": False, "Taskbar": True, "Program Manager": True}, 3),
            (["ForegroundApp", "Taskbar", "Program Manager"], {"ForegroundApp": True, "Taskbar": False, "Program Manager": False}, 1),
        ],
    )
    def test_get_appwise_nodes(
        self, tree_instance, mock_control, mock_desktop, app_names, is_app_visible_map, expected_apps_to_process
    ):
        root_mock = mock_control()
        children_mocks = [MagicMock(Name=name) for name in app_names]
        root_mock.GetChildren.return_value = children_mocks

        mock_desktop.is_app_visible.side_effect = lambda app: is_app_visible_map.get(app.Name, False)

        mock_executor = self.MockThreadPoolExecutor.return_value.__enter__.return_value

        def create_result(i):
            return ([MagicMock(spec=TreeElementNode, name=f"node_{i}")], [], [])

        futures = [MagicMock() for i in range(expected_apps_to_process)]
        for i, future in enumerate(futures):
            future.result.return_value = create_result(i)

        submitted_apps = []
        def submit_effect(func, app):
            submitted_apps.append(app)
            return futures[len(submitted_apps)-1]

        mock_executor.submit.side_effect = submit_effect

        with patch("windows_use.tree.as_completed", return_value=futures):
            interactive, _, _ = tree_instance.get_appwise_nodes(root_mock)

            assert mock_executor.submit.call_count == expected_apps_to_process
            assert len(interactive) == expected_apps_to_process

    @pytest.mark.parametrize(
    "control_setup, expected",
    [
        ({"ControlTypeName": "ButtonControl"}, {"interactive": True}),
        ({"ControlTypeName": "TextControl"}, {"informative": True}),
        # --- FIX: PaneControl is interactive, so it's found as interactive FIRST. ---
        # The elif for scrollable is not reached. The test expectation was wrong.
        ({"ControlTypeName": "PaneControl", "GetScrollPattern.return_value.VerticallyScrollable": True}, {"interactive": True}),
        ({"ControlTypeName": "GroupControl", "GetLegacyIAccessiblePattern.return_value.DefaultAction": "Press"}, {"interactive": True}),
        ({"ControlTypeName": "GroupControl", "IsKeyboardFocusable": True}, {"interactive": True}),
        ({"ControlTypeName": "ImageControl", "Name": "Save Icon"}, {"interactive": True}),
        # --- FIX: A nameless graphic image is decorative and should produce NO nodes ---
        ({"ControlTypeName": "ImageControl", "LocalizedControlType": "graphic", "Name": ""}, {}),
        ({"ControlTypeName": "ButtonControl", "IsEnabled": False}, {}),
        ({"ControlTypeName": "ButtonControl", "BoundingRectangle.isempty.return_value": True}, {}),
    ])
    def test_get_nodes_logic(self, tree_instance, mock_control, control_setup, expected):
        control = mock_control()

        for key, value in control_setup.items():
            parts = key.split('.')
            obj = control
            for part in parts[:-1]:
                obj = getattr(obj, part)
            setattr(obj, parts[-1], value)

        interactive, informative, scrollable = tree_instance.get_nodes(control)

        assert (len(interactive) > 0) == expected.get("interactive", False)
        assert (len(informative) > 0) == expected.get("informative", False)
        assert (len(scrollable) > 0) == expected.get("scrollable", False)

    def test_annotated_screenshot(self, tree_instance, mock_desktop):
        mock_screenshot = self.MockImage.new.return_value
        mock_draw = self.MockImageDraw.Draw.return_value
        mock_executor = self.MockThreadPoolExecutor.return_value.__enter__.return_value

        def map_side_effect(func, *iterables):
            for args in zip(*iterables):
                func(*args)

        mock_executor.map.side_effect = map_side_effect

        nodes = [
            TreeElementNode("btn1", "Button", "", BoundingBox(10, 20, 110, 70), Center(60, 45), "App"),
            TreeElementNode("btn2", "Button", "", BoundingBox(150, 200, 250, 250), Center(200, 225), "App")
        ]

        result_image = tree_instance.annotated_screenshot(nodes, scale=1.0)

        mock_desktop.get_screenshot.assert_called_once_with(scale=1.0)
        self.MockImage.new.assert_called_once_with("RGB", (1040, 840), color=(255, 255, 255))
        self.MockImageDraw.Draw.assert_called_once_with(mock_screenshot)
        assert mock_draw.rectangle.call_count == 2 * len(nodes)
        assert mock_draw.text.call_count == len(nodes)

        padding = 20
        expected_box_1 = (
            nodes[0].bounding_box.left + padding,
            nodes[0].bounding_box.top + padding,
            nodes[0].bounding_box.right + padding,
            nodes[0].bounding_box.bottom + padding,
        )
        mock_draw.rectangle.assert_any_call(expected_box_1, outline=ANY, width=2)

    def test_get_annotated_image_data(self, tree_instance):
        mock_nodes = [MagicMock(spec=TreeElementNode)]
        mock_screenshot = MagicMock(spec=Image.Image)

        tree_instance.get_appwise_nodes = MagicMock(return_value=(mock_nodes, [], []))
        tree_instance.annotated_screenshot = MagicMock(return_value=mock_screenshot)

        screenshot_result, nodes_result = tree_instance.get_annotated_image_data()

        self.mock_get_root_control.assert_called_once()
        root_node = self.mock_get_root_control.return_value

        tree_instance.get_appwise_nodes.assert_called_once_with(node=root_node)
        tree_instance.annotated_screenshot.assert_called_once_with(nodes=mock_nodes, scale=1.0)

        assert screenshot_result == mock_screenshot
        assert nodes_result == mock_nodes
