"""Hooks system: event types and service for agent lifecycle events."""

from operator_use.hooks.service import Hooks
from operator_use.hooks.types import (
    # Session lifecycle
    SessionStartEvent,
    SessionBeforeSwitchEvent,
    SessionBeforeForkEvent,
    SessionBeforeCompactEvent,
    SessionCompactEvent,
    SessionShutdownEvent,
    TreePreparation,
    SessionBeforeTreeEvent,
    SessionTreeEvent,
    # Agent lifecycle
    ContextEvent,
    BeforeAgentStartEvent,
    AgentStartEvent,
    AgentEndEvent,
    AgentErrorEvent,
    # Turn lifecycle
    TurnStartEvent,
    TurnEndEvent,
    # Message lifecycle
    MessageStartEvent,
    MessageUpdateEvent,
    MessageEndEvent,
    # Tool execution
    ToolExecutionStartEvent,
    ToolExecutionUpdateEvent,
    ToolExecutionEndEvent,
    ToolCallEvent,
    ToolResultEvent,
    # Model / thinking
    ModelSelectEvent,
    ThinkingLevelSelectEvent,
    # Input / resources / misc
    InputEvent,
    UserBashEvent,
    ResourcesDiscoverEvent,
    SavePointEvent,
    SettledEvent,
    GatewayStartupEvent,
    GatewayStopEvent,
    ChannelConnectEvent,
    ChannelDisconnectEvent,
    MessageReceiveEvent,
    MessageSendEvent,
    MessageCancelEvent,
    GatewayErrorEvent,
    # Union
    HookEvent,
    # Result types
    ResourcesDiscoverResult,
    ContextEventResult,
    ToolCallEventResult,
    ToolResultEventResult,
    MessageEndEventResult,
    BeforeAgentStartEventResult,
    SessionBeforeSwitchResult,
    SessionBeforeForkResult,
    SessionBeforeCompactResult,
    SessionBeforeTreeResult,
    InputEventResult,
    MessageReceiveResult,
    MessageSendResult,
)

__all__ = [
    'Hooks',
    # Session lifecycle
    'SessionStartEvent',
    'SessionBeforeSwitchEvent',
    'SessionBeforeForkEvent',
    'SessionBeforeCompactEvent',
    'SessionCompactEvent',
    'SessionShutdownEvent',
    'TreePreparation',
    'SessionBeforeTreeEvent',
    'SessionTreeEvent',
    # Agent lifecycle
    'ContextEvent',
    'BeforeAgentStartEvent',
    'AgentStartEvent',
    'AgentEndEvent',
    'AgentErrorEvent',
    # Turn lifecycle
    'TurnStartEvent',
    'TurnEndEvent',
    # Message lifecycle
    'MessageStartEvent',
    'MessageUpdateEvent',
    'MessageEndEvent',
    # Tool execution
    'ToolExecutionStartEvent',
    'ToolExecutionUpdateEvent',
    'ToolExecutionEndEvent',
    'ToolCallEvent',
    'ToolResultEvent',
    # Model / thinking
    'ModelSelectEvent',
    'ThinkingLevelSelectEvent',
    # Input / resources / misc
    'InputEvent',
    'UserBashEvent',
    'ResourcesDiscoverEvent',
    'SavePointEvent',
    'SettledEvent',
    'GatewayStartupEvent',
    'GatewayStopEvent',
    'ChannelConnectEvent',
    'ChannelDisconnectEvent',
    'MessageReceiveEvent',
    'MessageSendEvent',
    'MessageCancelEvent',
    'GatewayErrorEvent',
    # Union
    'HookEvent',
    # Result types
    'ResourcesDiscoverResult',
    'ContextEventResult',
    'ToolCallEventResult',
    'ToolResultEventResult',
    'MessageEndEventResult',
    'BeforeAgentStartEventResult',
    'SessionBeforeSwitchResult',
    'SessionBeforeForkResult',
    'SessionBeforeCompactResult',
    'SessionBeforeTreeResult',
    'InputEventResult',
    'MessageReceiveResult',
    'MessageSendResult',
]
