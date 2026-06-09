from __future__ import annotations

import asyncio
import logging
import traceback
from collections import defaultdict
from typing import Any, Callable, Awaitable

from operator_use.hooks.types import HookEvent

logger = logging.getLogger(__name__)

Handler = Callable[[Any], Awaitable[Any] | Any]
Unsubscribe = Callable[[], None]


class Hooks:
    """
    Register and emit typed lifecycle hooks.

    Usage — imperative:
        hooks = Hooks()
        hooks.register('agent_start', my_handler)
        hooks.unregister('agent_start', my_handler)

    Usage — decorator:
        @hooks.on('agent_start')
        async def handle(event: AgentStartEvent) -> None:
            ...

    Usage — emit:
        results = await hooks.emit(AgentStartEvent())
    """

    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = defaultdict(list)
        self._subscribers: list[Handler] = []

    # ── Registration ──────────────────────────────────────────────────────────

    def register(self, event_type: str, handler: Handler) -> Unsubscribe:
        """Register a handler for the given event type. Returns an unsubscribe callable."""
        self._handlers[event_type].append(handler)

        def unsubscribe() -> None:
            self.unregister(event_type, handler)

        return unsubscribe

    def unregister(self, event_type: str, handler: Handler) -> None:
        """Remove a previously registered handler. No-op if not found."""
        try:
            self._handlers[event_type].remove(handler)
        except ValueError:
            pass

    def subscribe(self, listener: Handler) -> Unsubscribe:
        """
        Register a catch-all listener that receives every emitted event.
        Listener signature: (event: HookEvent) -> Awaitable | None.
        Returns an unsubscribe callable.
        """
        self._subscribers.append(listener)
        return lambda: self._subscribers.remove(listener)

    def on(self, event_type: str) -> Callable[[Handler], Handler]:
        """
        Decorator form — register a handler for an event type.

        Example:
            @hooks.on('agent_end')
            async def on_end(event: AgentEndEvent) -> None:
                print(event.messages)
        """
        def decorator(fn: Handler) -> Handler:
            self.register(event_type, fn)
            return fn

        return decorator

    # ── Emit ──────────────────────────────────────────────────────────────────

    async def emit(self, event: HookEvent) -> list[Any]:
        """
        Fire all handlers registered for event.type.

        Handlers may be sync or async. Results are collected and returned.
        Exceptions in handlers are logged but never abort the pipeline.
        """
        event_type: str = event.type  # type: ignore[attr-defined]
        handlers = list(self._handlers.get(event_type, []))
        results: list[Any] = []

        for handler in handlers:
            try:
                result = handler(event)
                if asyncio.iscoroutine(result):
                    result = await result
                results.append(result)
            except Exception:
                logger.error(
                    "Hook handler %r raised on event %r:\n%s",
                    getattr(handler, '__name__', handler),
                    event_type,
                    traceback.format_exc(),
                )

        for subscriber in list(self._subscribers):
            try:
                result = subscriber(event)
                if asyncio.iscoroutine(result):
                    await result
            except Exception:
                logger.error(
                    "Hook subscriber %r raised on event %r:\n%s",
                    getattr(subscriber, '__name__', subscriber),
                    event_type,
                    traceback.format_exc(),
                )

        return results

    # ── Introspection ─────────────────────────────────────────────────────────

    def handler_count(self, event_type: str) -> int:
        """Return the number of handlers registered for an event type."""
        return len(self._handlers.get(event_type, []))

    def registered_events(self) -> list[str]:
        """Return event types that have at least one handler."""
        return [k for k, v in self._handlers.items() if v]

    def clear(self, event_type: str | None = None) -> None:
        """Remove all handlers for a specific event type, or all events if None."""
        if event_type is None:
            self._handlers.clear()
        else:
            self._handlers.pop(event_type, None)
