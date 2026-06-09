from __future__ import annotations
import json
from operator_use.inference.api.text.utils import parse_tool_args
from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any
from openai import AsyncOpenAI
from operator_use.inference.api.text.base import BaseLLMAPI as BaseAPI
from operator_use.inference.model.types import Model
from operator_use.inference.types import (
    LLMContext, LLMEvent, LLMOptions, StopReason, ThinkingLevel,
    StartEvent, EndEvent, ErrorEvent,
    TextStartEvent, TextDeltaEvent, TextEndEvent,
    ThinkingStartEvent, ThinkingDeltaEvent, ThinkingEndEvent,
    ToolCallStartEvent, ToolCallDeltaEvent, ToolCallEndEvent,
    normalize_structured_response_format,
)
from operator_use.message.types import (
    SystemMessage, UserMessage, AssistantMessage, ToolMessage,
    TextContent, ImageContent, ThinkingContent, ToolCallContent, ToolResultContent,
)
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from operator_use.tool.types import Tool

_THINKING_EFFORT: dict[ThinkingLevel, str] = {
    ThinkingLevel.Minimal: "low",
    ThinkingLevel.Low: "low",
    ThinkingLevel.Medium: "medium",
    ThinkingLevel.High: "high",
    ThinkingLevel.XHigh: "high",
    ThinkingLevel.Max: "high",
}

_STOP_REASON: dict[str, StopReason] = {
    "stop": StopReason.Stop,
    "max_output_tokens": StopReason.Length,
    "tool_calls": StopReason.ToolCalls,
    "content_filter": StopReason.ContentFilter,
}


def _content_to_openai(content_items: list) -> list[dict[str, Any]]:
    """Convert typed message content items to OpenAI Responses API content parts."""
    parts: list[dict[str, Any]] = []
    for item in content_items:
        match item:
            case TextContent():
                parts.append({"type": "input_text", "text": item.content})
            case ImageContent():
                for b64, mime in item.to_base64():
                    url = b64 if b64.startswith("http") else f"data:{mime or 'image/png'};base64,{b64}"
                    parts.append({"type": "input_image", "image_url": url})
            case ThinkingContent():
                parts.append({
                    "type": "thinking",
                    "thinking": item.content,
                    "signature": item.signature,
                })
            case ToolCallContent():
                parts.append({
                    "type": "function_call",
                    "call_id": item.id,
                    "name": item.name,
                    "arguments": json.dumps(item.args),
                })
    return parts


def _messages_to_input(
    messages: list[LLMMessage],
) -> tuple[str | None, list[dict[str, Any]]]:
    """Convert a message list to OpenAI Responses API input items, extracting system as instructions."""
    instructions: str | None = None
    input_items: list[dict[str, Any]] = []

    for msg in messages:
        match msg:
            case SystemMessage():
                text_parts = [c.content for c in msg.contents if isinstance(c, TextContent)]
                instructions = "\n".join(text_parts)
            case ToolMessage():
                for content in msg.contents:
                    if isinstance(content, ToolResultContent):
                        input_items.append({
                            "type": "function_call_output",
                            "call_id": content.id,
                            "output": content.content,
                        })
            case UserMessage() | AssistantMessage():
                role = "user" if isinstance(msg, UserMessage) else "assistant"
                parts = _content_to_openai(msg.contents)
                if parts:
                    input_items.append({"role": role, "content": parts})

    return instructions, input_items


def _text_format(response_format: Any | None) -> dict[str, Any] | None:
    """Convert response_format to the OpenAI Responses API text.format structure."""
    structured = normalize_structured_response_format(response_format)
    if structured is None:
        return None
    return {
        "format": {
            "type": "json_schema",
            "name": structured.name,
            "schema": structured.schema,
            "strict": structured.strict,
        }
    }


class OpenAIResponsesAPI(BaseAPI):
    """Streaming LLM API adapter for the OpenAI Responses API (o-series / GPT-4o)."""

    def __init__(self, options: LLMOptions) -> None:
        """Initialise the AsyncOpenAI client with the supplied options."""
        super().__init__(options)
        self._client = AsyncOpenAI(
            api_key=options.api_key or "placeholder",
            base_url=options.base_url,
            default_headers=options.headers,
            max_retries=options.max_retries,
            timeout=options.timeout.total_seconds(),
        )

    def _build_params(self, model: Model, instructions: str | None, input_items: list, tools: Optional[list[Tool]] = None) -> dict[str, Any]:
        """Assemble the OpenAI Responses API request payload."""
        params: dict[str, Any] = {
            "model": model.id,
            "input": input_items,
            "temperature": self.options.temperature,
        }
        if instructions:
            params["instructions"] = instructions
        if self.options.max_tokens is not None:
            params["max_output_tokens"] = self.options.max_tokens
        if self.options.thinking_level is not None:
            params["reasoning"] = {"effort": _THINKING_EFFORT[self.options.thinking_level]}
        
        if tools:
            params["tools"] = [
                {
                    "type": "function",
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.schema.model_json_schema(),
                }
                for tool in tools
            ]

        return params

    async def stream(self, context: LLMContext, model: Model) -> AsyncGenerator[LLMEvent, None]:  # type: ignore[override]
        """Stream LLMEvents from the OpenAI Responses API."""
        if self.options.api_key:
            self._client.api_key = self.options.api_key
        instructions, input_items = _messages_to_input(context.messages)
        params = self._build_params(model, instructions, input_items, tools=context.tools or None)
        text_format = _text_format(context.response_format)
        if text_format is not None:
            params["text"] = text_format

        if self.options.on_payload:
            modified = self.options.on_payload(params)
            if modified is not None:
                params = modified

        tool_names: dict[str, str] = {}
        _input_tokens = 0
        _output_tokens = 0

        yield StartEvent()

        async with self._client.responses.stream(**params) as stream:
            async for event in stream:
                if self._cancelled():
                    yield ErrorEvent(reason=StopReason.Abort, error="Cancelled")
                    return
                etype = event.type

                if etype == "response.output_item.added":
                    item = event.item
                    if item.type == "message":
                        yield TextStartEvent(text=TextContent(content=""))
                    elif item.type == "reasoning":
                        yield ThinkingStartEvent(thinking=None)
                    elif item.type == "function_call":
                        tool_names[item.call_id] = item.name
                        yield ToolCallStartEvent(tool_call=ToolCallContent(id=item.call_id, name=item.name))

                elif etype == "response.output_text.delta":
                    yield TextDeltaEvent(text=TextContent(content=event.delta))

                elif etype == "response.output_text.done":
                    yield TextEndEvent(text=TextContent(content=event.text))

                elif etype == "response.reasoning_summary_text.delta":
                    yield ThinkingDeltaEvent(thinking=ThinkingContent(content=event.delta))

                elif etype == "response.reasoning_summary_text.done":
                    yield ThinkingEndEvent(thinking=ThinkingContent(content=event.text))

                elif etype == "response.function_call_arguments.delta":
                    call_id = event.item_id
                    yield ToolCallDeltaEvent(tool_call=ToolCallContent(id=call_id))

                elif etype == "response.function_call_arguments.done":
                    call_id = event.item_id
                    args_str = event.arguments.strip()
                    args = parse_tool_args(args_str)

                    yield ToolCallEndEvent(tool_call=ToolCallContent(
                        id=call_id,
                        name=tool_names.get(call_id, ""),
                        args=args
                    ))

                elif etype == "response.done":
                    resp = event.response
                    u = getattr(resp, 'usage', None)
                    if u:
                        _input_tokens = getattr(u, 'input_tokens', 0) or 0
                        _output_tokens = getattr(u, 'output_tokens', 0) or 0
                    stop_reason = _STOP_REASON.get(
                        getattr(resp, "stop_reason", None) or "",
                        StopReason.Stop,
                    )
                    yield EndEvent(reason=stop_reason, input_tokens=_input_tokens, output_tokens=_output_tokens)

                elif etype == "error":
                    yield ErrorEvent(reason=StopReason.Abort, error=str(event))
