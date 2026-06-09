"""
Google Antigravity API — SSE streaming via cloudcode-pa.googleapis.com.

Uses a Bearer token from Google OAuth to access Claude and Gemini models
through Google's Antigravity IDE quota.
"""
from __future__ import annotations

import asyncio
import json
from operator_use.inference.api.text.utils import parse_tool_args
import os
from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any, Optional, TYPE_CHECKING

import httpx

from operator_use.inference.api.text.base import BaseLLMAPI as BaseAPI
from operator_use.inference.api.text.types import APIResponse
from operator_use.inference.model.types import Model
from operator_use.inference.types import (
    LLMContext, LLMEvent, LLMOptions, StopReason,
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
if TYPE_CHECKING:
    from operator_use.tool.types import Tool

__all__ = ["GoogleAntigravityAPI"]

_SKIP_KEYS = {"title", "$schema", "$defs", "default", "prefixItems", "maxItems", "minItems", "exclusiveMinimum", "exclusiveMaximum"}


def _resolve_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Flatten Pydantic JSON schema for Gemini: resolve $ref/$defs, drop unsupported keys."""
    defs = schema.get("$defs", {})

    def _resolve(obj: Any) -> Any:
        if not isinstance(obj, dict):
            return obj if not isinstance(obj, list) else [_resolve(i) for i in obj]
        if "$ref" in obj:
            ref_name = obj["$ref"].rsplit("/", 1)[-1]
            return _resolve(defs.get(ref_name, {}))
        result: dict[str, Any] = {}
        for k, v in obj.items():
            if k in _SKIP_KEYS:
                continue
            if k == "anyOf" and isinstance(v, list):
                non_null = [_resolve(s) for s in v if s != {"type": "null"}]
                if len(non_null) == 1:
                    result.update(non_null[0])
                else:
                    result[k] = non_null
            elif isinstance(v, dict):
                result[k] = _resolve(v)
            elif isinstance(v, list):
                result[k] = [_resolve(i) for i in v]
            else:
                result[k] = v

        # Gemini requires `items` on every array type.
        # Pydantic encodes tuple[int, int] as {type: array, prefixItems: [...]}
        # which we drop above — fill in a generic integer items fallback.
        if result.get("type") == "array" and "items" not in result:
            prefix = obj.get("prefixItems")
            if prefix and isinstance(prefix, list) and len(prefix) > 0:
                # Use the type of the first element (all tuple coords are the same type)
                result["items"] = _resolve(prefix[0])
            else:
                result["items"] = {"type": "string"}

        return result

    return _resolve(schema)

_DEFAULT_BASE_URL = "https://cloudcode-pa.googleapis.com"
_STREAM_PATH = "/v1internal:streamGenerateContent?alt=sse"
_LOAD_CODE_ASSIST_PATH = "/v1internal:loadCodeAssist"
_ONBOARD_USER_PATH = "/v1internal:onboardUser"
_ANTIGRAVITY_VERSION = "1.26.0"
_FALLBACK_PROJECT_ID = "rising-fact-p41fc"

_STOP_REASON: dict[str, StopReason] = {
    "STOP": StopReason.Stop,
    "MAX_TOKENS": StopReason.Length,
    "SAFETY": StopReason.ContentFilter,
    "RECITATION": StopReason.ContentFilter,
}


def _antigravity_headers(access_token: str) -> dict[str, str]:
    platform = "WINDOWS" if os.name == "nt" else "MACOS"
    arch = "windows/amd64" if os.name == "nt" else "darwin/arm64"
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "User-Agent": f"antigravity/{_ANTIGRAVITY_VERSION} {arch}",
        "X-Goog-Api-Client": "google-cloud-sdk vscode_cloudshelleditor/0.1",
        "Client-Metadata": json.dumps(
            {"ideType": "ANTIGRAVITY", "platform": platform, "pluginType": "GEMINI"}
        ),
        "accept": "text/event-stream",
    }


_METADATA = {
    "ideType": "ANTIGRAVITY",
    "platform": "PLATFORM_UNSPECIFIED",
    "pluginType": "GEMINI",
}


def _extract_managed_project(payload: dict[str, Any]) -> Optional[str]:
    project = payload.get("cloudaicompanionProject")
    if isinstance(project, str) and project:
        return project
    if isinstance(project, dict) and isinstance(project.get("id"), str):
        return project["id"]
    return None


def _pick_default_tier(allowed: list[dict[str, Any]]) -> Optional[str]:
    for tier in allowed:
        if tier.get("isDefault") and tier.get("id"):
            return tier["id"]
    return allowed[0].get("id") if allowed else None


async def resolve_project_id(access_token: str, base_url: str = _DEFAULT_BASE_URL) -> str:
    """Resolve the user's managed Cloud Code Assist project ID.

    Calls loadCodeAssist; if no project is returned, calls onboardUser and
    polls the returned Long Running Operation until done (up to 10×5s).
    """
    headers = _antigravity_headers(access_token)

    async with httpx.AsyncClient(timeout=30.0) as client:
        load_payload: dict[str, Any] = {}
        try:
            r = await client.post(
                f"{base_url}{_LOAD_CODE_ASSIST_PATH}",
                json={"metadata": _METADATA},
                headers=headers,
            )
            if r.status_code == 200:
                load_payload = r.json()
        except Exception:
            pass

        existing = _extract_managed_project(load_payload)
        if existing:
            return existing

        tier_id = _pick_default_tier(load_payload.get("allowedTiers") or []) or "free-tier"
        body = {"tierId": tier_id, "metadata": _METADATA}

        for _ in range(10):
            try:
                r = await client.post(
                    f"{base_url}{_ONBOARD_USER_PATH}",
                    json=body,
                    headers=headers,
                )
                if r.status_code != 200:
                    break
                payload = r.json()
                if payload.get("done"):
                    resp = payload.get("response") or {}
                    project = resp.get("cloudaicompanionProject") or {}
                    proj_id = project.get("id") if isinstance(project, dict) else None
                    if proj_id:
                        return proj_id
                    break
            except Exception:
                break
            await asyncio.sleep(5)

    return _FALLBACK_PROJECT_ID


def _messages_to_contents(
    messages: list[LLMMessage],
) -> tuple[str | None, list[dict[str, Any]]]:
    system: str | None = None
    raw: list[dict[str, Any]] = []

    for msg in messages:
        match msg:
            case SystemMessage():
                system = "\n".join(c.content for c in msg.contents if isinstance(c, TextContent))
            case UserMessage():
                parts: list[dict[str, Any]] = []
                for item in msg.contents:
                    match item:
                        case TextContent():
                            parts.append({"text": item.content})
                        case ImageContent():
                            for b64, mime in item.to_base64():
                                parts.append({"inlineData": {"mimeType": mime or "image/png", "data": b64}})
                if parts:
                    raw.append({"role": "user", "parts": parts})
            case AssistantMessage():
                parts = []
                for item in msg.contents:
                    match item:
                        case TextContent():
                            parts.append({"text": item.content})
                        case ThinkingContent():
                            tp: dict[str, Any] = {"thought": True, "text": item.content}
                            if item.signature:
                                tp["thoughtSignature"] = item.signature
                            parts.append(tp)
                        case ToolCallContent():
                            fc_entry: dict[str, Any] = {
                                "functionCall": {
                                    "name": item.name,
                                    "args": item.args if isinstance(item.args, dict) else {},
                                }
                            }
                            sig = item.metadata.get("thoughtSignature") if item.metadata else None
                            if sig:
                                fc_entry["thoughtSignature"] = sig
                            parts.append(fc_entry)
                if parts:
                    raw.append({"role": "model", "parts": parts})
            case ToolMessage():
                parts = []
                for content in msg.contents:
                    if isinstance(content, ToolResultContent):
                        parts.append({
                            "functionResponse": {
                                "name": content.id,
                                "response": {"result": content.content}
                            }
                        })
                if parts:
                    raw.append({"role": "user", "parts": parts})

    # Merge consecutive same-role turns (Gemini requires strict alternation)
    contents: list[dict[str, Any]] = []
    for item in raw:
        if contents and contents[-1]["role"] == item["role"]:
            contents[-1]["parts"] = contents[-1]["parts"] + item["parts"]
        else:
            contents.append({"role": item["role"], "parts": list(item["parts"])})

    return system, contents


def _response_schema(response_format: Any | None) -> dict[str, Any] | None:
    structured = normalize_structured_response_format(response_format)
    return structured.schema if structured is not None else None


_PROVIDER_ID = "google-antigravity"
_EXTRA_PROJECT_KEY = "project_id"


def _load_cached_project_id() -> Optional[str]:
    try:
        from operator_use.inference.api.text.service import LLM
        from operator_use.auth.types import OAuthCredential as _Cred
        cred = LLM._auth_store.get(_PROVIDER_ID)
        if isinstance(cred, _Cred):
            return cred.extra.get(_EXTRA_PROJECT_KEY) or None
    except Exception:
        pass
    return None


def _persist_project_id(project_id: str) -> None:
    try:
        from operator_use.inference.api.text.service import LLM
        from operator_use.auth.types import OAuthCredential as _Cred
        cred = LLM._auth_store.get(_PROVIDER_ID)
        if isinstance(cred, _Cred) and cred.extra.get(_EXTRA_PROJECT_KEY) != project_id:
            cred.extra[_EXTRA_PROJECT_KEY] = project_id
            LLM._auth_store.set(_PROVIDER_ID, cred)
    except Exception:
        pass


class GoogleAntigravityAPI(BaseAPI):
    def __init__(self, options: LLMOptions) -> None:
        super().__init__(options)
        self._base_url = (options.base_url or _DEFAULT_BASE_URL).rstrip("/")
        self._project_id: Optional[str] = (
            (options.headers or {}).get("x-goog-user-project")
            or _load_cached_project_id()
        )

    async def _ensure_project_id(self) -> str:
        if not self._project_id:
            resolved = await resolve_project_id(
                self.options.api_key or "", self._base_url
            )
            self._project_id = resolved
            if resolved and resolved != _FALLBACK_PROJECT_ID:
                _persist_project_id(resolved)
        return self._project_id

    @staticmethod
    def _tools_to_declarations(tools: list[Tool]) -> list[dict[str, Any]]:
        """Convert Tool objects to Gemini functionDeclarations format."""
        seen: set[str] = set()
        decls = []
        for t in tools:
            if t.name in seen:
                continue
            seen.add(t.name)
            raw = t.schema.model_json_schema() if t.schema else {}
            schema = _resolve_schema(raw)
            decls.append({"name": t.name, "description": t.description or "", "parameters": schema})
        return decls

    def _build_request_body(
        self,
        model: Model,
        project: str,
        system: str | None,
        contents: list[dict[str, Any]],
        tools: Optional[list[Tool]] = None,
        response_format: Any | None = None,
    ) -> dict[str, Any]:
        generation_config: dict[str, Any] = {}
        if self.options.temperature is not None:
            generation_config["temperature"] = self.options.temperature
        if self.options.max_tokens is not None:
            generation_config["maxOutputTokens"] = self.options.max_tokens
        schema = _response_schema(response_format)
        if schema is not None:
            generation_config["responseMimeType"] = "application/json"
            generation_config["responseSchema"] = schema
        if self.options.thinking_level is not None:
            from operator_use.inference.types import ThinkingBudgets
            budgets = self.options.thinking_budgets or ThinkingBudgets()
            generation_config["thinkingConfig"] = {
                "thinkingBudget": budgets.get(self.options.thinking_level),
                "includeThoughts": True,
            }

        inner: dict[str, Any] = {"contents": contents}
        if system:
            inner["systemInstruction"] = {"parts": [{"text": system}]}
        if generation_config:
            inner["generationConfig"] = generation_config
        if tools:
            decls = self._tools_to_declarations(tools)
            if decls:
                inner["tools"] = [{"functionDeclarations": decls}]

        return {"model": model.id, "project": project, "request": inner}

    async def stream(self, context: LLMContext, model: Model) -> AsyncGenerator[LLMEvent, None]:  # type: ignore[override]
        project = await self._ensure_project_id()
        system, contents = _messages_to_contents(context.messages)
        if context.system_prompt:
            system = context.system_prompt
        body = self._build_request_body(
            model,
            project,
            system,
            contents,
            tools=context.tools or None,
            response_format=context.response_format,
        )
        headers = _antigravity_headers(self.options.api_key or "")

        if self.options.on_payload:
            modified = self.options.on_payload(body)
            if modified is not None:
                body = modified

        text_index = 0
        thinking_index = 0
        tool_index = 0
        text_started = False
        thinking_started = False
        text_buf = ""
        thinking_buf = ""
        thinking_sig = ""

        yield StartEvent()

        done = False
        try:
            async with httpx.AsyncClient(timeout=self.options.timeout.total_seconds()) as client:
                async with client.stream(
                    "POST",
                    f"{self._base_url}{_STREAM_PATH}",
                    headers=headers,
                    content=json.dumps(body),
                ) as response:
                    if self.options.on_response:
                        self.options.on_response(APIResponse(response.status_code, dict(response.headers)))

                    if not response.is_success:
                        error_body = (await response.aread()).decode(errors="replace")
                        yield ErrorEvent(reason=StopReason.Abort, error=f"HTTP {response.status_code}: {error_body}")
                        return

                    # Use aiter_bytes() directly rather than the aiter_lines →
                    # aiter_text → aiter_bytes wrapper chain: one iterator with
                    # a single explicit finally:aclose() is easier to tear down
                    # deterministically than several nested ones. Deterministic
                    # cleanup of the whole generator chain on cancellation is
                    # handled by the aclosing() wrappers at the consuming sites
                    # (engine/service.py, inference/api/text/service.py); without
                    # those, an early exit leaves this generator suspended inside
                    # the httpx context managers and defers teardown to the GC
                    # asyncgen finalizer ("Task was destroyed but it is pending!").
                    _bytes = response.aiter_bytes()
                    line_buf = ""
                    try:
                        async for chunk in _bytes:
                            if self._cancelled():
                                yield ErrorEvent(reason=StopReason.Abort, error="Cancelled")
                                done = True
                                break
                            line_buf += chunk.decode("utf-8", errors="replace")
                            while "\n" in line_buf:
                                line, line_buf = line_buf.split("\n", 1)
                                line = line.rstrip("\r")
                                if not line.startswith("data: "):
                                    continue
                                raw = line[6:].strip()
                                if not raw or raw == "[DONE]":
                                    continue

                                try:
                                    chunk_data = json.loads(raw)
                                except json.JSONDecodeError:
                                    continue

                                # API wraps the response in a "response" key
                                if "response" in chunk_data:
                                    chunk_data = chunk_data["response"]

                                candidates = chunk_data.get("candidates", [])
                                if not candidates:
                                    continue

                                candidate = candidates[0]
                                content = candidate.get("content", {})
                                for part in content.get("parts", []):
                                    if part.get("thought") and part.get("text"):
                                        if not thinking_started:
                                            yield ThinkingStartEvent(thinking=None)
                                            thinking_started = True
                                        delta = part["text"]
                                        thinking_buf += delta
                                        if part.get("thoughtSignature"):
                                            thinking_sig = part["thoughtSignature"]
                                        yield ThinkingDeltaEvent(thinking=ThinkingContent(content=delta))
                                    elif part.get("thought") and part.get("thoughtSignature") and not part.get("text"):
                                        # Gemini may send a signature-only thought part
                                        thinking_sig = part["thoughtSignature"]
                                    elif part.get("text"):
                                        if thinking_started:
                                            yield ThinkingEndEvent(thinking=ThinkingContent(content=thinking_buf, signature=thinking_sig))
                                            thinking_started = False
                                            thinking_index += 1
                                            thinking_buf = ""
                                            thinking_sig = ""
                                        if not text_started:
                                            yield TextStartEvent(text=TextContent(content=""))
                                            text_started = True
                                        delta = part["text"]
                                        text_buf += delta
                                        yield TextDeltaEvent(text=TextContent(content=delta))
                                    elif part.get("functionCall"):
                                        fc = part["functionCall"]
                                        name = fc.get("name", "") or fc.get("id", "")
                                        args_raw = fc.get("args", {})
                                        args = parse_tool_args(args_raw)
                                        call_meta: dict[str, Any] = {}
                                        part_sig = part.get("thoughtSignature")
                                        if part_sig:
                                            call_meta["thoughtSignature"] = part_sig
                                        call_id = fc.get("id") or name
                                        yield ToolCallStartEvent(tool_call=ToolCallContent(id=call_id, name=name))
                                        yield ToolCallDeltaEvent(tool_call=ToolCallContent(id=call_id))
                                        yield ToolCallEndEvent(tool_call=ToolCallContent(id=call_id, name=name, args=args, metadata=call_meta))
                                        tool_index += 1

                                finish_reason = candidate.get("finishReason", "")
                                if finish_reason and finish_reason not in ("", "FINISH_REASON_UNSPECIFIED"):
                                    if thinking_started:
                                        yield ThinkingEndEvent(thinking=ThinkingContent(content=thinking_buf, signature=thinking_sig))
                                        thinking_index += 1
                                    if text_started:
                                        yield TextEndEvent(text=TextContent(content=text_buf))
                                        text_index += 1
                                    stop = StopReason.ToolCalls if tool_index > 0 else _STOP_REASON.get(finish_reason, StopReason.Stop)
                                    yield EndEvent(reason=stop)
                                    done = True
                                    break
                            if done:
                                break
                    finally:
                        await _bytes.aclose()

        except Exception as exc:
            yield ErrorEvent(reason=StopReason.Abort, error=str(exc))
            return

        if not done:
            if thinking_started:
                yield ThinkingEndEvent(thinking=ThinkingContent(content=thinking_buf, signature=thinking_sig))
            if text_started:
                yield TextEndEvent(text=TextContent(content=text_buf))
            yield EndEvent(reason=StopReason.Stop)
