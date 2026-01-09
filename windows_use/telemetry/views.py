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
    query: str
    steps: int
    max_steps: int
    model:str
    provider:str
    use_vision:bool=False
    answer: str | None=None
    error: str | None=None
    event_name: str = "agent_event"
    is_success:bool=False
    action_intent_confidence: float | None = None
    action_success: bool | None = None
    evidence_mismatch: bool | None = None
    rerun_count: int | None = None
    post_check_pass: bool | None = None
    
