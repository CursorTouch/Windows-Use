# tests/unit/agent/agent_tools/test_agent_tools_views.py


import pytest
from pydantic import ValidationError

from windows_use.agent.tools.service import (
    App,
    Click,
    Desktop,
    Done,
    Memory,
    Move,
    Scrape,
    Scroll,
    Shell,
    Shortcut,
    Type,
    Wait,
)
from windows_use.agent.tools.views import SharedBaseModel

THOUGHT = "test thought"

class TestAgentToolsViews:
    """
    Tests for the Pydantic models in windows_use.agent.tools.views.
    """

    def test_shared_base_model_extra_fields(self):
        model = SharedBaseModel(thought=THOUGHT, field1="value1", extra_field="extra")
        assert getattr(model, "field1") == "value1"
        assert getattr(model, "extra_field") == "extra"

    def test_app_model(self):
        app = App(thought=THOUGHT, mode="launch", name="notepad")
        assert app.mode == "launch"
        assert app.name == "notepad"

        app_resize = App(thought=THOUGHT, mode="resize", loc=[10, 20], size=[100, 200])
        assert app_resize.mode == "resize"
        assert app_resize.loc == [10, 20]
        assert app_resize.size == [100, 200]

        with pytest.raises(ValidationError):
            App(thought=THOUGHT, mode="invalid")

    def test_done_model(self):
        done = Done(thought=THOUGHT, answer="Task completed.")
        assert done.answer == "Task completed."
        with pytest.raises(ValidationError):
            Done(thought=THOUGHT, answer=123)  # type: ignore
        with pytest.raises(ValidationError):
            Done()  # type: ignore

    def test_memory_model(self):
        mem = Memory(thought=THOUGHT, mode="write", path="test.md", content="hello")
        assert mem.mode == "write"
        assert mem.path == "test.md"
        assert mem.content == "hello"

        mem_update = Memory(thought=THOUGHT, mode="update", path="test.md", operation="replace", old_str="a", new_str="b")
        assert mem_update.operation == "replace"

        with pytest.raises(ValidationError):
            Memory(thought=THOUGHT, mode="invalid")

    @pytest.mark.parametrize(
        "loc, button, clicks, should_pass",
        [
            ([10, 20], "left", 1, True),
            ([0, 0], "right", 2, True),
            ([100, 100], "middle", 0, True),
            ([10, 20, 30], "left", 1, True),
            ([10, 20], "top", 1, False),
            ([10, 20], "left", 3, False),
            (None, "left", 1, False),
        ],
    )
    def test_click_model(self, loc, button, clicks, should_pass):
        if should_pass:
            click = Click(thought=THOUGHT, loc=loc, button=button, clicks=clicks)
            assert click.loc == loc
            assert click.button == button
            assert click.clicks == clicks
        else:
            with pytest.raises(ValidationError):
                Click(thought=THOUGHT, loc=loc, button=button, clicks=clicks)

    def test_shell_model(self):
        shell = Shell(thought=THOUGHT, command="Get-Process")
        assert shell.command == "Get-Process"
        with pytest.raises(ValidationError):
            Shell(thought=THOUGHT, command=123)  # type: ignore
        with pytest.raises(ValidationError):
            Shell()  # type: ignore

    @pytest.mark.parametrize(
        "loc, text, clear, caret_position, should_pass",
        [
            ([10, 20], "hello", False, "idle", True),
            ([0, 0], "world", True, "start", True),
            ([50, 50], "test", False, "end", True),
            ([10, 20], "hello", False, "invalid", False),
            (None, "hello", False, "idle", False),
            ([10, 20], None, False, "idle", False),
        ],
    )
    def test_type_model(self, loc, text, clear, caret_position, should_pass):
        if should_pass:
            type_obj = Type(thought=THOUGHT, loc=loc, text=text, clear=clear, caret_position=caret_position)
            assert type_obj.loc == loc
            assert type_obj.text == text
            assert type_obj.clear == clear
            assert type_obj.caret_position == caret_position
        else:
            with pytest.raises(ValidationError):
                Type(thought=THOUGHT, loc=loc, text=text, clear=clear, caret_position=caret_position)

    @pytest.mark.parametrize(
        "loc, type_val, direction, wheel_times, should_pass",
        [
            (None, "vertical", "down", 1, True),
            ([10, 20], "horizontal", "left", 5, True),
            (None, "vertical", "up", 10, True),
            (None, "invalid", "down", 1, False),
            (None, "vertical", "invalid", 1, False),
        ],
    )
    def test_scroll_model(self, loc, type_val, direction, wheel_times, should_pass):
        if should_pass:
            scroll = Scroll(thought=THOUGHT, loc=loc, type=type_val, direction=direction, wheel_times=wheel_times)
            assert scroll.loc == loc
            assert scroll.type == type_val
            assert scroll.direction == direction
            assert scroll.wheel_times == wheel_times
        else:
            with pytest.raises(ValidationError):
                Scroll(thought=THOUGHT, loc=loc, type=type_val, direction=direction, wheel_times=wheel_times)

    @pytest.mark.parametrize(
        "loc, drag, should_pass",
        [
            ([100, 100], True, True),
            ([0, 0], False, True),
            (None, False, False),
        ],
    )
    def test_move_model(self, loc, drag, should_pass):
        if should_pass:
            move = Move(thought=THOUGHT, loc=loc, drag=drag)
            assert move.loc == loc
            assert move.drag == drag
        else:
            with pytest.raises(ValidationError):
                Move(thought=THOUGHT, loc=loc, drag=drag)

    @pytest.mark.parametrize(
        "shortcut, should_pass",
        [
            ("ctrl+c", True),
            ("win", True),
            ("enter", True),
            (123, False),
            (None, False),
        ],
    )
    def test_shortcut_model(self, shortcut, should_pass):
        if should_pass:
            s = Shortcut(thought=THOUGHT, shortcut=shortcut)
            assert s.shortcut == shortcut
        else:
            with pytest.raises(ValidationError):
                Shortcut(thought=THOUGHT, shortcut=shortcut)

    @pytest.mark.parametrize(
        "duration, should_pass",
        [
            (5, True),
            (0, True),
            ("5", True),
            (None, False),
        ],
    )
    def test_wait_model(self, duration, should_pass):
        if should_pass:
            wait = Wait(thought=THOUGHT, duration=duration)
            assert wait.duration == int(duration)
        else:
            with pytest.raises(ValidationError):
                Wait(thought=THOUGHT, duration=duration)

    def test_scrape_model(self):
        scrape = Scrape(thought=THOUGHT, url="https://example.com")
        assert scrape.url == "https://example.com"
        with pytest.raises(ValidationError):
            Scrape(thought=THOUGHT, url=123)  # type: ignore
        with pytest.raises(ValidationError):
            Scrape()  # type: ignore

    def test_desktop_model(self):
        dt = Desktop(thought=THOUGHT, action="switch", desktop_name="Desktop 1")
        assert dt.action == "switch"
        assert dt.desktop_name == "Desktop 1"

        dt_create = Desktop(thought=THOUGHT, action="create")
        assert dt_create.action == "create"

        with pytest.raises(ValidationError):
            Desktop(thought=THOUGHT, action="invalid")
