from __future__ import annotations
import json
from operator_use.inference.api.text.utils import parse_tool_args, openai_user_content, openai_response_format
from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any
from mistralai import Mistral
from mistralai.models.thinkchunk import ThinkChunk
from mistralai.models.textchunk import TextChunk
from mistralai.types import UNSET
from operator_use.inference.api.text.base import BaseLLMAPI as BaseAPI
from operator_use.inference.model.types import Model
from operator_use.inference.types import (
    LLMContext, LLMEvent, LLMOptions, StopReason, ThinkingLevel,
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
    "stop": StopReason.Stop,
    "length": StopReason.Length,
    "model_length": StopReason.Length,
    "tool_calls": StopReason.ToolCalls,
    "error": StopReason.Error,
}

_MINIMAL_LEVELS = {ThinkingLevel.Low, ThinkingLevel.Minimal}



def _messages_to_mistral(messages: list[LLMMessage]) -> list[dict[str, Any]]:
    """Convert a message list to Mistral Chat API format, preserving thinking content blocks."""
    result: list[dict[str, Any]] = []
    for msg in messages:
        match msg:
            case SystemMessage():
                text = "\n".join(c.content for c in msg.contents if isinstance(c, TextContent))
                result.append({"role": "system", "content": text})
            case UserMessage():
                result.append({"role": "user", "content": openai_user_content(msg.contents)})
            case AssistantMessage():
                text_parts: list[str] = []
                tool_calls: list[dict[str, Any]] = []
                content_chunks: list[dict[str, Any]] = []
                has_thinking = any(isinstance(c, ThinkingContent) for c in msg.contents)
                for item in msg.contents:
                    match item:
                        case ThinkingContent():
                            content_chunks.append({
                                "type": "thinking",
                                "thinking": [{"type": "text", "text": item.content}],
                                "signature": item.signature,
                            })
                        case TextContent():
                            if has_thinking:
                                content_chunks.append({"type": "text", "text": item.content})
                            else:
                                text_parts.append(item.content)
                        case ToolCallContent():
                            tool_calls.append({
                                "id": item.id,
                                "type": "function",
                                "function": {"name": item.name, "arguments": json.dumps(item.args)},
                            })
                entry: dict[str, Any] = {"role": "assistant"}
                if has_thinking:
                    # When thinking blocks are present, Mistral requires chunked content format.
                    entry["content"] = content_chunks
                else:
                    text = "".join(text_parts) or None
                    if text is not None:
                        entry["content"] = text
                if tool_calls:
                    entry["tool_calls"] = tool_calls
                result.append(entry)
            case ToolMessage():
                for content in msg.contents:
                    if isinstance(content, ToolResultContent):
                        result.append({
                            "role": "tool",
                            "tool_call_id": content.id,
                            "content": content.content,
                        })
    return result


class MistralChatAPI(BaseAPI):
    """Streaming LLM API adapter for the Mistral Chat API."""

    def __init__(self, options: LLMOptions) -> None:
        """Initialise the Mistral client and cache the initial api_key for change detection."""
        super().__init__(options)
        self._client_key = options.api_key
        self._client = self._build_client()

    def _build_client(self) -> Mistral:
        """Construct a fresh Mistral SDK client from the current options."""
        return Mistral(
            api_key=self.options.api_key,
            server_url=self.options.base_url,
            timeout_ms=int(self.options.timeout.total_seconds() * 1000),
        )

    def _sync_client(self) -> None:
        """Rebuild the Mistral client if the api_key has changed since construction."""
        # The api_key is resolved and assigned to options *after* __init__,
        # so rebuild the client whenever it changes.
        if self.options.api_key != self._client_key:
            self._client_key = self.options.api_key
            self._client = self._build_client()

    async def stream(self, context: LLMContext, model: Model) -> AsyncGenerator[LLMEvent, None]:  # type: ignore[override]
        """Stream LLMEvents from the Mistral Chat API."""
        self._sync_client()
        mistral_messages = _messages_to_mistral(context.messages)
        if context.system_prompt:
            mistral_messages = [{"role": "system", "content": context.system_prompt}] + mistral_messages

        reasoning_effort = None
        if self.options.thinking_level is not None:
            reasoning_effort = "none" if self.options.thinking_level in _MINIMAL_LEVELS else "high"

        text_started = False
        text_buf = ""
        text_index = 0
        thinking_started = False
        thinking_buf = ""
        thinking_index = 0
        tool_index = 0
        tool_started: dict[int, bool] = {}
        tool_bufs: dict[int, str] = {}
        tool_meta: dict[int, dict[str, str]] = {}
        _input_tokens = 0
        _output_tokens = 0

        yield StartEvent()

        try:
            kwargs: dict[str, Any] = {
                "model": model.id,
                "messages": mistral_messages,
                "temperature": self.options.temperature,
                "max_tokens": self.options.max_tokens,
            }
            if reasoning_effort is not None:
                kwargs["reasoning_effort"] = reasoning_effort
            response_format = openai_response_format(context.response_format)
            if response_format is not None:
                kwargs["response_format"] = response_format

            tools = context.tools or None
            if tools:
                kwargs["tools"] = [
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
                kwargs["tool_choice"] = "auto"

            if self.options.on_payload:
                modified = self.options.on_payload(kwargs)
                if modified is not None:
                    kwargs = modified

            async with await self._client.chat.stream_async(**kwargs) as stream:
                async for event in stream:
                    if self._cancelled():
                        yield ErrorEvent(reason=StopReason.Abort, error="Cancelled")
                        return
                    chunk = event.data
                    usage_data = getattr(chunk, 'usage', None)
                    if usage_data and usage_data != UNSET:
                        _input_tokens = getattr(usage_data, 'prompt_tokens', 0) or 0
                        _output_tokens = getattr(usage_data, 'completion_tokens', 0) or 0
                    if not chunk.choices:
                        continue
                    choice = chunk.choices[0]
                    delta = choice.delta

                    content = delta.content
                    if content and content !=UNSET:
                        if isinstance(content, str):
                            if not text_started:
                                yield TextStartEvent(text=TextContent(content=""))
                                text_started = True
                            text_buf += content
                            yield TextDeltaEvent(text=TextContent(content=content))
                        elif isinstance(content, list):
                            for chunk_item in content:
                                if isinstance(chunk_item, ThinkChunk):
                                    thinking_text = "".join(
                                        t.text for t in chunk_item.thinking
                                        if isinstance(t, TextChunk)
                                    )
                                    if thinking_text:
                                        if not thinking_started:
                                            yield ThinkingStartEvent(thinking=None)
                                            thinking_started = True
                                        thinking_buf += thinking_text
                                        yield ThinkingDeltaEvent(thinking=ThinkingContent(content=thinking_text))
                                    if chunk_item.closed:
                                        if thinking_started:
                                            yield ThinkingEndEvent(thinking=ThinkingContent(content=thinking_buf))
                                            thinking_index += 1
                                            thinking_started = False
                                            thinking_buf = ""
                                elif isinstance(chunk_item, TextChunk):
                                    if not text_started:
                                        yield TextStartEvent(text=TextContent(content=""))
                                        text_started = True
                                    text_buf += chunk_item.text
                                    yield TextDeltaEvent(text=TextContent(content=chunk_item.text))

                    tool_calls = delta.tool_calls
                    if tool_calls and tool_calls != UNSET:
                        for tc in tool_calls:
                            idx = tc.index if tc.index is not None else 0
                            fn = tc.function
                            args = fn.arguments if isinstance(fn.arguments, str) else json.dumps(fn.arguments)
                            tc_id = tc.id or ""
                            if idx not in tool_started:
                                tool_started[idx] = True
                                tool_bufs[idx] = ""
                                tool_meta[idx] = {"id": tc_id, "name": fn.name}
                                yield ToolCallStartEvent(tool_call=ToolCallContent(id=tc_id, name=fn.name)
                                )
                            if args:
                                tool_bufs[idx] += args
                                yield ToolCallDeltaEvent(tool_call=ToolCallContent(id=tc_id)
                                )

                    finish = choice.finish_reason
                    if finish and finish != UNSET:
                        if thinking_started:
                            yield ThinkingEndEvent(thinking=ThinkingContent(content=thinking_buf))
                            thinking_index += 1
                            thinking_started = False
                            thinking_buf = ""

                        if text_started:
                            yield TextEndEvent(text=TextContent(content=text_buf))
                            text_index += 1
                            text_started = False
                            text_buf = ""

                        for idx in sorted(tool_started):
                            args_str = tool_bufs[idx].strip()
                            args = parse_tool_args(args_str)

                            yield ToolCallEndEvent(tool_call=ToolCallContent(
                                    id=tool_meta[idx]["id"],
                                    name=tool_meta[idx]["name"],
                                    args=args
                                )
                            )
                        if tool_started:
                            tool_index += len(tool_started)
                            tool_started.clear()
                            tool_bufs.clear()
                            tool_meta.clear()

                        stop_reason = _STOP_REASON.get(str(finish), StopReason.Stop)
                        yield EndEvent(reason=stop_reason, input_tokens=_input_tokens, output_tokens=_output_tokens)

        except Exception as e:
            yield ErrorEvent(reason=StopReason.Error, error=str(e))
