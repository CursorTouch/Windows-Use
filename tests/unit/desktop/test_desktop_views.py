# tests/unit/desktop/test_desktop_views.py

import pytest
from windows_use.agent.desktop.views import Window, DesktopState, Status, Size
from windows_use.agent.tree.views import BoundingBox

@pytest.fixture
def sample_window():
    return Window(
        name="Notepad",
        is_browser=False,
        depth=0,
        status=Status.NORMAL,
        bounding_box=BoundingBox(0, 0, 100, 100, 100, 100),
        handle=123,
        process_id=456
    )

class TestDesktopViews:
    def test_window_to_row(self, sample_window):
        row = sample_window.to_row()
        assert row == ["Notepad", 0, "Normal", 100, 100, 123]

    def test_size(self):
        size = Size(1920, 1080)
        assert size.to_string() == "(1920,1080)"

    def test_desktop_state_strings(self, sample_window):
        state = DesktopState(
            active_desktop={"name": "Desktop 1"},
            all_desktops=[{"name": "Desktop 1"}, {"name": "Desktop 2"}],
            windows=[sample_window],
            active_window=sample_window
        )
        
        assert "Desktop 1" in state.active_desktop_to_string()
        assert "Desktop 2" in state.desktops_to_string()
        assert "Notepad" in state.active_window_to_string()
        assert "Notepad" in state.windows_to_string()
        
        # Test tabulate output roughly
        assert "Name" in state.windows_to_string()
        assert "Handle" in state.windows_to_string()
