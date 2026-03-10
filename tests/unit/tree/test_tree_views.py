# tests/unit/tree/test_tree_views.py

import pytest
from windows_use.agent.tree.views import (
    TreeElementNode, TextElementNode, ScrollElementNode, 
    Center, BoundingBox, TreeState
)

@pytest.fixture
def sample_center():
    return Center(x=100, y=200)

@pytest.fixture
def sample_bbox():
    return BoundingBox(left=50, top=150, right=150, bottom=250, width=100, height=100)

@pytest.fixture
def sample_interactive_node(sample_bbox, sample_center):
    return TreeElementNode(
        name="Button",
        control_type="Button",
        window_name="App",
        bounding_box=sample_bbox,
        center=sample_center,
        is_focused=True
    )

@pytest.fixture
def sample_scrollable_node(sample_bbox, sample_center):
    return ScrollElementNode(
        name="Pane",
        control_type="Pane",
        window_name="App",
        xpath="/path",
        bounding_box=sample_bbox,
        center=sample_center,
        horizontal_scrollable=False,
        horizontal_scroll_percent=0.0,
        vertical_scrollable=True,
        vertical_scroll_percent=50.0,
        is_focused=False
    )

class TestTreeViews:
    def test_center(self, sample_center):
        assert sample_center.to_string() == "(100,200)"

    def test_bbox(self, sample_bbox):
        assert sample_bbox.width == 100
        assert sample_bbox.height == 100
        assert sample_bbox.xywh_to_string() == "(50,150,100,100)"

    def test_tree_state_interactive_string(self, sample_interactive_node):
        state = TreeState(interactive_nodes=[sample_interactive_node])
        s = state.interactive_elements_to_string()
        assert "0|App|Button|Button|(100,200)|True" in s
        assert "# id|window|control_type|name|coords|focus" in s

    def test_tree_state_scrollable_string(self, sample_interactive_node, sample_scrollable_node):
        state = TreeState(
            interactive_nodes=[sample_interactive_node],
            scrollable_nodes=[sample_scrollable_node]
        )
        s = state.scrollable_elements_to_string()
        # id should be 1 since there is 1 interactive node
        assert "1|App|Pane|Pane|(100,200)|False|0.0|True|50.0|False" in s
        assert "# id|window|control_type|name|coords|h_scroll|h_pct|v_scroll|v_pct|focus" in s