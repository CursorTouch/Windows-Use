"""Agent event dataclasses."""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class EventType(str, Enum):
    """Agent event types."""

    THOUGHT = "thought"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    DONE = "done"
    ERROR = "error"


@dataclass
class AgentEvent:
    """Generic agent event with type discriminator and data dict.

    All agent events are emitted as instances of this single class.
    The `type` field discriminates the event kind, and `data` contains
    the event-specific fields (including step when applicable).

    Example:
        ```python
        event = AgentEvent(
            type=EventType.THOUGHT,
            data={"step": 0, "thought": "Let me click the button"}
        )

        match event.type:
            case EventType.THOUGHT:
                print(event.data["thought"])
        ```
    """

    type: EventType
    data: dict[str, Any]
