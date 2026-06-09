from __future__ import annotations
from asyncio import Queue
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Awaitable, Callable, Optional
import asyncio

if TYPE_CHECKING:
    from windows_use.inference import LLM
    from windows_use.inference.types import ThinkingLevel
    from windows_use.tool.types import Tool

from windows_use.message.types import LLMMessage, AssistantMessage, ToolCallContent, ToolResultContent
from windows_use.tool.types import ToolInvocation, ToolResult, ToolExecutionMode

AbortSignal = asyncio.Event
EmitEvent = Callable[['AgentEvent'], Awaitable[None]]

class SteeringMode(str, Enum):
    OneAtATime = "one_at_a_time"
    All = "all"


class FollowupMode(str, Enum):
    OneAtATime = "one_at_a_time"
    All = "all"


class AgentEventType(str, Enum):
    AgentStart = "agent_start"
    AgentEnd = "agent_end"
    TurnStart = "turn_start"
    TurnEnd = "turn_end"
    MessageStart = "message_start"
    MessageUpdate = "message_update"
    MessageEnd = "message_end"
    ToolExecutionStart = "tool_execution_start"
    ToolExecutionUpdate = "tool_execution_update"
    ToolExecutionEnd = "tool_execution_end"
    AgentError = "agent_error"


# Hook event types — canonical definitions live in program.hooks
from windows_use.hooks.types import (
    AgentStartEvent, AgentEndEvent, AgentErrorEvent,
    TurnStartEvent, TurnEndEvent,
    MessageStartEvent, MessageUpdateEvent, MessageEndEvent,
    ToolExecutionStartEvent, ToolExecutionUpdateEvent, ToolExecutionEndEvent,
    ToolExecutionFailureEvent,
    BeforeProviderRequestEvent, AfterProviderResponseEvent, QueueUpdateEvent,
)

AgentEvent = (
    AgentStartEvent
    | AgentEndEvent
    | TurnStartEvent
    | TurnEndEvent
    | MessageStartEvent
    | MessageUpdateEvent
    | MessageEndEvent
    | ToolExecutionStartEvent
    | ToolExecutionUpdateEvent
    | ToolExecutionEndEvent
    | ToolExecutionFailureEvent
    | AgentErrorEvent
)

AfterToolCallCallback = Callable[[ToolInvocation, ToolResult, Optional[AbortSignal]], Awaitable[Optional[ToolResult]]]
BeforeToolCallCallback = Callable[[ToolInvocation, Optional[AbortSignal]], Awaitable[Optional[ToolInvocation | ToolResultContent]]]
GetFollowUpMessagesCallback = Callable[[], list[LLMMessage]]
GetSteeringMessagesCallback = Callable[[], list[LLMMessage]]
GetEphemeralMessagesCallback = Callable[[], Awaitable[list[LLMMessage]]]
OnEventCallback = Callable[['AgentEvent'], Awaitable[None]]
ShouldSkipToolCallsCallback = Callable[[ToolCallContent], ToolResultContent]
ShouldStopAfterTurnCallback = Callable[[AssistantMessage, list[ToolResultContent]], bool]
TransformContextCallback = Callable[[list[LLMMessage], Optional[AbortSignal]], list[LLMMessage]]

@dataclass
class EngineContext:
    system_prompt:Optional[str]=None
    messages:list[LLMMessage]=field(default_factory=list)
    tools:list[Tool]=field(default_factory=list)

@dataclass
class EngineState:
    """Mutable runtime state shared between the Engine loop and external observers."""
    system_prompt: Optional[str] = None
    messages: list[LLMMessage] = field(default_factory=list)
    pending_tool_calls: set[str] = field(default_factory=set)
    is_streaming: bool = False
    llm: Optional[LLM] = None
    streaming_message: Optional[AssistantMessage] = None
    thinking_level: Optional[ThinkingLevel] = None
    error_message: Optional[str] = None
    tools: list[Tool] = field(default_factory=list)
    follow_up_queue: Optional[FollowupQueue] = None
    steering_queue: Optional[SteeringQueue] = None


@dataclass
class Options:
    """Engine behaviour knobs: hooks, execution strategy, and message injection callbacks."""
    after_tool_call: Optional[AfterToolCallCallback] = None
    before_tool_call: Optional[BeforeToolCallCallback] = None
    on_event: Optional[OnEventCallback] = None
    execution_mode: Optional[ToolExecutionMode] = None
    steering_mode: SteeringMode = SteeringMode.OneAtATime
    followup_mode: FollowupMode = FollowupMode.OneAtATime
    get_follow_up_messages: Optional[GetFollowUpMessagesCallback] = None
    get_steering_messages: Optional[GetSteeringMessagesCallback] = None
    should_stop_after_turn: Optional[ShouldStopAfterTurnCallback] = None
    should_skip_tool_calls: Optional[ShouldSkipToolCallsCallback] = None
    transform_context: Optional[TransformContextCallback] = None
    get_ephemeral_messages: Optional[GetEphemeralMessagesCallback] = None


@dataclass
class _MessageQueue:
    """Async FIFO queue for steering/follow-up messages with configurable drain behaviour."""
    mode: FollowupMode | SteeringMode
    queue: Queue[LLMMessage] = field(default_factory=Queue)

    def clear(self) -> None:
        # Replace rather than drain to avoid blocking on an empty get() mid-loop.
        self.queue = Queue()

    async def enqueue(self, message: LLMMessage) -> None:
        await self.queue.put(message)

    def is_empty(self) -> bool:
        return self.queue.empty()

    def snapshot(self) -> list[LLMMessage]:
        """Return a non-destructive copy of queued messages for inspection (e.g. QueueUpdateEvent)."""
        return list(self.queue._queue)  # type: ignore[attr-defined]

    async def dequeue(self) -> list[LLMMessage]:
        """Drain one (OneAtATime) or all (All) messages from the queue."""
        messages: list[LLMMessage] = []
        if self.mode.value == "one_at_a_time":
            if not self.is_empty():
                messages.append(await self.queue.get())
        else:
            while not self.is_empty():
                messages.append(await self.queue.get())
        return messages


@dataclass
class FollowupQueue(_MessageQueue):
    mode: FollowupMode  # type: ignore[assignment]


@dataclass
class SteeringQueue(_MessageQueue):
    mode: SteeringMode  # type: ignore[assignment]


