from __future__ import annotations
import json
from operator_use.inference.api.text.utils import parse_tool_args
from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any
from ollama import AsyncClient
from operator_use.inference.api.text.base import BaseLLMAPI as BaseAPI
from operator_use.inference.model.types import Model
from operator_use.inference.types import (
    LLMContext, LLMEvent, LLMOptions, StopReason, ThinkingLevel,
    StartEvent, EndEvent, ErrorEvent,
    TextStartEvent, TextDeltaEvent, TextEndEvent,
    ThinkingStartEvent, ThinkingDeltaEvent, ThinkingEndEvent,
    ToolCallStartEvent, ToolCallEndEvent,
    normalize_structured_response_format,
)
from operator_use.message.types import (
    SystemMessage, UserMessage, AssistantMessage, ToolMessage,
    TextContent, ImageContent, ThinkingContent, ToolCallContent, ToolResultContent,
)
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from operator_use.tool.types import Tool

_MINIMAL_LEVELS = {ThinkingLevel.Low, ThinkingLevel.Minimal}

_STOP_REASON: dict[str, StopReason] = {
    "stop": StopReason.Stop,
    "length": StopReason.Length,
}


def _messages_to_ollama(messages: list[LLMMessage]) -> list[dict[str, Any]]:
    """Convert a message list to Ollama Chat API format, placing images in a separate field."""
    result: list[dict[str, Any]] = []
    for msg in messages:
        match msg:
            case SystemMessage():
                text = "\n".join(c.content for c in msg.contents if isinstance(c, TextContent))
                result.append({"role": "system", "content": text})
            case UserMessage():
                text_parts: list[str] = []
                images: list[str] = []
                for item in msg.contents:
                    match item:
                        case TextContent():
                            text_parts.append(item.content)
                        case ImageContent():
                            images.extend(b64 for b64, _ in item.to_base64())
                entry: dict[str, Any] = {"role": "user", "content": "\n".join(text_parts)}
                if images:
                    entry["images"] = images
                result.append(entry)
            case AssistantMessage():
                text_parts = []
                thinking_parts: list[str] = []
                tool_calls: list[dict[str, Any]] = []
                for item in msg.contents:
                    match item:
                        case TextContent():
                            text_parts.append(item.content)
                        case ThinkingContent():
                            thinking_parts.append(item.content)
                        case ToolCallContent():
                            tool_calls.append({
                                "function": {"name": item.name, "arguments": item.args}
                            })
                entry = {"role": "assistant", "content": "\n".join(text_parts)}
                if thinking_parts:
                    entry["thinking"] = "\n".join(thinking_parts)
                if tool_calls:
                    entry["tool_calls"] = tool_calls
                result.append(entry)
            case ToolMessage():
                for content in msg.contents:
                    if isinstance(content, ToolResultContent):
                        result.append({"role": "tool", "content": content.content})

    return result


def _format(response_format: Any | None) -> dict[str, Any] | None:
    """Extract the raw JSON schema dict for Ollama's format field, or None if unstructured."""
    structured = normalize_structured_response_format(response_format)
    return structured.schema if structured is not None else None


class OllamaChatAPI(BaseAPI):
    """Streaming LLM API adapter for the Ollama Chat endpoint."""

    def __init__(self, options: LLMOptions) -> None:
        """Initialise the Ollama AsyncClient targeting the configured host."""
        super().__init__(options)
        self._client = AsyncClient(
            host=options.base_url,
            headers=options.headers or {},
            timeout=options.timeout.total_seconds(),
        )

    def _inference_options(self) -> dict[str, Any]:
        """Build Ollama model-level options dict (temperature, token limit)."""
        opts: dict[str, Any] = {"temperature": self.options.temperature}
        if self.options.max_tokens is not None:
            opts["num_predict"] = self.options.max_tokens
        return opts

    async def stream(self, context: LLMContext, model: Model) -> AsyncGenerator[LLMEvent, None]:  # type: ignore[override]
        """Stream LLMEvents from the local Ollama Chat endpoint."""
        ollama_messages = _messages_to_ollama(context.messages)
        if context.system_prompt:
            ollama_messages = [{"role": "system", "content": context.system_prompt}] + ollama_messages

        think: bool | None = None
        if self.options.thinking_level is not None:
            think = self.options.thinking_level not in _MINIMAL_LEVELS

        text_started = False
        text_buf = ""
        thinking_started = False
        thinking_buf = ""
        _input_tokens = 0
        _output_tokens = 0

        yield StartEvent()

        try:
            payload: dict[str, Any] = {
                "model": model.id,
                "messages": ollama_messages,
                "stream": True,
                "think": think,
                "options": self._inference_options(),
            }
            response_format = _format(context.response_format)
            if response_format is not None:
                payload["format"] = response_format

            tools = context.tools or None
            if tools:
                payload["tools"] = [
                    {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.schema.model_json_schema(),
                        }
                    }
                    for tool in tools
                ]

            if self.options.on_payload:
                modified = self.options.on_payload(payload)
                if modified is not None:
                    payload = modified

            async for chunk in await self._client.chat(**payload):
                if self._cancelled():
                    yield ErrorEvent(reason=StopReason.Abort, error="Cancelled")
                    return
                msg = chunk.message

                if msg.thinking:
                    if not thinking_started:
                        yield ThinkingStartEvent(thinking=None)
                        thinking_started = True
                    thinking_buf += msg.thinking
                    yield ThinkingDeltaEvent(thinking=ThinkingContent(content=msg.thinking))

                if msg.content:
                    if not text_started:
                        yield TextStartEvent(text=TextContent(content=""))
                        text_started = True
                    text_buf += msg.content
                    yield TextDeltaEvent(text=TextContent(content=msg.content))

                # Ollama sends all tool calls in the final chunk, not incrementally.
                if msg.tool_calls:
                    for i, tc in enumerate(msg.tool_calls):
                        fn = tc.function
                        args_raw = fn.arguments
                        args = parse_tool_args(args_raw)

                        yield ToolCallStartEvent(tool_call=ToolCallContent(name=fn.name))
                        yield ToolCallEndEvent(tool_call=ToolCallContent(name=fn.name, args=args))

                if chunk.done:
                    _input_tokens = getattr(chunk, 'prompt_eval_count', 0) or 0
                    _output_tokens = getattr(chunk, 'eval_count', 0) or 0
                    if thinking_started:
                        yield ThinkingEndEvent(thinking=ThinkingContent(content=thinking_buf))
                    if text_started:
                        yield TextEndEvent(text=TextContent(content=text_buf))
                    stop_reason = _STOP_REASON.get(chunk.done_reason or "", StopReason.Stop)
                    yield EndEvent(reason=stop_reason, input_tokens=_input_tokens, output_tokens=_output_tokens)

        except Exception as e:
            yield ErrorEvent(reason=StopReason.Error, error=str(e))
