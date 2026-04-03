import os
import json
import logging
from typing import Optional, Any, List, Iterator, AsyncIterator

import httpx
from pydantic import BaseModel

from windows_use.providers.base import BaseChatLLM
from windows_use.providers.views import TokenUsage, Metadata
from windows_use.providers.events import LLMEvent, LLMEventType, LLMStreamEvent, LLMStreamEventType, ToolCall
from windows_use.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ImageMessage, ToolMessage
from windows_use.tools import Tool
from windows_use.providers.perplexity.view import get_model_info

logger = logging.getLogger(__name__)


class ChatPerplexity:
    """
    Perplexity LLM implementation using the Perplexity Agent API (/v1/agent).

    This uses the Responses API format — NOT OpenAI Chat Completions.
    Supports tool/function calling, vision, and reasoning models.

    Supported models include Perplexity's own Sonar family plus
    third-party models via the Agent API (GPT, Gemini, Claude).
    """

    def __init__(
        self,
        model: str = "sonar-pro",
        api_key: Optional[str] = None,
        base_url: str = "https://api.perplexity.ai",
        timeout: float = 600.0,
        temperature: float = 0.5,
        max_output_tokens: int = 16000,
        **kwargs: Any,
    ):
        self._model = model
        self._model_info = get_model_info(model)
        self._api_model = self._model_info["api_name"]
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.api_key = api_key or os.environ.get("PERPLEXITY_API_KEY")
        if not self.api_key:
            logger.warning("No Perplexity API key found. Set PERPLEXITY_API_KEY.")
            self.api_key = "missing_key"

        self._client = httpx.Client(timeout=timeout)
        self._aclient = httpx.AsyncClient(timeout=timeout)

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def provider(self) -> str:
        return "perplexity"

    # ── Message conversion ──────────────────────────────────────────

    def _convert_messages(self, messages: list[BaseMessage]) -> tuple[Optional[str], list[dict]]:
        """Convert internal messages to Perplexity Agent API format.

        Returns (instructions, input_messages).
        System messages become `instructions`; others go into `input`.
        """
        instructions = None
        input_msgs: list[dict] = []

        for msg in messages:
            if isinstance(msg, SystemMessage):
                instructions = msg.content

            elif isinstance(msg, ImageMessage):
                content_parts: list[dict] = []
                if msg.content:
                    content_parts.append({"type": "input_text", "text": msg.content})
                for b64 in msg.convert_images("base64"):
                    content_parts.append({
                        "type": "input_image",
                        "image_url": f"data:{msg.mime_type};base64,{b64}",
                    })
                input_msgs.append({"role": "user", "content": content_parts})

            elif isinstance(msg, HumanMessage):
                input_msgs.append({
                    "role": "user",
                    "content": [{"type": "input_text", "text": msg.content or ""}],
                })

            elif isinstance(msg, AIMessage):
                text = msg.content if isinstance(msg.content, str) else json.dumps(msg.content)
                input_msgs.append({
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": text or ""}],
                })

            elif isinstance(msg, ToolMessage):
                # A ToolMessage represents a prior tool call + its result.
                # In the Responses API format this is two items:
                #   1. function_call  (the model's call)
                #   2. function_call_output  (the tool's result)
                input_msgs.append({
                    "type": "function_call",
                    "name": msg.name,
                    "arguments": json.dumps(msg.params),
                    "call_id": msg.id,
                })
                input_msgs.append({
                    "type": "function_call_output",
                    "call_id": msg.id,
                    "output": msg.content or "",
                })

        return instructions, input_msgs

    # ── Tool conversion ─────────────────────────────────────────────

    def _convert_tools(self, tools: List[Tool]) -> list[dict]:
        """Convert Tool objects to Perplexity Agent API (Responses API) format.

        Responses API uses a flat structure (no `function` wrapper):
            {"type": "function", "name": ..., "description": ..., "parameters": ...}
        """
        result = []
        for tool in tools:
            schema = self.sanitize_schema(tool.json_schema)
            result.append({
                "type": "function",
                "name": schema["name"],
                "description": schema.get("description", ""),
                "parameters": schema["parameters"],
            })
        return result

    def sanitize_schema(self, tool_schema: dict) -> dict:
        """Simplify tool schema for Perplexity compatibility.

        Keeps only: name, description, and simplified parameters
        (type, enum, description). Strips anyOf, title, examples, etc.
        """
        params = tool_schema.get("parameters", {})
        properties = params.get("properties", {})
        required = params.get("required", [])

        clean_props = {}
        for name, prop in properties.items():
            if isinstance(prop, dict):
                # Handle anyOf (Optional types)
                if "anyOf" in prop:
                    non_null = [s for s in prop["anyOf"] if s != {"type": "null"}]
                    t = non_null[0].get("type", "string") if non_null else "string"
                else:
                    t = prop.get("type", "string")
                enum_vals = prop.get("enum")
                description = prop.get("description")
            else:
                t = "string"
                enum_vals = None
                description = None

            if t not in {"string", "integer", "number", "boolean", "array", "object"}:
                t = "string"

            entry: dict = {"type": t}
            if enum_vals is not None:
                entry["enum"] = enum_vals
            if description is not None:
                entry["description"] = description
            clean_props[name] = entry

        return {
            "name": tool_schema.get("name"),
            "description": tool_schema.get("description"),
            "parameters": {
                "type": "object",
                "properties": clean_props,
                "required": required,
            },
        }

    # ── API call ────────────────────────────────────────────────────

    def _build_request(self, messages: list[BaseMessage], tools: list[Tool] = []) -> dict:
        """Build the JSON body for the Perplexity Agent API."""
        instructions, input_msgs = self._convert_messages(messages)

        data: dict[str, Any] = {
            "model": self._api_model,
            "input": input_msgs,
            "max_output_tokens": self.max_output_tokens,
            "temperature": self.temperature,
        }

        if instructions:
            data["instructions"] = instructions

        if tools:
            data["tools"] = self._convert_tools(tools)

        if self._model_info.get("reasoning_support", False):
            data["reasoning"] = {
                "effort": self._model_info.get("reasoning_effort", "low")
            }

        return data

    def _parse_response(self, result: dict) -> LLMEvent:
        """Parse Perplexity Agent API response into an LLMEvent."""
        usage_data = result.get("usage", {})
        usage = TokenUsage(
            prompt_tokens=usage_data.get("input_tokens", 0),
            completion_tokens=usage_data.get("output_tokens", 0),
            total_tokens=usage_data.get("input_tokens", 0) + usage_data.get("output_tokens", 0),
        )

        for item in result.get("output", []):
            # Tool call
            if item.get("type") == "function_call":
                try:
                    params = json.loads(item.get("arguments", "{}"))
                except (json.JSONDecodeError, TypeError):
                    params = {}
                return LLMEvent(
                    type=LLMEventType.TOOL_CALL,
                    tool_call=ToolCall(
                        id=item.get("call_id", item.get("id", "")),
                        name=item.get("name", ""),
                        params=params,
                    ),
                    usage=usage,
                )

            # Text message
            if item.get("type") == "message":
                for block in item.get("content", []):
                    if block.get("type") == "output_text":
                        return LLMEvent(
                            type=LLMEventType.TEXT,
                            content=block.get("text", ""),
                            usage=usage,
                        )

        # Fallback
        return LLMEvent(type=LLMEventType.TEXT, content="", usage=usage)

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    # ── Public interface ────────────────────────────────────────────

    def invoke(
        self,
        messages: list[BaseMessage],
        tools: list[Tool] = [],
        structured_output: BaseModel | None = None,
        json_mode: bool = False,
    ) -> LLMEvent:
        data = self._build_request(messages, tools)
        url = f"{self.base_url}/v1/agent"

        resp = self._client.post(url, json=data, headers=self._headers())
        resp.raise_for_status()
        return self._parse_response(resp.json())

    async def ainvoke(
        self,
        messages: list[BaseMessage],
        tools: list[Tool] = [],
        structured_output: BaseModel | None = None,
        json_mode: bool = False,
    ) -> LLMEvent:
        data = self._build_request(messages, tools)
        url = f"{self.base_url}/v1/agent"

        resp = await self._aclient.post(url, json=data, headers=self._headers())
        resp.raise_for_status()
        return self._parse_response(resp.json())

    def stream(
        self,
        messages: list[BaseMessage],
        tools: list[Tool] = [],
        structured_output: BaseModel | None = None,
        json_mode: bool = False,
    ) -> Iterator[LLMStreamEvent]:
        # Perplexity Agent API: fall back to non-streaming
        event = self.invoke(messages, tools, structured_output, json_mode)
        if event.type == LLMEventType.TOOL_CALL:
            yield LLMStreamEvent(type=LLMStreamEventType.TOOL_CALL, tool_call=event.tool_call, usage=event.usage)
        else:
            yield LLMStreamEvent(type=LLMStreamEventType.TEXT_START, content="")
            yield LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content=event.content or "")
            yield LLMStreamEvent(type=LLMStreamEventType.TEXT_END, content="", usage=event.usage)

    async def astream(
        self,
        messages: list[BaseMessage],
        tools: list[Tool] = [],
        structured_output: BaseModel | None = None,
        json_mode: bool = False,
    ) -> AsyncIterator[LLMStreamEvent]:
        event = await self.ainvoke(messages, tools, structured_output, json_mode)
        if event.type == LLMEventType.TOOL_CALL:
            yield LLMStreamEvent(type=LLMStreamEventType.TOOL_CALL, tool_call=event.tool_call, usage=event.usage)
        else:
            yield LLMStreamEvent(type=LLMStreamEventType.TEXT_START, content="")
            yield LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content=event.content or "")
            yield LLMStreamEvent(type=LLMStreamEventType.TEXT_END, content="", usage=event.usage)

    def get_metadata(self) -> Metadata:
        return Metadata(
            name=self.model_name,
            context_window=127072,
            owned_by="perplexity",
        )
