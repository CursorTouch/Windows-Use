from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator, AsyncIterator
from operator_use.inference.model.types import Model
from operator_use.inference.types import LLMContext, LLMEvent, LLMOptions, Transport
from operator_use.message.types import LLMMessage


class BaseLLMAPI(ABC):
    """Abstract base for all provider-specific streaming LLM API implementations."""

    SUPPORTED_TRANSPORTS: tuple[Transport, ...] = (Transport.HTTP,)

    def __init__(self, options: LLMOptions) -> None:
        """Validate transport compatibility and store options."""
        if options.transport not in self.SUPPORTED_TRANSPORTS:
            raise ValueError(
                f"{self.__class__.__name__} does not support transport '{options.transport.value}'. "
                f"Supported: {[t.value for t in self.SUPPORTED_TRANSPORTS]}"
            )
        self.options = options

    def _cancelled(self) -> bool:
        """Return True if the caller has set the abort signal."""
        return self.options.signal is not None and self.options.signal.is_set()

    @abstractmethod
    async def stream(self, context: LLMContext, model: Model) -> AsyncGenerator[LLMEvent, None]:
        """Yield LLMEvent objects as the provider streams its response."""
        # The unreachable `yield` marks this as an async-generator signature so
        # callers (and type-checkers) treat stream() as returning an
        # AsyncGenerator — which supports aclose() — rather than a coroutine.
        raise NotImplementedError
        yield  # type: ignore[unreachable]  # pragma: no cover

    async def invoke(self, context: LLMContext, model: Model) -> list[LLMEvent]:
        """Collect all stream events into a list and return them."""
        events: list[LLMEvent] = []
        async for event in self.stream(context, model=model):
            events.append(event)
        return events


# Backward-compat alias (existing code imports BaseAPI from llm.api.base)
BaseAPI = BaseLLMAPI
