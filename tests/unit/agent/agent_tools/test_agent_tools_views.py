# tests/unit/agent/agent_tools/test_agent_tools_views.py

import pytest
from pydantic import ValidationError
from typing import Literal

from windows_use.agent.tools.views import (
    SharedBaseModel,
    Done,
    Clipboard,
    Click,
    Shell,
    Type,
    Launch,
    Scroll,
    Drag,
    Move,
    Shortcut,
    Key,
    Wait,
    Scrape,
    Switch,
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
        assert model.field1 == "value1"
        assert model.extra_field == "extra"

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

    @pytest.mark.parametrize(
        "mode, text, should_pass, error_match",
        [
            ("copy", "some text", True, None),
            ("paste", None, True, None),
            # Invalid cases based on new validator
            ("copy", None, False, "must be provided for 'copy' mode"),
            ("paste", "some text", False, "must not be provided for 'paste' mode"),
            ("invalid", "text", False, "Input should be 'copy' or 'paste'"),
        ],
    )
    def test_clipboard_model(self, mode, text, should_pass, error_match):
        """
        Test Clipboard model validation for mode and text.
        """
        if should_pass:
            # We need to construct the dict carefully to test the default `text=None`
            input_dict = {"mode": mode}
            if text is not None:
                input_dict["text"] = text
            
            clipboard = Clipboard(**input_dict)
            assert clipboard.mode == mode
            # For paste mode, text should be None even if not passed
            assert clipboard.text == text
        else:
            with pytest.raises(ValidationError, match=error_match):
                Clipboard(mode=mode, text=text)

    @pytest.mark.parametrize(
        "loc, button, clicks, should_pass",
        [
            ((10, 20), "left", 1, True),
            ((0, 0), "right", 2, True),
            ((100, 100), "middle", 0, True),
            ((10, 20, 30), "left", 1, False),  # Invalid loc tuple size
            ((10, 20), "top", 1, False),  # Invalid button
            ((10, 20), "left", 4, False),  # Invalid clicks
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
            ((10, 20), "hello", "false", "idle", True),
            ((0, 0), "world", "true", "start", True),
            ((50, 50), "test", "false", "end", True),
            ((10, 20, 30), "hello", "false", "idle", False),  # Invalid loc
            ((10, 20), "hello", "invalid", "idle", False),  # Invalid clear
            ((10, 20), "hello", "false", "invalid", False),  # Invalid caret_position
            (None, "hello", "false", "idle", False),  # Missing loc
            ((10, 20), None, "false", "idle", False),  # Missing text
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

    def test_launch_model(self):
        """
        Test Launch model validation.
        """
        launch = Launch(name="notepad")
        assert launch.name == "notepad"
        with pytest.raises(ValidationError):
            Launch(name=123)  # type: ignore
        with pytest.raises(ValidationError):
            Launch()  # type: ignore

    @pytest.mark.parametrize(
        "loc, type_val, direction, wheel_times, should_pass",
        [
            (None, "vertical", "down", 1, True),
            ((10, 20), "horizontal", "left", 5, True),
            (None, "vertical", "up", 10, True),
            (None, "invalid", "down", 1, False),  # Invalid type
            (None, "vertical", "invalid", 1, False),  # Invalid direction
            (None, "vertical", "down", -1, False),  # Invalid wheel_times (negative)
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
        "from_loc, to_loc, should_pass",
        [
            ((0, 0), (100, 100), True),
            ((10, 20), (50, 60), True),
            ((0, 0, 0), (100, 100), False),  # Invalid from_loc
            ((0, 0), (100, 100, 100), False),  # Invalid to_loc
            (None, (100, 100), False),  # Missing from_loc
            ((0, 0), None, False),  # Missing to_loc
        ],
    )
    def test_drag_model(self, from_loc, to_loc, should_pass):
        """
        Test Drag model validation for from_loc and to_loc.
        """
        if should_pass:
            drag = Drag(from_loc=from_loc, to_loc=to_loc)
            assert drag.from_loc == from_loc
            assert drag.to_loc == to_loc
        else:
            with pytest.raises(ValidationError):
                Drag(from_loc=from_loc, to_loc=to_loc)

    @pytest.mark.parametrize(
        "to_loc, should_pass",
        [
            ((100, 100), True),
            ((0, 0), True),
            ((100, 100, 100), False),  # Invalid to_loc
            (None, False),  # Missing to_loc
        ],
    )
    def test_move_model(self, to_loc, should_pass):
        """
        Test Move model validation for to_loc.
        """
        if should_pass:
            move = Move(to_loc=to_loc)
            assert move.to_loc == to_loc
        else:
            with pytest.raises(ValidationError):
                Move(to_loc=to_loc)

    @pytest.mark.parametrize(
        "shortcut, should_pass",
        [
            (["ctrl", "c"], True),
            (["alt", "f4"], True),
            ([], True),  # Empty list is valid
            ("ctrl+c", False),  # Not a list
            (["ctrl", 123], False),  # Invalid type in list
            (None, False),  # Missing shortcut
        ],
    )
    def test_shortcut_model(self, shortcut, should_pass):
        """
        Test Shortcut model validation for shortcut list.
        """
        if should_pass:
            s = Shortcut(shortcut=shortcut)
            assert s.shortcut == shortcut
        else:
            with pytest.raises(ValidationError):
                Shortcut(shortcut=shortcut)

    def test_switch_model(self):
        """
        Test Switch model validation.
        """
        switch = Switch(name="chrome")
        assert switch.name == "chrome"
        with pytest.raises(ValidationError):
            Switch(name=123)  # type: ignore
        with pytest.raises(ValidationError):
            Switch()  # type: ignore

    def test_key_model(self):
        """
        Test Key model validation.
        """
        key = Key(key="enter")
        assert key.key == "enter"
        with pytest.raises(ValidationError):
            Key(key=123)  # type: ignore
        with pytest.raises(ValidationError):
            Key()  # type: ignore

    @pytest.mark.parametrize(
        "duration, should_pass",
        [
            (5, True),
            (0, True),
            (-1, False),  # Negative duration
            (1.5, False),  # Float duration is ok for pydantic, but not for the tool, we check int here
            (None, False),  # Missing duration
        ],
    )
    def test_wait_model(self, duration, should_pass):
        """
        Test Wait model validation for duration.
        """
        if should_pass:
            wait = Wait(duration=duration)
            assert wait.duration == duration
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
