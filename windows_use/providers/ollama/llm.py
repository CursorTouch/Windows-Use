import os
import json
import uuid
import logging
from typing import Iterator, AsyncIterator, List, Optional, Any, overload
import ollama
from ollama import Client, AsyncClient
from pydantic import BaseModel
from windows_use.providers.base import BaseChatLLM
from windows_use.providers.views import TokenUsage, Metadata
from windows_use.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ImageMessage, ToolMessage
from windows_use.tools import Tool
from windows_use.providers.events import LLMEvent, LLMEventType, LLMStreamEvent, LLMStreamEventType, ToolCall, Thinking

logger = logging.getLogger(__name__)

class ChatOllama(BaseChatLLM):
    """
    Ollama LLM implementation following the BaseChatLLM protocol.
    """
    
    def __init__(
        self,
        model: str = "llama3.1",
        host: Optional[str] = None,
        timeout: float = 600.0,
        temperature: Optional[float] = None,
        **kwargs
    ):
        """
        Initialize the Ollama LLM.

        Args:
            model (str): The model name to use.
            host (str, optional): Ollama host URL. Defaults to OLLAMA_HOST environment variable or localhost.
            timeout (float): Request timeout.
            temperature (float, optional): Sampling temperature.
            **kwargs: Additional arguments for chat.
        """
        self._model = model
        self.host = host or os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self.temperature = temperature
        
        self.client = Client(host=self.host, timeout=timeout)
        self.aclient = AsyncClient(host=self.host, timeout=timeout)
        self.kwargs = kwargs

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def provider(self) -> str:
        return "ollama"

    def _is_thinking_model(self) -> bool:
        """Check if the model supports thinking (qwen3, deepseek-r1, deepseek-v3, gpt-oss, etc.)."""
        m = self._model.lower()
        return any(
            m.startswith(p)
            for p in ("qwen3", "deepseek-r1", "deepseek-v3", "gpt-oss")
        )

    def _convert_messages(self, messages: List[BaseMessage]) -> List[dict]:
        """
        Convert BaseMessage objects to Ollama-compatible message dictionaries.
        """
        ollama_messages = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                ollama_messages.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                ollama_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, ImageMessage):
                b64_imgs = msg.convert_images(format="base64")
                ollama_messages.append({
                    "role": "user",
                    "content": msg.content or "",
                    "images": b64_imgs
                })
            elif isinstance(msg, AIMessage):
                msg_dict: dict = {"role": "assistant", "content": msg.content or ""}
                if getattr(msg, "thinking", None):
                    msg_dict["thinking"] = msg.thinking
                ollama_messages.append(msg_dict)
            elif isinstance(msg, ToolMessage):
                # Ollama expects assistant message with tool_calls followed by tool message
                # Reconstruct for history consistency
                ollama_messages.append({
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [{
                        "function": {
                            "name": msg.name,
                            "arguments": msg.params
                        }
                    }]
                })
                ollama_messages.append({
                    "role": "tool",
                    "content": msg.content or ""
                })
        return ollama_messages

    def _convert_tools(self, tools: List[Tool]) -> List[dict]:
        """
        Convert Tool objects to Ollama-compatible tool definitions.
        """
        return [
            {
                "type": "function",
                "function": tool.json_schema
            }
            for tool in tools
        ]

    def _process_response(self, response: Any) -> LLMEvent:
        """Process Ollama API response into AIMessage or ToolMessage."""
        message = response.get("message", {})
        thinking = message.get("thinking")
        # Ollama doesn't expose thinking_tokens; estimate from content when available
        thinking_tokens = None
        if thinking:
            thinking_tokens = max(1, len(thinking) // 4)

        usage = TokenUsage(
            prompt_tokens=response.get("prompt_eval_count", 0),
            completion_tokens=response.get("eval_count", 0),
            total_tokens=response.get("prompt_eval_count", 0) + response.get("eval_count", 0),
            thinking_tokens=thinking_tokens,
        )

        tool_calls = message.get("tool_calls", [])
        if tool_calls:
            tool_call = tool_calls[0]
            func = tool_call.get("function", {})
            args = func.get("arguments", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args) if args else {}
                except json.JSONDecodeError:
                    args = {}
            return LLMEvent(
                type=LLMEventType.TOOL_CALL,
                tool_call=ToolCall(
                    id=f"call_{uuid.uuid4().hex[:8]}",  # Ollama doesn't return tool call ID consistently
                    name=func.get("name"),
                    params=args
                ),
                usage=usage
            )
        thinking_obj = Thinking(content=thinking, signature=None) if thinking else None
        return LLMEvent(type=LLMEventType.TEXT, content=message.get("content", ""), thinking=thinking_obj, usage=usage)

    @overload
    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ...

    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ollama_messages = self._convert_messages(messages)
        ollama_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": ollama_messages,
            **self.kwargs
        }
        
        if ollama_tools:
            params["tools"] = ollama_tools
        if self._is_thinking_model():
            params["think"] = True
        
        if self.temperature is not None:
            if "options" not in params:
                params["options"] = {}
            params["options"]["temperature"] = self.temperature
        
        if json_mode or structured_output:
            params["format"] = "json" if not structured_output else structured_output.model_json_schema()

        response = self.client.chat(**params)
        
        if structured_output:
            try:
                parsed = structured_output.model_validate_json(response["message"]["content"])
                content = parsed.model_dump() if hasattr(parsed, "model_dump") else str(parsed)
                usage = TokenUsage(
                    prompt_tokens=response.get("prompt_eval_count", 0),
                    completion_tokens=response.get("eval_count", 0),
                    total_tokens=response.get("prompt_eval_count", 0) + response.get("eval_count", 0),
                    thinking_tokens=None,
                )
                return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content) if isinstance(content, dict) else content, usage=usage)
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse structured output: {e}")
                # Fall through to normal response processing

        return self._process_response(response)

    @overload
    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ...

    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ollama_messages = self._convert_messages(messages)
        ollama_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": ollama_messages,
            **self.kwargs
        }
        
        if ollama_tools:
            params["tools"] = ollama_tools
        if self._is_thinking_model():
            params["think"] = True
        
        if self.temperature is not None:
            if "options" not in params:
                params["options"] = {}
            params["options"]["temperature"] = self.temperature
        
        if json_mode or structured_output:
            params["format"] = "json" if not structured_output else structured_output.model_json_schema()

        response = await self.aclient.chat(**params)
        
        if structured_output:
            try:
                parsed = structured_output.model_validate_json(response["message"]["content"])
                content = parsed.model_dump() if hasattr(parsed, "model_dump") else parsed
                usage = TokenUsage(
                    prompt_tokens=response.get("prompt_eval_count", 0),
                    completion_tokens=response.get("eval_count", 0),
                    total_tokens=response.get("prompt_eval_count", 0) + response.get("eval_count", 0),
                    thinking_tokens=None,
                )
                return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content) if isinstance(content, dict) else content, usage=usage)
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse structured output: {e}")

        return self._process_response(response)

    @overload
    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> Iterator[LLMStreamEvent]:
        ...

    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> Iterator[LLMStreamEvent]:
        ollama_messages = self._convert_messages(messages)
        ollama_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": ollama_messages,
            "stream": True,
            **self.kwargs
        }
        
        if ollama_tools:
            params["tools"] = ollama_tools
        if self._is_thinking_model():
            params["think"] = True
        
        if self.temperature is not None:
            if "options" not in params:
                params["options"] = {}
            params["options"]["temperature"] = self.temperature
        
        if json_mode:
            params["format"] = "json"

        response = self.client.chat(**params)
        
        text_started = False
        think_started = False
        usage = None

        for chunk in response:
            message = chunk.get("message", {})
            # Ollama may send usage in the final chunk
            if "eval_count" in chunk or "prompt_eval_count" in chunk:
                thinking = message.get("thinking")
                thinking_tokens = max(1, len(thinking) // 4) if thinking else None
                usage = TokenUsage(
                    prompt_tokens=chunk.get("prompt_eval_count", 0),
                    completion_tokens=chunk.get("eval_count", 0),
                    total_tokens=chunk.get("prompt_eval_count", 0) + chunk.get("eval_count", 0),
                    thinking_tokens=thinking_tokens,
                )
            if message.get("thinking"):
                if not think_started:
                    think_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_START)
                yield LLMStreamEvent(type=LLMStreamEventType.THINK_DELTA, content=message["thinking"])
            if "content" in message and message["content"]:
                if think_started:
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
                    think_started = False
                if not text_started:
                    text_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.TEXT_START)
                yield LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content=message["content"])

            # Handle tool calls in stream
            tool_calls = message.get("tool_calls", [])
            if tool_calls:
                tc = tool_calls[0]
                func = tc.get("function", {})
                args = func.get("arguments", {})
                if isinstance(args, str):
                    try:
                        args = json.loads(args) if args else {}
                    except json.JSONDecodeError:
                        args = {}
                yield LLMStreamEvent(
                    type=LLMStreamEventType.TOOL_CALL,
                    tool_call=ToolCall(
                        id=f"call_{uuid.uuid4().hex[:8]}",
                        name=func.get("name"),
                        params=args
                    ),
                    usage=usage
                )

        if think_started:
            yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
        if text_started:
            yield LLMStreamEvent(type=LLMStreamEventType.TEXT_END, usage=usage)

    @overload
    async def astream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> AsyncIterator[LLMStreamEvent]:
        ...

    async def astream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> AsyncIterator[LLMStreamEvent]:
        ollama_messages = self._convert_messages(messages)
        ollama_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": ollama_messages,
            "stream": True,
            **self.kwargs
        }
        
        if ollama_tools:
            params["tools"] = ollama_tools
        if self._is_thinking_model():
            params["think"] = True
        
        if self.temperature is not None:
            if "options" not in params:
                params["options"] = {}
            params["options"]["temperature"] = self.temperature
        
        if json_mode:
            params["format"] = "json"

        response = await self.aclient.chat(**params)
        
        text_started = False
        think_started = False
        usage = None

        async for chunk in response:
            message = chunk.get("message", {})
            # Ollama may send usage in the final chunk
            if "eval_count" in chunk or "prompt_eval_count" in chunk:
                thinking = message.get("thinking")
                thinking_tokens = max(1, len(thinking) // 4) if thinking else None
                usage = TokenUsage(
                    prompt_tokens=chunk.get("prompt_eval_count", 0),
                    completion_tokens=chunk.get("eval_count", 0),
                    total_tokens=chunk.get("prompt_eval_count", 0) + chunk.get("eval_count", 0),
                    thinking_tokens=thinking_tokens,
                )
            if message.get("thinking"):
                if not think_started:
                    think_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_START)
                yield LLMStreamEvent(type=LLMStreamEventType.THINK_DELTA, content=message["thinking"])
            if "content" in message and message["content"]:
                if think_started:
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
                    think_started = False
                if not text_started:
                    text_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.TEXT_START)
                yield LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content=message["content"])

            # Handle tool calls in stream
            tool_calls = message.get("tool_calls", [])
            if tool_calls:
                tc = tool_calls[0]
                func = tc.get("function", {})
                args = func.get("arguments", {})
                if isinstance(args, str):
                    try:
                        args = json.loads(args) if args else {}
                    except json.JSONDecodeError:
                        args = {}
                yield LLMStreamEvent(
                    type=LLMStreamEventType.TOOL_CALL,
                    tool_call=ToolCall(
                        id=f"call_{uuid.uuid4().hex[:8]}",
                        name=func.get("name"),
                        params=args
                    ),
                    usage=usage
                )
                
        if think_started:
            yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
        if text_started:
            yield LLMStreamEvent(type=LLMStreamEventType.TEXT_END, usage=usage)

    def get_metadata(self) -> Metadata:
        return Metadata(
            name=self._model,
            context_window=32768, # Common default for llama3
            owned_by="ollama"
        )
