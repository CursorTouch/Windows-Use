# tests/unit/tree/test_tree_init.py

import pytest
from unittest.mock import MagicMock, patch
from windows_use.agent.tree.service import Tree
from windows_use.agent.tree.views import TreeState, BoundingBox
from windows_use.agent.desktop.views import Size

class TestTreeService:
    @pytest.fixture
    def mock_desktop(self):
        mock = MagicMock()
        mock.get_screen_size.return_value = Size(width=1920, height=1080)
        return mock

    @pytest.fixture
    def tree(self, mock_desktop):
        return Tree(desktop=mock_desktop)

    @patch("windows_use.agent.tree.service.GetRootControl")
    def test_init(self, mock_get_root, mock_desktop):
        tree = Tree(desktop=mock_desktop)
        assert tree.desktop == mock_desktop
        assert tree.screen_size.width == 1920
        assert tree.screen_box.width == 1920

    @patch("windows_use.agent.tree.service.ControlFromHandle")
    def test_get_nodes(self, mock_from_handle, tree):
        mock_node = MagicMock()
        mock_from_handle.return_value = mock_node
        
        # Mock tree_traversal to not actually do anything
        with patch.object(tree, 'tree_traversal') as mock_traversal:
            tree.get_nodes(handle=123)
            mock_from_handle.assert_called_once_with(123)
            assert mock_traversal.called

    @patch("windows_use.agent.tree.service.sleep")
    def test_get_state(self, mock_sleep, tree):
        # Mock get_window_wise_nodes returning 3 lists
        with patch.object(tree, 'get_window_wise_nodes') as mock_window_wise:
            mock_window_wise.return_value = ([], [], [])
            state = tree.get_state(active_window_handle=1, other_windows_handles=[2])
            
            assert isinstance(state, TreeState)
            mock_window_wise.assert_called_once_with(windows_handles=[1, 2], active_window_flag=True)
