"""
CLI-specific event subscriber for simple terminal output.
"""

from __future__ import annotations

from typing import Callable

from windows_use.agent.events.views import AgentEvent, EventType
from windows_use.agent.events.subscriber import BaseEventSubscriber
from rich.markdown import Markdown
from rich.console import Console


def _format_tool_name(tool_name: str) -> str:
    """Format tool name for display: click_tool -> Click."""
    if not tool_name:
        return ""
    name = tool_name.removesuffix("_tool") if tool_name.endswith("_tool") else tool_name
    return " ".join(word.capitalize() for word in name.split("_"))


def _truncate(text: str, max_len: int = 1_000) -> str:
    """Truncate long text with ellipsis."""
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


class CLIEventSubscriber(BaseEventSubscriber):
    def __init__(self, tts_callback: Callable[[str], None] | None = None) -> None:
        self._console = Console()
        self._pending_tool_name: str | None = None
        self._pending_tool_params: str | None = None
        self._tts_callback = tts_callback

    def invoke(self, event: AgentEvent) -> None:
        match event.type:
            case EventType.THOUGHT:
                thought = event.data.get("thought", "")
                if thought:
                    self._console.print("[bold]Thinking:[/bold]", end="")
                    self._console.print(Markdown(_truncate(thought)), end="\n")
            case EventType.TOOL_CALL:
                name = _format_tool_name(event.data.get("tool_name", ""))
                params = event.data.get("tool_params", {})
                params_str = ", ".join(f"{k}={_truncate(str(v))}" for k, v in params.items())
                self._pending_tool_name = name
                self._pending_tool_params = params_str if params_str else None
            case EventType.TOOL_RESULT:
                if self._pending_tool_name is None:
                    return
                name = self._pending_tool_name
                params_str = self._pending_tool_params
                self._pending_tool_name = None
                self._pending_tool_params = None
                if event.data.get("tool_name") == "done_tool":
                    return
                success = event.data.get("is_success", True)
                mark = "[green]✓[/green]" if success else "[red]✗[/red]"
                params_part = f"({params_str})" if params_str else "()"
                self._console.print(f"[bold]Tool:[/bold] [green]{name}[/green]{params_part} {mark}")
            case EventType.DONE:
                content = (event.data.get("content", "") or "").strip() or "No answer provided."
                self._console.print("[bold]Answer:[/bold]", Markdown(content), end="")
                if self._tts_callback and content != "No answer provided.":
                    try:
                        self._tts_callback(content)
                    except Exception:
                        pass
            case EventType.ERROR:
                err = event.data.get("error", "")
                self._console.print(f"[bold]Error:[/bold] {err}")
