from __future__ import annotations
import asyncio
import base64
import json
from operator_use.inference.api.text.utils import parse_tool_args
import re
from collections.abc import AsyncGenerator, AsyncIterator
from contextlib import aclosing
from typing import Any

import httpx
import websockets
import websockets.asyncio.client

from operator_use.inference.api.text.base import BaseLLMAPI as BaseAPI
from operator_use.inference.api.text.types import APIResponse
from operator_use.inference.model.types import Model
from operator_use.inference.types import (
    LLMContext, LLMEvent, LLMOptions, StopReason, ThinkingLevel, Transport,
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

_DEFAULT_BASE_URL = "https://chatgpt.com/backend-api"
_JWT_CLAIM_PATH = "https://api.openai.com/auth"
_MAX_RETRIES = 3
_BASE_DELAY_S = 1.0
_RETRYABLE_STATUSES = {429, 500, 502, 503, 504}
_RETRYABLE_RE = re.compile(
    r"rate.?limit|overloaded|service.?unavailable|upstream.?connect|connection.?refused", re.I
)
_COMPLETION_TYPES = {"response.done", "response.completed", "response.incomplete"}

_THINKING_EFFORT: dict[ThinkingLevel, str] = {
    ThinkingLevel.Low: "low",
    ThinkingLevel.Minimal: "low",
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


# ── Auth ──────────────────────────────────────────────────────────────────────

def _extract_account_id(token: str) -> str:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("not a JWT")
        padding = (4 - len(parts[1]) % 4) % 4
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + "=" * padding))
        account_id = payload.get(_JWT_CLAIM_PATH, {}).get("chatgpt_account_id")
        if not account_id:
            raise ValueError("missing chatgpt_account_id")
        return account_id
    except Exception as exc:
        raise ValueError(f"Failed to extract account_id from token: {exc}") from exc


# ── URL ───────────────────────────────────────────────────────────────────────

def _resolve_http_url(base_url: str | None) -> str:
    raw = (base_url or _DEFAULT_BASE_URL).rstrip("/")
    if raw.endswith("/codex/responses"):
        return raw
    if raw.endswith("/codex"):
        return f"{raw}/responses"
    return f"{raw}/codex/responses"


def _resolve_ws_url(base_url: str | None) -> str:
    http = _resolve_http_url(base_url)
    return http.replace("https://", "wss://", 1).replace("http://", "ws://", 1)


# ── Message → input conversion ────────────────────────────────────────────────

def _content_to_input(content_items: list, role: str) -> list[dict[str, Any]]:
    # The Responses API requires assistant text parts to be "output_text"
    # ("input_text" is only valid for user/input content).
    text_type = "output_text" if role == "assistant" else "input_text"
    parts: list[dict[str, Any]] = []
    for item in content_items:
        match item:
            case TextContent():
                parts.append({"type": text_type, "text": item.content})
            case ImageContent():
                for b64, mime in item.to_base64():
                    url = b64 if b64.startswith("http") else f"data:{mime or 'image/png'};base64,{b64}"
                    parts.append({"type": "input_image", "image_url": url})
    return parts


def _messages_to_input(messages: list[LLMMessage]) -> tuple[str, list[dict[str, Any]]]:
    instructions = "You are a helpful assistant."
    input_items: list[dict[str, Any]] = []

    for msg in messages:
        match msg:
            case SystemMessage():
                text = "\n".join(c.content for c in msg.contents if isinstance(c, TextContent))
                if text:
                    instructions = text
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
                parts = _content_to_input(msg.contents, role)
                if parts:
                    input_items.append({"role": role, "content": parts})
                # function_call is a top-level input item in the Responses API,
                # not nested inside a message's content array. It must precede
                # its matching function_call_output (emitted by the ToolMessage).
                for content in msg.contents:
                    if isinstance(content, ToolCallContent):
                        input_items.append({
                            "type": "function_call",
                            "call_id": content.id,
                            "name": content.name,
                            "arguments": json.dumps(content.args),
                        })

    return instructions, input_items


def _text_format(response_format: Any | None) -> dict[str, Any] | None:
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


# ── Request building ──────────────────────────────────────────────────────────

def _build_body(
    model: Model,
    instructions: str,
    input_items: list[dict[str, Any]],
    options: LLMOptions,
    tools: Optional[list[Tool]] = None,
) -> dict[str, Any]:
    effort = _THINKING_EFFORT.get(options.thinking_level, "medium") if options.thinking_level else "medium"
    body: dict[str, Any] = {
        "model": model.id,
        "store": False,
        "stream": True,
        "instructions": instructions,
        "input": input_items,
        "text": {"verbosity": "medium"},
        "include": ["reasoning.encrypted_content"],
        "reasoning": {"effort": effort, "summary": "auto"},
    }
    # NOTE: the ChatGPT Codex backend rejects `max_output_tokens`
    # ("Unsupported parameter") — unlike the standard OpenAI Responses API.
    # Output length is governed by the subscription, so we never send it.

    if tools:
        body["tools"] = [
            {
                "type": "function",
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.schema.model_json_schema(),
            }
            for tool in tools
        ]
    return body


def _build_headers(token: str, account_id: str, *, websocket: bool = False) -> dict[str, str]:
    headers: dict[str, str] = {
        "Authorization": f"Bearer {token}",
        "chatgpt-account-id": account_id,
        "originator": "codex_cli_rs",
    }
    if websocket:
        headers["OpenAI-Beta"] = "responses_websockets=2026-02-06"
    else:
        headers["OpenAI-Beta"] = "responses=experimental"
        headers["accept"] = "text/event-stream"
        headers["content-type"] = "application/json"
    return headers


# ── Codex event normalization ─────────────────────────────────────────────────

async def _map_codex_events(
    raw: AsyncIterator[dict[str, Any]],
) -> AsyncIterator[dict[str, Any]]:
    async for event in raw:
        etype = event.get("type", "")

        if etype == "error":
            code = event.get("code", "")
            message = event.get("message", "") or code or json.dumps(event)
            raise RuntimeError(f"Codex error: {message}")

        if etype == "response.failed":
            err = (event.get("response") or {}).get("error") or {}
            raise RuntimeError(err.get("message") or "Codex response failed")

        if etype in _COMPLETION_TYPES:
            yield {**event, "type": "response.completed", "response": event.get("response") or {}}
            return

        yield event


# ── SSE parsing ───────────────────────────────────────────────────────────────

async def _parse_sse(response: httpx.Response) -> AsyncIterator[dict[str, Any]]:
    buffer = ""
    async for chunk in response.aiter_text():
        buffer += chunk
        while "\n\n" in buffer:
            block, buffer = buffer.split("\n\n", 1)
            data_lines = [
                line[5:].strip()
                for line in block.splitlines()
                if line.startswith("data:")
            ]
            if not data_lines:
                continue
            data = "\n".join(data_lines).strip()
            if not data or data == "[DONE]":
                continue
            yield json.loads(data)


# ── WebSocket parsing ─────────────────────────────────────────────────────────

async def _parse_ws(ws: websockets.asyncio.client.ClientConnection) -> AsyncIterator[dict[str, Any]]:
    saw_completion = False
    async for raw in ws:
        event: dict[str, Any] = json.loads(raw)
        etype = event.get("type", "")
        if etype in _COMPLETION_TYPES:
            saw_completion = True
        yield event
        if saw_completion:
            return
    if not saw_completion:
        raise RuntimeError("WebSocket stream closed before completion event")


# ── Retry helper ──────────────────────────────────────────────────────────────

def _is_retryable(status: int, body: str) -> bool:
    return status in _RETRYABLE_STATUSES or bool(_RETRYABLE_RE.search(body))


# ── Event processing ──────────────────────────────────────────────────────────

async def _process_events(events: AsyncIterator[dict[str, Any]]) -> AsyncGenerator[LLMEvent, None]:
    # The Responses API gives a function_call output item both an `id`
    # (e.g. "fc_...") and a `call_id` (e.g. "call_..."). The subsequent
    # function_call_arguments.delta/.done events reference the item by
    # `item_id` (== item `id`), while the tool result must be paired by
    # `call_id`. Map item id -> (call_id, name) to bridge the two.
    call_id_by_item: dict[str, str] = {}
    name_by_item: dict[str, str] = {}
    # The Codex backend delivers a complete function_call as a single
    # response.output_item.done (no streamed *.arguments.delta/.done events),
    # while the standard streaming path emits them incrementally. Track which
    # call_ids have already been started/ended so the two paths don't duplicate.
    started_calls: set[str] = set()
    ended_calls: set[str] = set()
    saw_tool_call = False
    _input_tokens = 0
    _output_tokens = 0

    async for event in events:
        etype = event.get("type", "")

        if etype == "response.output_item.added":
            item = event.get("item") or {}
            itype = item.get("type", "")
            if itype == "message":
                yield TextStartEvent(text=TextContent(content=""))
            elif itype == "reasoning":
                yield ThinkingStartEvent(thinking=None)
            elif itype == "function_call":
                item_id = item.get("id", "")
                call_id = item.get("call_id", "")
                name = item.get("name", "")
                saw_tool_call = True
                call_id_by_item[item_id] = call_id
                name_by_item[item_id] = name
                started_calls.add(call_id)
                yield ToolCallStartEvent(tool_call=ToolCallContent(id=call_id, name=name)
                )

        elif etype == "response.output_text.delta":
            yield TextDeltaEvent(text=TextContent(content=event.get("delta", "")))

        elif etype == "response.output_text.done":
            yield TextEndEvent(text=TextContent(content=event.get("text", "")))

        elif etype == "response.reasoning_summary_text.delta":
            yield ThinkingDeltaEvent(thinking=ThinkingContent(content=event.get("delta", "")))

        elif etype == "response.reasoning_summary_text.done":
            yield ThinkingEndEvent(thinking=ThinkingContent(content=event.get("text", "")))

        elif etype == "response.function_call_arguments.delta":
            item_id = event.get("item_id", "")
            yield ToolCallDeltaEvent(tool_call=ToolCallContent(
                    id=call_id_by_item.get(item_id, item_id)
                )
            )

        elif etype == "response.function_call_arguments.done":
            item_id = event.get("item_id", "")
            args_str = event.get("arguments", "").strip()
            args = parse_tool_args(args_str)

            call_id = call_id_by_item.get(item_id, item_id)
            saw_tool_call = True
            ended_calls.add(call_id)
            yield ToolCallEndEvent(tool_call=ToolCallContent(
                    id=call_id,
                    name=name_by_item.get(item_id, ""),
                    args=args
                )
            )

        elif etype == "response.output_item.done":
            item = event.get("item") or {}
            if item.get("type") == "function_call":
                call_id = item.get("call_id", "")
                name = item.get("name", "")
                saw_tool_call = True
                if call_id not in ended_calls:
                    args_str = (item.get("arguments") or "").strip()
                    args = parse_tool_args(args_str)
                    if call_id not in started_calls:
                        started_calls.add(call_id)
                        yield ToolCallStartEvent(
                            tool_call=ToolCallContent(id=call_id, name=name)
                        )
                    ended_calls.add(call_id)
                    yield ToolCallEndEvent(tool_call=ToolCallContent(
                            id=call_id, name=name, args=args
                        )
                    )

        elif etype == "response.completed":
            response = event.get("response") or {}
            usage = response.get("usage") or {}
            _input_tokens = usage.get("input_tokens", 0) or 0
            _output_tokens = usage.get("output_tokens", 0) or 0
            stop_reason = _STOP_REASON.get(response.get("stop_reason") or "", StopReason.Stop)
            if saw_tool_call and stop_reason == StopReason.Stop:
                stop_reason = StopReason.ToolCalls
            yield EndEvent(reason=stop_reason, input_tokens=_input_tokens, output_tokens=_output_tokens)


# ── API class ─────────────────────────────────────────────────────────────────

class OpenAICodexResponsesAPI(BaseAPI):
    SUPPORTED_TRANSPORTS = (Transport.HTTP, Transport.WEBSOCKET)

    def __init__(self, options: LLMOptions) -> None:
        super().__init__(options)
        self._http_url = _resolve_http_url(options.base_url)
        self._ws_url = _resolve_ws_url(options.base_url)

    async def _stream_sse(
        self,
        body: dict[str, Any],
        headers: dict[str, str],
    ) -> AsyncGenerator[LLMEvent, None]:
        body_bytes = json.dumps(body).encode()
        last_error: Exception | None = None

        # Per-call client in an async-with so the connection pool is always
        # closed when the stream ends or is torn down — no persistent client
        # left unclosed for the GC to warn about.
        async with httpx.AsyncClient(
            timeout=self.options.timeout.total_seconds(),
            headers=self.options.headers or {},
        ) as client:
            for attempt in range(_MAX_RETRIES + 1):
                if attempt > 0:
                    await asyncio.sleep(_BASE_DELAY_S * (2 ** (attempt - 1)))
                try:
                    async with client.stream(
                        "POST", self._http_url, content=body_bytes, headers=headers,
                    ) as response:
                        if self.options.on_response:
                            self.options.on_response(APIResponse(response.status_code, dict(response.headers)))

                        if not response.is_success:
                            text = (await response.aread()).decode(errors="replace")
                            if attempt < _MAX_RETRIES and _is_retryable(response.status_code, text):
                                last_error = RuntimeError(f"HTTP {response.status_code}: {text}")
                                continue
                            raise RuntimeError(f"HTTP {response.status_code}: {text}")

                        async for event in _process_events(_map_codex_events(_parse_sse(response))):
                            yield event
                        return

                except RuntimeError:
                    raise
                except Exception as exc:
                    last_error = exc
                    if attempt < _MAX_RETRIES:
                        continue
                    raise

        raise last_error or RuntimeError("Failed after retries")

    async def _stream_ws(
        self,
        body: dict[str, Any],
        headers: dict[str, str],
    ) -> AsyncGenerator[LLMEvent, None]:
        ws_headers = {k: v for k, v in headers.items() if k.lower() not in ("accept", "content-type")}
        async with websockets.asyncio.client.connect(
            self._ws_url,
            additional_headers=ws_headers,
        ) as ws:
            await ws.send(json.dumps({"type": "response.create", **body}))
            async for event in _process_events(_map_codex_events(_parse_ws(ws))):
                yield event

    async def stream(self, context: LLMContext, model: Model) -> AsyncGenerator[LLMEvent, None]:  # type: ignore[override]
        token = self.options.api_key or ""
        account_id = _extract_account_id(token)
        instructions, input_items = _messages_to_input(context.messages)
        body = _build_body(model, instructions, input_items, self.options, tools=context.tools or None)
        text_format = _text_format(context.response_format)
        if text_format is not None:
            body["text"] = {**body.get("text", {}), **text_format}

        if self.options.on_payload:
            modified = self.options.on_payload(body)
            if modified is not None:
                body = modified

        yield StartEvent()

        if self.options.transport == Transport.WEBSOCKET:
            headers = _build_headers(token, account_id, websocket=True)
            stream_iter = self._stream_ws(body, headers)
        else:
            headers = _build_headers(token, account_id, websocket=False)
            stream_iter = self._stream_sse(body, headers)

        cancelled = False
        # aclosing() so breaking out on cancellation deterministically tears
        # down the inner SSE/WS stream (and its httpx/websocket connection)
        # here, instead of leaving it to the GC asyncgen finalizer
        # ("Task was destroyed but it is pending!").
        async with aclosing(stream_iter) as stream:
            async for event in stream:
                if self._cancelled():
                    cancelled = True
                    break
                yield event
        if cancelled:
            yield ErrorEvent(reason=StopReason.Abort, error="Cancelled")
