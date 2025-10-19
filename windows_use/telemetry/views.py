from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class BaseTelemetryEvent(ABC):
    @property
    @abstractmethod
    def event_name(self) -> str:
        pass

    @property
    def properties(self) -> dict[str,Any]:
        return {k: v for k, v in asdict(self).items()}
    
@dataclass
class AgentTelemetryEvent(BaseTelemetryEvent):
    task: str
    use_vision:bool
    max_steps:int
    result: str | None
    error: str | None
    actions: list[dict]|None
    event_name: str = "agent_event"
    
