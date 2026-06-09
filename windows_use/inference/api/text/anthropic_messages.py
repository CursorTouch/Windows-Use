from __future__ import annotations
import json
from operator_use.inference.api.text.utils import parse_tool_args, anthropic_messages_to_list, anthropic_output_config, anthropic_apply_message_cache
from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any
from anthropic import AsyncAnthropic
from operator_use.inference.api.text.base import BaseLLMAPI as BaseAPI
from operator_use.inference.model.types import Model
from operator_use.inference.types import (
    LLMContext, LLMEvent, LLMOptions, StopReason, ThinkingBudgets,
    StartEvent, EndEvent, ErrorEvent,
    TextStartEvent, TextDeltaEvent, TextEndEvent,
    ThinkingStartEvent, ThinkingDeltaEvent, ThinkingEndEvent,
    ToolCallStartEvent, ToolCallDeltaEvent, ToolCallEndEvent,
)
from operator_use.message.types import (
    SystemMessage, UserMessage, AssistantMessage, ToolMessage,
    TextContent, ImageContent, ThinkingContent, ToolCallContent, ToolResultContent,
)
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from operator_use.tool.types import Tool

_STOP_REASON: dict[str, StopReason] = {
    "end_turn": StopReason.Stop,
    "max_tokens": StopReason.Length,
    "tool_use": StopReason.ToolCalls,
    "stop_sequence": StopReason.Stop,
}

_DEFAULT_MAX_TOKENS = 8096


class AnthropicMessagesAPI(BaseAPI):
    """Streaming LLM API adapter for Anthropic Messages API (API-key auth)."""

    def __init__(self, options: LLMOptions) -> None:
        """Initialise the AsyncAnthropic client with the supplied options."""
        super().__init__(options)
        self._client = AsyncAnthropic(
            api_key=options.api_key,
            base_url=options.base_url,
            default_headers=options.headers,
            max_retries=options.max_retries,
            timeout=options.timeout.total_seconds(),
        )

    def _build_params(
        self,
        model: Model,
        system: str | None,
        messages: list[dict[str, Any]],
        tools: Optional[list[Tool]] = None,
        num_ephemeral: int = 0,
    ) -> dict[str, Any]:
        """Assemble the Anthropic API request payload, including thinking and tool configs."""
        params: dict[str, Any] = {
            "model": model.id,
            "messages": anthropic_apply_message_cache(messages, skip_tail=num_ephemeral),
            "max_tokens": self.options.max_tokens or _DEFAULT_MAX_TOKENS,
            "temperature": self.options.temperature,
        }
        if system:
            params["system"] = [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
        if self.options.thinking_level is not None:
            budgets = self.options.thinking_budgets or ThinkingBudgets()
            params["thinking"] = {"type": "enabled", "budget_tokens": budgets.get(self.options.thinking_level)}

        if tools:
            tool_defs = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.schema.model_json_schema(),
                }
                for tool in tools
            ]
            # Cache the last tool definition to reduce repeated prompt-token charges.
            tool_defs[-1]["cache_control"] = {"type": "ephemeral"}
            params["tools"] = tool_defs

        return params

    async def stream(self, context: LLMContext, model: Model) -> AsyncGenerator[LLMEvent, None]:  # type: ignore[override]
        """Stream LLMEvents from the Anthropic Messages API."""
        system, anthropic_messages = anthropic_messages_to_list(context.messages)
        if context.system_prompt:
            system = context.system_prompt
        params = self._build_params(model, system, anthropic_messages, tools=context.tools or None, num_ephemeral=context.num_ephemeral)
        output_config = anthropic_output_config(context.response_format)
        if output_config is not None:
            params["output_config"] = output_config

        if self.options.on_payload:
            modified = self.options.on_payload(params)
            if modified is not None:
                params = modified

        # Per-block accumulation buffers keyed by content block index.
        block_types: dict[int, str] = {}
        tool_ids: dict[int, str] = {}
        tool_names: dict[int, str] = {}
        text_bufs: dict[int, str] = {}
        thinking_bufs: dict[int, str] = {}
        tool_bufs: dict[int, str] = {}
        _input_tokens = 0
        _output_tokens = 0
        _cache_read_tokens = 0
        _cache_write_tokens = 0

        yield StartEvent()

        async with self._client.messages.stream(**params) as stream:
            async for event in stream:
                if self._cancelled():
                    yield ErrorEvent(reason=StopReason.Abort, error="Cancelled")
                    return
                etype = event.type

                if etype == "content_block_start":
                    idx = event.index
                    block = event.content_block
                    block_types[idx] = block.type
                    if block.type == "text":
                        text_bufs[idx] = ""
                        yield TextStartEvent(text=TextContent(content=""))
                    elif block.type == "thinking":
                        thinking_bufs[idx] = ""
                        yield ThinkingStartEvent(thinking=None)
                    elif block.type == "tool_use":
                        tool_ids[idx] = block.id
                        tool_names[idx] = block.name
                        tool_bufs[idx] = ""
                        yield ToolCallStartEvent(tool_call=ToolCallContent(id=block.id, name=block.name)
                        )

                elif etype == "content_block_delta":
                    idx = event.index
                    delta = event.delta
                    if delta.type == "text_delta":
                        text_bufs[idx] = text_bufs.get(idx, "") + delta.text
                        yield TextDeltaEvent(text=TextContent(content=delta.text))
                    elif delta.type == "thinking_delta":
                        thinking_bufs[idx] = thinking_bufs.get(idx, "") + delta.thinking
                        yield ThinkingDeltaEvent(thinking=ThinkingContent(content=delta.thinking))
                    elif delta.type == "input_json_delta":
                        tool_bufs[idx] = tool_bufs.get(idx, "") + delta.partial_json
                        yield ToolCallDeltaEvent(tool_call=ToolCallContent(id=tool_ids.get(idx, ""))
                        )

                elif etype == "content_block_stop":
                    idx = event.index
                    btype = block_types.get(idx, "")
                    if btype == "text":
                        yield TextEndEvent(text=TextContent(content=text_bufs.get(idx, "")))
                    elif btype == "thinking":
                        yield ThinkingEndEvent(thinking=ThinkingContent(content=thinking_bufs.get(idx, "")))
                    elif btype == "tool_use":
                        args_str = tool_bufs.get(idx, "").strip()
                        args = parse_tool_args(args_str)

                        yield ToolCallEndEvent(tool_call=ToolCallContent(
                                id=tool_ids.get(idx, ""),
                                name=tool_names.get(idx, ""),
                                args=args
                            )
                        )

                elif etype == "message_start":
                    u = getattr(event.message, 'usage', None)
                    if u:
                        _input_tokens = getattr(u, 'input_tokens', 0) or 0
                        _cache_read_tokens = getattr(u, 'cache_read_input_tokens', 0) or 0
                        _cache_write_tokens = getattr(u, 'cache_creation_input_tokens', 0) or 0

                elif etype == "message_delta":
                    u = getattr(event, 'usage', None)
                    if u:
                        _output_tokens = getattr(u, 'output_tokens', 0) or 0
                    stop_reason = _STOP_REASON.get(event.delta.stop_reason or "", StopReason.Stop)
                    yield EndEvent(
                        reason=stop_reason,
                        input_tokens=_input_tokens,
                        output_tokens=_output_tokens,
                        cache_read_tokens=_cache_read_tokens,
                        cache_write_tokens=_cache_write_tokens,
                    )

                elif etype == "error":
                    yield ErrorEvent(reason=StopReason.Abort, error=str(event))
