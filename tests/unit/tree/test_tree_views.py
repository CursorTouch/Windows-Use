# tests/unit/tree/test_tree_views.py

import pytest
from unittest.mock import MagicMock

from windows_use.tree.views import TreeElementNode, TextElementNode, ScrollElementNode, Center, BoundingBox, TreeState

# --- Fixtures for creating reusable test data ---

@pytest.fixture
def sample_center():
    """Returns a sample Center object."""
    return Center(x=100, y=200)

@pytest.fixture
def sample_bounding_box():
    """Returns a sample BoundingBox object."""
    # --- FIX: Remove width and height, they are now auto-calculated ---
    return BoundingBox(left=50, top=150, right=150, bottom=250)

@pytest.fixture
def sample_interactive_node(sample_bounding_box, sample_center):
    """Returns a sample TreeElementNode (interactive node)."""
    return TreeElementNode(
        name="Click Me Button",
        control_type="Button",
        shortcut="alt+c",
        bounding_box=sample_bounding_box,
        center=sample_center,
        app_name="TestApp"
    )

@pytest.fixture
def sample_informative_node():
    """Returns a sample TextElementNode (informative node)."""
    return TextElementNode(
        name="Welcome to the App",
        app_name="TestApp"
    )

@pytest.fixture
def sample_scrollable_node(sample_bounding_box, sample_center):
    """Returns a sample ScrollElementNode."""
    return ScrollElementNode(
        name="Main Content Area",
        control_type="Pane",
        app_name="TestApp",
        bounding_box=sample_bounding_box,
        center=sample_center,
        horizontal_scrollable=False,
        vertical_scrollable=True
    )

# --- Tests for individual data classes ---

def test_center_to_string(sample_center):
    """Tests the string representation of the Center class."""
    assert sample_center.to_string() == "(100,200)"

def test_bounding_box_methods(sample_bounding_box):
    """Tests the methods of the BoundingBox class."""
    assert sample_bounding_box.width == 100
    assert sample_bounding_box.height == 100
    assert sample_bounding_box.xywh_to_string() == "(50,150,100,100)"
    assert sample_bounding_box.convert_xywh_to_xyxy() == (50, 150, 150, 250)
    assert sample_bounding_box.xyxy_to_string() == "(50,150,150,250)"

# --- Tests for the TreeState class, grouped in a test class ---

class TestTreeState:

    def test_initialization(self):
        """Tests that TreeState initializes with empty lists by default."""
        state = TreeState()
        assert state.interactive_nodes == []
        assert state.informative_nodes == []
        assert state.scrollable_nodes == []

    def test_interactive_elements_to_string_empty(self):
        """Tests interactive_elements_to_string with no nodes."""
        state = TreeState()
        assert state.interactive_elements_to_string() == ""

    def test_interactive_elements_to_string_single(self, sample_interactive_node):
        """Tests interactive_elements_to_string with a single node."""
        state = TreeState(interactive_nodes=[sample_interactive_node])
        expected_string = "Label: 0 App Name: TestApp ControlType: Button Control Name: Click Me Button Shortcut: alt+c Cordinates: (100,200)"
        assert state.interactive_elements_to_string() == expected_string

    def test_interactive_elements_to_string_multiple(self, sample_interactive_node):
        """Tests interactive_elements_to_string with multiple nodes."""
        node2 = TreeElementNode(
            name="File Menu", control_type="Menu", shortcut="",
            center=Center(x=10, y=10), bounding_box=None, app_name="TestApp"
        )
        state = TreeState(interactive_nodes=[sample_interactive_node, node2])
        expected_string = (
            "Label: 0 App Name: TestApp ControlType: Button Control Name: Click Me Button Shortcut: alt+c Cordinates: (100,200)\n"
            "Label: 1 App Name: TestApp ControlType: Menu Control Name: File Menu Shortcut:  Cordinates: (10,10)"
        )
        assert state.interactive_elements_to_string() == expected_string

    def test_informative_elements_to_string_empty(self):
        """Tests informative_elements_to_string with no nodes."""
        state = TreeState()
        assert state.informative_elements_to_string() == ""

    def test_informative_elements_to_string_multiple(self, sample_informative_node):
        """Tests informative_elements_to_string with multiple nodes."""
        node2 = TextElementNode(name="Version 1.0", app_name="TestApp")
        state = TreeState(informative_nodes=[sample_informative_node, node2])
        expected_string = (
            "App Name: TestApp Name: Welcome to the App\n"
            "App Name: TestApp Name: Version 1.0"
        )
        assert state.informative_elements_to_string() == expected_string

    def test_scrollable_elements_to_string_empty(self):
        """Tests scrollable_elements_to_string with no nodes."""
        state = TreeState()
        assert state.scrollable_elements_to_string() == ""

    def test_scrollable_elements_to_string_no_interactive_nodes(self, sample_scrollable_node):
        """Tests scrollable_elements_to_string with no interactive nodes present."""
        state = TreeState(scrollable_nodes=[sample_scrollable_node])
        expected_string = "Label: 0 App Name: TestApp ControlType: Pane Control Name: Main Content Area Cordinates: (100,200) Horizontal Scrollable: False Vertical Scrollable: True"
        assert state.scrollable_elements_to_string() == expected_string

    def test_scrollable_elements_label_offset(self, sample_interactive_node, sample_scrollable_node):
        """
        Tests that scrollable node labels are correctly offset by the number
        of interactive nodes.
        """
        state = TreeState(
            interactive_nodes=[sample_interactive_node, sample_interactive_node],
            scrollable_nodes=[sample_scrollable_node]
        )
        expected_string = "Label: 2 App Name: TestApp ControlType: Pane Control Name: Main Content Area Cordinates: (100,200) Horizontal Scrollable: False Vertical Scrollable: True"
        assert state.scrollable_elements_to_string() == expected_string