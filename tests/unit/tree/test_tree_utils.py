import pytest
from unittest.mock import MagicMock, patch
import random

from windows_use.tree.utils import random_point_within_bounding_box
import uiautomation as uia

class TestTreeUtils:
    """
    Tests for utility functions in windows_use.tree.utils.
    """

    @pytest.fixture(autouse=True)
    def setup_mocks(self):
        """
        Mocks global dependencies for Tree utility tests.
        """
        with patch("windows_use.tree.utils.random") as mock_random:
            self.mock_random = mock_random
            yield

    @pytest.mark.parametrize(
        "box_width, box_height, scale_factor, expected_x_range, expected_y_range",
        [
            (100, 100, 1.0, (0, 100), (0, 100)),  # No scaling
            (100, 100, 0.5, (25, 75), (25, 75)),  # 50% scaling
            (200, 50, 0.8, (20, 180), (5, 45)),  # Rectangular box, 80% scaling
        ],
    )
    def test_random_point_within_bounding_box(
        self,
        box_width,
        box_height,
        scale_factor,
        expected_x_range,
        expected_y_range,
    ):
        """
        Test `random_point_within_bounding_box` generates points within the scaled box.

        What is being tested:
            - The generated x and y coordinates fall within the calculated scaled bounding box.
            - `random.randint` is called with the correct ranges.
        """
        mock_node = MagicMock(spec=uia.Control)
        mock_node.BoundingRectangle = MagicMock()
        mock_node.BoundingRectangle.width.return_value = box_width
        mock_node.BoundingRectangle.height.return_value = box_height
        mock_node.BoundingRectangle.left = 0
        mock_node.BoundingRectangle.top = 0

        # Mock random.randint to return values within the expected range for verification
        self.mock_random.randint.side_effect = lambda a, b: (a + b) // 2 # Return midpoint for predictability

        x, y = random_point_within_bounding_box(mock_node, scale_factor)

        scaled_width = int(box_width * scale_factor)
        scaled_height = int(box_height * scale_factor)
        scaled_left = mock_node.BoundingRectangle.left + (box_width - scaled_width) // 2
        scaled_top = mock_node.BoundingRectangle.top + (box_height - scaled_height) // 2

        assert scaled_left <= x <= scaled_left + scaled_width
        assert scaled_top <= y <= scaled_top + scaled_height

        # Verify randint calls
        self.mock_random.randint.assert_any_call(scaled_left, scaled_left + scaled_width)
        self.mock_random.randint.assert_any_call(scaled_top, scaled_top + scaled_height)
