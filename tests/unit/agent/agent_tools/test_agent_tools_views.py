# tests/unit/agent/agent_tools/test_agent_tools_views.py

import pytest
from pydantic import ValidationError
from typing import Literal

from windows_use.agent.tools.views import SharedBaseModel
from windows_use.agent.tools.service import (
    App,
    Done,
    Memory,
    Click,
    Shell,
    Type,
    MultiSelect,
    MultiEdit,
    Scroll,
    Move,
    Shortcut,
    Wait,
    Scrape,
    Desktop,
)

class TestAgentToolsViews:
    """
    Tests for the Pydantic models in windows_use.agent.tools.views.
    """

    def test_shared_base_model_extra_fields(self):
        """
        Test SharedBaseModel allows extra fields.
        """
        model = SharedBaseModel(field1="value1", extra_field="extra")
        assert getattr(model, "field1") == "value1"
        assert getattr(model, "extra_field") == "extra"

    def test_app_model(self):
        """
        Test App model validation.
        """
        app = App(mode="launch", name="notepad")
        assert app.mode == "launch"
        assert app.name == "notepad"
        
        # Test resize
        app_resize = App(mode="resize", loc=[10, 20], size=[100, 200])
        assert app_resize.mode == "resize"
        assert app_resize.loc == [10, 20]
        assert app_resize.size == [100, 200]

        with pytest.raises(ValidationError):
            App(mode="invalid")

    def test_done_model(self):
        """
        Test Done model validation.
        """
        done = Done(answer="Task completed.")
        assert done.answer == "Task completed."
        with pytest.raises(ValidationError):
            Done(answer=123)  # type: ignore
        with pytest.raises(ValidationError):
            Done()  # type: ignore

    def test_memory_model(self):
        """
        Test Memory model validation.
        """
        mem = Memory(mode="write", path="test.md", content="hello")
        assert mem.mode == "write"
        assert mem.path == "test.md"
        assert mem.content == "hello"

        mem_update = Memory(mode="update", path="test.md", operation="replace", old_str="a", new_str="b")
        assert mem_update.operation == "replace"
        
        with pytest.raises(ValidationError):
            Memory(mode="invalid")

    @pytest.mark.parametrize(
        "loc, button, clicks, should_pass",
        [
            ([10, 20], "left", 1, True),
            ([0, 0], "right", 2, True),
            ([100, 100], "middle", 0, True),
            ([10, 20, 30], "left", 1, True),  # list[int] doesn't enforce size in Pydantic unless specified
            ([10, 20], "top", 1, False),  # Invalid button
            ([10, 20], "left", 3, False),  # Invalid clicks (Literal[0,1,2])
            (None, "left", 1, False),  # Missing loc
        ],
    )
    def test_click_model(self, loc, button, clicks, should_pass):
        """
        Test Click model validation for loc, button, and clicks.
        """
        if should_pass:
            click = Click(loc=loc, button=button, clicks=clicks)
            assert click.loc == loc
            assert click.button == button
            assert click.clicks == clicks
        else:
            with pytest.raises(ValidationError):
                Click(loc=loc, button=button, clicks=clicks)

    def test_shell_model(self):
        """
        Test Shell model validation.
        """
        shell = Shell(command="Get-Process")
        assert shell.command == "Get-Process"
        with pytest.raises(ValidationError):
            Shell(command=123)  # type: ignore
        with pytest.raises(ValidationError):
            Shell()  # type: ignore

    @pytest.mark.parametrize(
        "loc, text, clear, caret_position, should_pass",
        [
            ([10, 20], "hello", "false", "idle", True),
            ([0, 0], "world", "true", "start", True),
            ([50, 50], "test", "false", "end", True),
            ([10, 20], "hello", "invalid", "idle", False),  # Invalid clear
            ([10, 20], "hello", "false", "invalid", False),  # Invalid caret_position
            (None, "hello", "false", "idle", False),  # Missing loc
            ([10, 20], None, "false", "idle", False),  # Missing text
        ],
    )
    def test_type_model(self, loc, text, clear, caret_position, should_pass):
        """
        Test Type model validation for loc, text, clear, and caret_position.
        """
        if should_pass:
            type_obj = Type(
                loc=loc, text=text, clear=clear, caret_position=caret_position
            )
            assert type_obj.loc == loc
            assert type_obj.text == text
            assert type_obj.clear == clear
            assert type_obj.caret_position == caret_position
        else:
            with pytest.raises(ValidationError):
                Type(loc=loc, text=text, clear=clear, caret_position=caret_position)

    @pytest.mark.parametrize(
        "loc, type_val, direction, wheel_times, should_pass",
        [
            (None, "vertical", "down", 1, True),
            ([10, 20], "horizontal", "left", 5, True),
            (None, "vertical", "up", 10, True),
            (None, "invalid", "down", 1, False),  # Invalid type
            (None, "vertical", "invalid", 1, False),  # Invalid direction
        ],
    )
    def test_scroll_model(self, loc, type_val, direction, wheel_times, should_pass):
        """
        Test Scroll model validation for loc, type, direction, and wheel_times.
        """
        if should_pass:
            scroll = Scroll(
                loc=loc, type=type_val, direction=direction, wheel_times=wheel_times
            )
            assert scroll.loc == loc
            assert scroll.type == type_val
            assert scroll.direction == direction
            assert scroll.wheel_times == wheel_times
        else:
            with pytest.raises(ValidationError):
                Scroll(
                    loc=loc, type=type_val, direction=direction, wheel_times=wheel_times
                )

    @pytest.mark.parametrize(
        "loc, drag, should_pass",
        [
            ([100, 100], True, True),
            ([0, 0], False, True),
            (None, False, False),  # Missing loc
        ],
    )
    def test_move_model(self, loc, drag, should_pass):
        """
        Test Move model validation for loc and drag.
        """
        if should_pass:
            move = Move(loc=loc, drag=drag)
            assert move.loc == loc
            assert move.drag == drag
        else:
            with pytest.raises(ValidationError):
                Move(loc=loc, drag=drag)

    @pytest.mark.parametrize(
        "shortcut, should_pass",
        [
            ("ctrl+c", True),
            ("win", True),
            ("enter", True),
            (123, False),  # Not a string
            (None, False),  # Missing shortcut
        ],
    )
    def test_shortcut_model(self, shortcut, should_pass):
        """
        Test Shortcut model validation for shortcut string.
        """
        if should_pass:
            s = Shortcut(shortcut=shortcut)
            assert s.shortcut == shortcut
        else:
            with pytest.raises(ValidationError):
                Shortcut(shortcut=shortcut)

    @pytest.mark.parametrize(
        "duration, should_pass",
        [
            (5, True),
            (0, True),
            ("5", True),  # Pydantic coerces string to int
            (None, False),  # Missing duration
        ],
    )
    def test_wait_model(self, duration, should_pass):
        """
        Test Wait model validation for duration.
        """
        if should_pass:
            wait = Wait(duration=duration)
            assert wait.duration == int(duration)
        else:
            with pytest.raises(ValidationError):
                Wait(duration=duration)

    def test_scrape_model(self):
        """
        Test Scrape model validation.
        """
        scrape = Scrape(url="https://example.com")
        assert scrape.url == "https://example.com"
        with pytest.raises(ValidationError):
            Scrape(url=123)  # type: ignore
        with pytest.raises(ValidationError):
            Scrape()  # type: ignore

    def test_desktop_model(self):
        """
        Test Desktop model validation.
        """
        dt = Desktop(action="switch", desktop_name="Desktop 1")
        assert dt.action == "switch"
        assert dt.desktop_name == "Desktop 1"
        
        dt_create = Desktop(action="create")
        assert dt_create.action == "create"
        
        with pytest.raises(ValidationError):
            Desktop(action="invalid")
