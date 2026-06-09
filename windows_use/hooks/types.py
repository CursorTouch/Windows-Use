from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, TYPE_CHECKING

from operator_use.subagent.types import SubagentStatus

if TYPE_CHECKING:
    from operator_use.message.types import ToolCallContent, ToolResultContent


# ============================================================================
# Session lifecycle
# ============================================================================

@dataclass
class SessionStartEvent:
    """Fired after a session has been fully loaded and is ready to accept turns."""

    type: Literal['session_start'] = field(default='session_start', init=False)
    reason: Literal['startup', 'reload', 'new', 'resume', 'fork'] = 'startup'
    previous_session_file: str | None = None


@dataclass
class SessionBeforeSwitchEvent:
    """Fired before the active session is replaced; handlers may cancel with SessionBeforeSwitchResult."""

    type: Literal['session_before_switch'] = field(default='session_before_switch', init=False)
    reason: Literal['new', 'resume'] = 'new'
    target_session_file: str | None = None


@dataclass
class SessionBeforeForkEvent:
    """Fired before a session tree branch is created; handlers may cancel with SessionBeforeForkResult."""

    type: Literal['session_before_fork'] = field(default='session_before_fork', init=False)
    entry_id: str = ''
    position: Literal['before', 'at'] = 'at'


@dataclass
class SessionBeforeCompactEvent:
    """Fired before compaction runs; handlers may cancel or replace the compaction result."""

    type: Literal['session_before_compact'] = field(default='session_before_compact', init=False)
    preparation: Any = None
    branch_entries: list[Any] = field(default_factory=list)
    custom_instructions: str | None = None


@dataclass
class SessionCompactEvent:
    """Fired after compaction completes with the resulting compaction entry."""

    type: Literal['session_compact'] = field(default='session_compact', init=False)
    compaction_entry: Any = None
    from_extension: bool = False


@dataclass
class SessionShutdownEvent:
    """Fired just before the session is torn down; last chance for cleanup."""

    type: Literal['session_shutdown'] = field(default='session_shutdown', init=False)
    reason: Literal['quit', 'reload', 'new', 'resume', 'fork'] = 'quit'
    target_session_file: str | None = None


@dataclass
class TreePreparation:
    """Computed plan for a session-tree rewrite, passed inside SessionBeforeTreeEvent."""

    target_id: str
    old_leaf_id: str | None
    common_ancestor_id: str | None
    entries_to_summarize: list[Any]
    user_wants_summary: bool = False
    custom_instructions: str | None = None
    replace_instructions: bool = False
    label: str | None = None


@dataclass
class SessionBeforeTreeEvent:
    """Fired before the session tree is restructured; handlers may mutate the preparation."""

    type: Literal['session_before_tree'] = field(default='session_before_tree', init=False)
    preparation: TreePreparation = field(default_factory=lambda: TreePreparation('', None, None, []))


@dataclass
class SessionTreeEvent:
    """Fired after the session tree has been rewritten with the new leaf information."""

    type: Literal['session_tree'] = field(default='session_tree', init=False)
    new_leaf_id: str | None = None
    old_leaf_id: str | None = None
    summary_entry: Any | None = None
    from_extension: bool = False


# ============================================================================
# Agent lifecycle
# ============================================================================

@dataclass
class ContextEvent:
    """Carries the full message history just before it is sent to the LLM; handlers may rewrite it."""

    type: Literal['context'] = field(default='context', init=False)
    messages: list[Any] = field(default_factory=list)


@dataclass
class BeforeAgentStartEvent:
    """Fired after the user prompt is known but before the engine loop begins; handlers may override the system prompt."""

    type: Literal['before_agent_start'] = field(default='before_agent_start', init=False)
    prompt: str = ''
    system_prompt: str = ''


@dataclass
class AgentStartEvent:
    """Fired when the engine loop starts processing a new user prompt."""

    type: Literal['agent_start'] = field(default='agent_start', init=False)


@dataclass
class AgentEndEvent:
    """Fired when the engine loop finishes, carrying all messages produced and the exit reason."""

    type: Literal['agent_end'] = field(default='agent_end', init=False)
    messages: list[Any] = field(default_factory=list)
    reason: Literal['completed', 'aborted', 'error'] = 'completed'


@dataclass
class AgentErrorEvent:
    """Fired when the engine loop terminates due to an unrecoverable error."""

    type: Literal['agent_error'] = field(default='agent_error', init=False)
    error: str = ''


# ============================================================================
# Subagent lifecycle
# ============================================================================

@dataclass
class SubagentStartEvent:
    """Fired when a subagent task is dispatched, before it begins executing."""

    type: Literal['subagent_start'] = field(default='subagent_start', init=False)
    task_id: str = ''
    label: str = ''
    task: str = ''


@dataclass
class SubagentEndEvent:
    """Fired when a subagent task completes, carrying its final status and result text."""

    type: Literal['subagent_end'] = field(default='subagent_end', init=False)
    task_id: str = ''
    label: str = ''
    status: SubagentStatus = SubagentStatus.completed
    result: str | None = None


# ============================================================================
# Turn lifecycle
# ============================================================================

@dataclass
class TurnStartEvent:
    """Fired at the beginning of each LLM inference turn within an agent loop."""

    type: Literal['turn_start'] = field(default='turn_start', init=False)
    turn_index: int = 0
    timestamp: float = 0.0


@dataclass
class TurnEndEvent:
    """Fired after a turn's assistant message and all tool results are available."""

    type: Literal['turn_end'] = field(default='turn_end', init=False)
    turn_index: int = 0
    message: Any = None
    tool_results: list[Any] = field(default_factory=list)


# ============================================================================
# Message lifecycle
# ============================================================================

@dataclass
class MessageStartEvent:
    """Fired when the LLM begins streaming a new assistant message."""

    type: Literal['message_start'] = field(default='message_start', init=False)
    message: Any = None


@dataclass
class MessageUpdateEvent:
    """Fired on each incremental content chunk while the assistant message streams."""

    type: Literal['message_update'] = field(default='message_update', init=False)
    message: Any = None


@dataclass
class MessageEndEvent:
    """Fired when the assistant message is fully received; handlers may replace it via MessageEndEventResult."""

    type: Literal['message_end'] = field(default='message_end', init=False)
    message: Any = None


# ============================================================================
# Tool execution
# ============================================================================

@dataclass
class ToolExecutionFailureEvent:
    """Fired when a tool raises an uncaught exception, distinct from a tool returning an error result."""

    type: Literal['tool_execution_failure'] = field(default='tool_execution_failure', init=False)
    tool_name: str = ''
    tool_call_id: str = ''
    input: dict[str, Any] = field(default_factory=dict)
    error: str = ''


@dataclass
class ToolExecutionStartEvent:
    """Fired just before a tool's execute() is called."""

    type: Literal['tool_execution_start'] = field(default='tool_execution_start', init=False)
    tool_call: ToolCallContent       # ToolCallContent


@dataclass
class ToolExecutionUpdateEvent:
    """Fired for each streaming progress update emitted by a long-running tool."""

    type: Literal['tool_execution_update'] = field(default='tool_execution_update', init=False)
    partial_tool_result: ToolResultContent     # ToolResultContent


@dataclass
class ToolExecutionEndEvent:
    """Fired after a tool's execute() returns with the final ToolResultContent."""

    type: Literal['tool_execution_end'] = field(default='tool_execution_end', init=False)
    tool_result: ToolResultContent     # ToolResultContent


@dataclass
class ToolCallEvent:
    """Fired before tool execution; handlers may block or rewrite params via ToolCallEventResult."""

    type: Literal['tool_call'] = field(default='tool_call', init=False)
    tool_call_id: str = ''
    tool_name: str = ''
    input: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResultEvent:
    """Fired after tool execution; handlers may override the result content via ToolResultEventResult."""

    type: Literal['tool_result'] = field(default='tool_result', init=False)
    tool_call_id: str = ''
    tool_name: str = ''
    input: dict[str, Any] = field(default_factory=dict)
    content: str = ''
    is_error: bool = False


# ============================================================================
# Model / thinking
# ============================================================================

@dataclass
class ModelSelectEvent:
    """Fired when the active model changes, either by user command or automatic cycling."""

    type: Literal['model_select'] = field(default='model_select', init=False)
    model: Any = None
    previous_model: Any | None = None
    source: Literal['set', 'cycle', 'restore'] = 'set'


@dataclass
class ThinkingLevelSelectEvent:
    """Fired when the extended-thinking budget level changes."""

    type: Literal['thinking_level_select'] = field(default='thinking_level_select', init=False)
    level: Any = None
    previous_level: Any = None


# ============================================================================
# Input / resources / misc
# ============================================================================

@dataclass
class InputEvent:
    """Fired when a new user message is received; handlers may transform or handle it via InputEventResult."""

    type: Literal['input'] = field(default='input', init=False)
    text: str = ''
    source: Literal['interactive', 'rpc', 'extension', 'cron', 'subagent', 'goal', 'queue', 'background'] = 'interactive'


@dataclass
class UserBashEvent:
    """Fired when a shell command is run on the user's behalf (e.g. via the bash tool)."""

    type: Literal['user_bash'] = field(default='user_bash', init=False)
    command: str = ''
    exclude_from_context: bool = False
    cwd: str = ''


@dataclass
class ResourcesDiscoverEvent:
    """Fired at startup and after reload to let extensions contribute extra skill/workflow paths."""

    type: Literal['resources_discover'] = field(default='resources_discover', init=False)
    cwd: str = ''
    reason: Literal['startup', 'reload'] = 'startup'


@dataclass
class SavePointEvent:
    """Fires after session writes are flushed — harness is idle and consistent."""
    type: Literal['save_point'] = field(default='save_point', init=False)


@dataclass
class SettledEvent:
    """Fires when the agent finishes a prompt() call with no more queued turns."""
    type: Literal['settled'] = field(default='settled', init=False)


@dataclass
class GatewayStartupEvent:
    """Fired after all enabled channels have been registered and started."""
    type: Literal['gateway:startup'] = field(default='gateway:startup', init=False)
    channel_ids: list[str] = field(default_factory=list)


@dataclass
class GatewayStopEvent:
    """Fired when the gateway is shutting down, before channel tasks are cancelled."""
    type: Literal['gateway:stop'] = field(default='gateway:stop', init=False)
    channel_ids: list[str] = field(default_factory=list)


# ============================================================================
# Provider request / response lifecycle
# ============================================================================

@dataclass
class BeforeProviderRequestEvent:
    """Fired just before the LLM API call is made."""
    type: Literal['before_provider_request'] = field(default='before_provider_request', init=False)
    model: Any = None
    messages: list[Any] = field(default_factory=list)
    options: Any = None


@dataclass
class AfterProviderResponseEvent:
    """Fired immediately after the LLM streaming response is fully collected."""
    type: Literal['after_provider_response'] = field(default='after_provider_response', init=False)
    model: Any = None
    response: Any = None  # AssistantMessage produced by the turn


@dataclass
class QueueUpdateEvent:
    """Fired when a follow-up or steering message enters the queue."""
    type: Literal['queue_update'] = field(default='queue_update', init=False)
    queue: Literal['steering', 'followup'] = 'steering'
    message: Any = None
    messages: list[Any] = field(default_factory=list)  # full queue snapshot after enqueue


# ============================================================================
# Hook result types (returned by handlers to influence behaviour)
# ============================================================================

@dataclass
class ResourcesDiscoverResult:
    """Returned by resources_discover handlers to inject additional skill and workflow directories."""

    skill_paths: list[str] = field(default_factory=list)
    workflow_paths: list[str] = field(default_factory=list)


@dataclass
class ContextEventResult:
    """Returned by context handlers to replace the message list sent to the LLM."""

    messages: list[Any] | None = None


@dataclass
class ToolCallEventResult:
    """Returned by tool_call handlers to block execution or rewrite invocation params."""

    block: bool = False
    reason: str | None = None
    params: dict[str, Any] | None = None  # non-None → rewrite the invocation params


@dataclass
class ToolResultEventResult:
    """Returned by tool_result handlers to override content, error flag, or terminate the loop."""

    content: str | None = None
    is_error: bool | None = None
    terminate: bool = False


@dataclass
class MessageEndEventResult:
    """Returned by message_end handlers to swap the final AssistantMessage before it is stored."""

    message: Any | None = None


@dataclass
class BeforeAgentStartEventResult:
    """Returned by before_agent_start handlers to override the system prompt for this turn."""

    system_prompt: str | None = None


@dataclass
class SessionBeforeSwitchResult:
    """Returned by session_before_switch handlers; cancel=True aborts the session switch."""

    cancel: bool = False


@dataclass
class SessionBeforeForkResult:
    """Returned by session_before_fork handlers; cancel=True aborts the fork."""

    cancel: bool = False


@dataclass
class SessionBeforeCompactResult:
    """Returned by session_before_compact handlers; cancel=True skips compaction, compaction overrides the result."""

    cancel: bool = False
    compaction: Any | None = None


@dataclass
class SessionBeforeTreeResult:
    """Returned by session_before_tree handlers to mutate or cancel the planned tree rewrite."""

    cancel: bool = False
    summary: dict[str, Any] | None = None
    custom_instructions: str | None = None
    replace_instructions: bool | None = None
    label: str | None = None


@dataclass
class InputEventResult:
    """Returned by input handlers; 'transform' replaces text, 'handled' suppresses normal processing."""

    action: Literal['continue', 'transform', 'handled'] = 'continue'
    text: str | None = None


# ============================================================================
# Gateway events (transport layer — channel and message lifecycle)
# ============================================================================

@dataclass
class ChannelConnectEvent:
    """Fired when a channel is registered with the gateway."""
    type: Literal['channel:connect'] = field(default='channel:connect', init=False)
    channel_id: str = ''


@dataclass
class ChannelDisconnectEvent:
    """Fired when a channel is unregistered from the gateway."""
    type: Literal['channel:disconnect'] = field(default='channel:disconnect', init=False)
    channel_id: str = ''


@dataclass
class MessageReceiveEvent:
    """
    Fired when a message arrives from a channel, before the agent processes it.
    Handlers can return MessageReceiveResult to reject or transform the message.

    `parts` carries the raw ContentPart list from the IncomingMessage (may include
    AudioPart for voice messages). STT hooks should detect AudioPart here, transcribe,
    and return MessageReceiveResult(parts=[TextPart(transcribed)]) to replace them.
    `text` is the pre-extracted text (TextParts only) for handlers that only care
    about text and don't need to touch audio.
    """
    type: Literal['message:receive'] = field(default='message:receive', init=False)
    channel_id: str = ''
    chat_id: str = ''
    user_id: str = ''
    text: str = ''
    parts: list = field(default_factory=list)  # list[ContentPart]
    stt_enabled: bool | None = None  # None = use global default; set from profile overlay


@dataclass
class MessageSendEvent:
    """
    Fired after the agent finishes, before the DONE frame is published.
    Handlers can return MessageSendResult to inject an audio (or any) part —
    used by TTS hooks to synthesize speech and send it alongside the text response.

    `is_voice` is True when the original incoming message contained an AudioPart,
    so TTS hooks can gate synthesis on whether the user spoke rather than typed.
    """
    type: Literal['message:send'] = field(default='message:send', init=False)
    channel_id: str = ''
    chat_id: str = ''
    input_text: str = ''
    response_text: str = ''
    is_voice: bool = False
    tts_enabled: bool | None = None  # None = use global default; set from profile overlay


@dataclass
class MessageCancelEvent:
    """Fired when an in-progress session is hard-cancelled."""
    type: Literal['message:cancel'] = field(default='message:cancel', init=False)
    channel_id: str = ''
    chat_id: str = ''


@dataclass
class GatewayErrorEvent:
    """Fired when an error occurs while processing a message."""
    type: Literal['gateway:error'] = field(default='gateway:error', init=False)
    channel_id: str = ''
    error: str = ''


# ============================================================================
# Union of all hook events
# ============================================================================

HookEvent = (
    SessionStartEvent
    | SessionBeforeSwitchEvent
    | SessionBeforeForkEvent
    | SessionBeforeCompactEvent
    | SessionCompactEvent
    | SessionShutdownEvent
    | SessionBeforeTreeEvent
    | SessionTreeEvent
    | ContextEvent
    | BeforeAgentStartEvent
    | AgentStartEvent
    | AgentEndEvent
    | AgentErrorEvent
    | SubagentStartEvent
    | SubagentEndEvent
    | TurnStartEvent
    | TurnEndEvent
    | MessageStartEvent
    | MessageUpdateEvent
    | MessageEndEvent
    | ToolExecutionFailureEvent
    | ToolExecutionStartEvent
    | ToolExecutionUpdateEvent
    | ToolExecutionEndEvent
    | ToolCallEvent
    | ToolResultEvent
    | ModelSelectEvent
    | ThinkingLevelSelectEvent
    | InputEvent
    | UserBashEvent
    | ResourcesDiscoverEvent
    | SavePointEvent
    | SettledEvent
    | GatewayStartupEvent
    | GatewayStopEvent
    | ChannelConnectEvent
    | ChannelDisconnectEvent
    | MessageReceiveEvent
    | MessageSendEvent
    | MessageCancelEvent
    | GatewayErrorEvent
    | BeforeProviderRequestEvent
    | AfterProviderResponseEvent
    | QueueUpdateEvent
)


# ============================================================================
# Gateway result types
# ============================================================================

@dataclass
class MessageReceiveResult:
    """
    Returned by message:receive handlers to control what happens next.

    action='continue'  — pass the message through unchanged (default).
    action='transform' — replace parts and/or text (STT: AudioPart → TextPart).
    action='reject'    — drop the message (optional `reason` sent to the channel).

    `parts` replaces the entire IncomingMessage.parts list when action='transform'.
    `text`  replaces only the extracted text string (for text-only transformations).
    """
    action: Literal['continue', 'transform', 'reject'] = 'continue'
    parts: list | None = None  # list[ContentPart] — replaces msg.parts when set
    text: str | None = None
    reason: str | None = None


@dataclass
class MessageSendResult:
    """
    Returned by message:send handlers to inject additional output parts.

    TTS hooks return AudioPart here after synthesizing speech from response_text.
    The gateway publishes these parts to the channel before the DONE frame.
    """
    parts: list | None = None  # list[ContentPart] — published to channel if set


@dataclass
class ChannelConnectResult:
    """
    Returned by channel:connect handlers.
    allow=False causes the channel to be unregistered immediately.
    """
    allow: bool = True
    reason: str | None = None
