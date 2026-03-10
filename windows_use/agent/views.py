from windows_use.messages import BaseMessage
from dataclasses import dataclass, field


@dataclass
class AgentResult:
    is_done: bool = False
    content: str | None = None
    error: str | None = None


@dataclass
class AgentState:
    task: str|None = None
    messages: list[BaseMessage] = field(default_factory=list)
    error_messages: list[BaseMessage] = field(default_factory=list)
    step: int = 0
    max_steps: int = 25
    max_consecutive_failures: int = 3

    def reset(self):
        self.task = None
        self.messages.clear()
        self.error_messages.clear()
        self.step = 0
