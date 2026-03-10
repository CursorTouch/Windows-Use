"""Built-in event subscribers for agent observation.

All subscribers extend `BaseEventSubscriber` which defines the interface
for receiving agent events. Custom subscribers can subclass it to
integrate with any output target (webhooks, databases, UI, etc.).
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from windows_use.agent.events.views import AgentEvent, EventType

logger = logging.getLogger("windows_use")


def _format_tool_name(tool_name: str) -> str:
    """Format tool name for display: click_tool -> Click, multi_select_tool -> Multi Select."""
    if not tool_name:
        return ""
    name = tool_name.removesuffix("_tool") if tool_name.endswith("_tool") else tool_name
    return " ".join(word.capitalize() for word in name.split("_"))


class BaseEventSubscriber(ABC):
    """Abstract base class for agent event subscribers.

    Subclass this to create custom subscribers for any output target.

    Example:
        ```python
        class MySubscriber(BaseEventSubscriber):
            def invoke(self, event: AgentEvent) -> None:
                print(f"Event: {event}")

        agent = Agent(llm=llm, event_subscriber=MySubscriber())
        ```
    """

    @abstractmethod
    def invoke(self, event: AgentEvent) -> None:
        """Process an agent event."""
        ...

    def __call__(self, event: AgentEvent) -> None:
        """Allow the subscriber to be used as a callable."""
        self.invoke(event)


class ConsoleEventSubscriber(BaseEventSubscriber):
    """Prints agent events to the console via the standard logger.

    This is the default subscriber used when `log_to_console=True`.
    """

    def invoke(self, event: AgentEvent) -> None:
        match event.type:
            case EventType.THOUGHT:
                t = event.data.get("thought", "")
                logger.info(f"[Agent] 🧠 Thinking: {t}")
            case EventType.TOOL_CALL:
                n = _format_tool_name(event.data.get("tool_name", ""))
                p = event.data.get("tool_params", {})
                params = ", ".join(f"{k}={v}" for k, v in p.items())
                logger.info(f"[Agent] 🛠️ Tool Call: {n}({params})")
            case EventType.TOOL_RESULT:
                n = _format_tool_name(event.data.get("tool_name", ""))
                s = event.data.get("is_success", True)
                c = event.data.get("content", "")
                if not s:
                    logger.warning(f"[Agent] 🚨 Tool '{n}' failed: {c}")
                elif n != "done_tool":
                    logger.info(f"[Agent] 📃 Tool Result: {c}")
            case EventType.DONE:
                c = event.data.get("content", "")
                logger.info(f"[Agent] 📜 Final Answer: {c}")
            case EventType.ERROR:
                e = event.data.get("error", "")
                logger.error(f"[Agent] 🚨 Error: {e}")


class FileEventSubscriber(BaseEventSubscriber):
    """Writes agent events to a log file with timestamps.

    Args:
        log_path: Path to the log file.
    """

    def __init__(self, log_path: Path | None = None) -> None:
        if log_path is None:
            log_dir = Path.home() / ".windows-use" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_path = log_dir / f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        self._log_file = open(log_path, "a", encoding="utf-8")

    def invoke(self, event: AgentEvent) -> None:
        ts = datetime.now().strftime("%H:%M:%S")

        match event.type:
            case EventType.THOUGHT:
                t = event.data.get("thought", "")
                self._write(ts, f"Thought: {t}")
            case EventType.TOOL_CALL:
                n = _format_tool_name(event.data.get("tool_name", ""))
                p = event.data.get("tool_params", {})
                params = ", ".join(f"{k}={v}" for k, v in p.items())
                self._write(ts, f"Tool Call: {n}({params})")
            case EventType.TOOL_RESULT:
                n = event.data.get("tool_name", "")
                s = event.data.get("is_success", True)
                c = event.data.get("content", "")
                if n != "done_tool":
                    status = "Success" if s else "Failed"
                    self._write(ts, f"Tool Result [{status}]: {_format_tool_name(n)} -> {c}")
            case EventType.DONE:
                c = event.data.get("content", "")
                self._write(ts, f"Final Answer: {c}")
            case EventType.ERROR:
                e = event.data.get("error", "")
                self._write(ts, f"Error: {e}")

    def _write(self, ts: str, msg: str) -> None:
        self._log_file.write(f"[{ts}] {msg}\n")
        self._log_file.flush()

    def close(self) -> None:
        self._log_file.close()
