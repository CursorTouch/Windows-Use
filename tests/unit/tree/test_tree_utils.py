# tests/unit/tree/test_tree_utils.py

import pytest
from unittest.mock import MagicMock, patch
from windows_use.agent.tree.utils import random_point_within_bounding_box

class TestTreeUtils:
    @patch("windows_use.agent.tree.utils.random.randint")
    def test_random_point_within_bounding_box(self, mock_randint):
        mock_node = MagicMock()
        mock_box = MagicMock()
        mock_box.width.return_value = 100
        mock_box.height.return_value = 100
        mock_box.left = 0
        mock_box.top = 0
        mock_node.BoundingRectangle = mock_box
        
        mock_randint.side_effect = [50, 60]
        
        x, y = random_point_within_bounding_box(mock_node, scale_factor=1.0)
        
        assert x == 50
        assert y == 60
        # For 1.0 scale, range is (0, 100)
        mock_randint.assert_any_call(0, 100)
        
    @patch("windows_use.agent.tree.utils.random.randint")
    def test_random_point_within_bounding_box_scaled(self, mock_randint):
        mock_node = MagicMock()
        mock_box = MagicMock()
        mock_box.width.return_value = 100
        mock_box.height.return_value = 100
        mock_box.left = 0
        mock_box.top = 0
        mock_node.BoundingRectangle = mock_box
        
        # scale_factor = 0.5 -> scaled_width = 50, scaled_height = 50
        # scaled_left = 0 + (100 - 50) // 2 = 25
        # scaled_top = 0 + (100 - 50) // 2 = 25
        # range = (25, 25+50=75)
        
        random_point_within_bounding_box(mock_node, scale_factor=0.5)
        mock_randint.assert_any_call(25, 75)
