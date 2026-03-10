import os
import json
import logging
from typing import Iterator, AsyncIterator, List, Optional, Any, overload
from openai import OpenAI, AsyncOpenAI
from pydantic import BaseModel
from windows_use.providers.base import BaseChatLLM
from windows_use.providers.views import TokenUsage, Metadata
from windows_use.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ImageMessage, ToolMessage
from windows_use.tools import Tool
from windows_use.providers.events import LLMEvent, LLMEventType, LLMStreamEvent, LLMStreamEventType, ToolCall, Thinking

logger = logging.getLogger(__name__)


class ChatVLLM(BaseChatLLM):
    """
    vLLM LLM implementation following the BaseChatLLM protocol.

    Connects to a vLLM server via its OpenAI-compatible API endpoint.
    vLLM serves models locally with high throughput and supports tool calling,
    structured outputs, streaming, and vision (depending on the served model).

    Usage:
        # Start vLLM server first:
        #   vllm serve <model-name> --host 0.0.0.0 --port 8000
        from windows_use.providers.vllm import ChatVLLM

        llm = ChatVLLM(model="Qwen/Qwen2.5-72B-Instruct")
        # Or with a custom server URL:
        llm = ChatVLLM(model="my-model", base_url="http://my-server:8000/v1")
    """

    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 600.0,
        max_retries: int = 2,
        temperature: Optional[float] = None,
        **kwargs,
    ):
        """
        Initialize the vLLM LLM.

        Args:
            model: The model name served by vLLM (e.g. "Qwen/Qwen2.5-72B-Instruct").
            api_key: API key for the vLLM server. Defaults to VLLM_API_KEY env var
                     or "EMPTY" (vLLM doesn't require a key by default).
            base_url: Base URL for the vLLM OpenAI-compatible endpoint.
                      Defaults to VLLM_BASE_URL env var or "http://localhost:8000/v1".
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries for failed requests.
            temperature: Sampling temperature.
            **kwargs: Additional arguments passed to the chat completions create method.
        """
        self._model = model
        self.api_key = api_key or os.environ.get("VLLM_API_KEY", "EMPTY")
        self.base_url = base_url or os.environ.get("VLLM_BASE_URL", "http://localhost:8000/v1")
        self.temperature = temperature

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.aclient = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.kwargs = kwargs

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def provider(self) -> str:
        return "vllm"

    def _convert_messages(self, messages: List[BaseMessage]) -> List[dict]:
        """Convert BaseMessage objects to OpenAI-compatible message dictionaries."""
        openai_messages = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                openai_messages.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                openai_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, ImageMessage):
                content_list = []
                if msg.content:
                    content_list.append({"type": "text", "text": msg.content})

                b64_imgs = msg.convert_images(format="base64")
                for b64 in b64_imgs:
                    content_list.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:{msg.mime_type};base64,{b64}"},
                    })
                openai_messages.append({"role": "user", "content": content_list})
            elif isinstance(msg, AIMessage):
                msg_dict: dict = {"role": "assistant", "content": msg.content or ""}
                if getattr(msg, "thinking", None):
                    msg_dict["reasoning_content"] = msg.thinking
                openai_messages.append(msg_dict)
            elif isinstance(msg, ToolMessage):
                tool_call = {
                    "id": msg.id,
                    "type": "function",
                    "function": {
                        "name": msg.name,
                        "arguments": json.dumps(msg.params),
                    },
                }
                openai_messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [tool_call],
                })
                openai_messages.append({
                    "role": "tool",
                    "tool_call_id": msg.id,
                    "content": msg.content or "",
                })
        return openai_messages

    def _convert_tools(self, tools: List[Tool]) -> List[dict]:
        """Convert Tool objects to OpenAI-compatible tool definitions."""
        return [
            {
                "type": "function",
                "function": tool.json_schema,
            }
            for tool in tools
        ]

    def _process_response(self, response: Any) -> LLMEvent:
        """Process an OpenAI-compatible API response into AIMessage or ToolMessage."""
        choice = response.choices[0]
        message = choice.message
        usage_data = response.usage

        usage = TokenUsage(
            prompt_tokens=usage_data.prompt_tokens,
            completion_tokens=usage_data.completion_tokens,
            total_tokens=usage_data.total_tokens,
            thinking_tokens=getattr(
                getattr(usage_data, "completion_tokens_details", None),
                "reasoning_tokens",
                None,
            ) or getattr(
                getattr(usage_data, "completion_tokens_details", None),
                "thinking_tokens",
                None,
            ),
        )

        thinking = getattr(message, "reasoning", None) or getattr(message, "reasoning_content", None)
        thinking_obj = Thinking(content=thinking, signature=None) if thinking else None

        if message.tool_calls:
            tool_call = message.tool_calls[0]
            try:
                params = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                params = {}

            content = LLMEvent(
                type=LLMEventType.TOOL_CALL,
                tool_call=ToolCall(
                    id=tool_call.id,
                    name=tool_call.function.name,
                    params=params
                ),
                thinking=thinking_obj,
                usage=usage
            )
        else:
            content = LLMEvent(type=LLMEventType.TEXT, content=message.content or "", thinking=thinking_obj, usage=usage)

        return content

    @overload
    def invoke(
        self,
        messages: list[BaseMessage],
        tools: list[Tool] = [],
        structured_output: BaseModel | None = None,
        json_mode: bool = False,
    ) -> LLMEvent: ...

    def invoke(
        self,
        messages: list[BaseMessage],
        tools: list[Tool] = [],
        structured_output: BaseModel | None = None,
        json_mode: bool = False,
    ) -> LLMEvent:
        openai_messages = self._convert_messages(messages)
        openai_tools = self._convert_tools(tools) if tools else None

        params = {
            "model": self._model,
            "messages": openai_messages,
            **self.kwargs,
        }

        if openai_tools:
            params["tools"] = openai_tools

        if self.temperature is not None:
            params["temperature"] = self.temperature

        if structured_output:
            # vLLM supports guided decoding via response_format with json_schema
            params["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": structured_output.__name__,
                    "schema": structured_output.model_json_schema(),
                },
            }
            params.pop("tools", None)

            response = self.client.chat.completions.create(**params)
            usage_data = response.usage
            thinking_tokens = getattr(
                getattr(usage_data, "completion_tokens_details", None),
                "reasoning_tokens",
                None,
            ) or getattr(
                getattr(usage_data, "completion_tokens_details", None),
                "thinking_tokens",
                None,
            )
            usage = TokenUsage(
                prompt_tokens=usage_data.prompt_tokens,
                completion_tokens=usage_data.completion_tokens,
                total_tokens=usage_data.total_tokens,
                thinking_tokens=thinking_tokens,
            )

            try:
                parsed = structured_output.model_validate_json(
                    response.choices[0].message.content
                )
                content_dump = parsed.model_dump()
                return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content_dump) if isinstance(content_dump, dict) else str(content_dump), usage=usage)
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse structured output: {e}")
                return LLMEvent(
                    type=LLMEventType.TEXT,
                    content=response.choices[0].message.content or "",
                    usage=usage,
                )

        if json_mode:
            params["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(**params)
        return self._process_response(response)

    @overload
    async def ainvoke(
        self,
        messages: list[BaseMessage],
        tools: list[Tool] = [],
        structured_output: BaseModel | None = None,
        json_mode: bool = False,
    ) -> LLMEvent: ...

    async def ainvoke(
        self,
        messages: list[BaseMessage],
        tools: list[Tool] = [],
        structured_output: BaseModel | None = None,
        json_mode: bool = False,
    ) -> LLMEvent:
        openai_messages = self._convert_messages(messages)
        openai_tools = self._convert_tools(tools) if tools else None

        params = {
            "model": self._model,
            "messages": openai_messages,
            **self.kwargs,
        }

        if openai_tools:
            params["tools"] = openai_tools

        if self.temperature is not None:
            params["temperature"] = self.temperature

        if structured_output:
            params["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": structured_output.__name__,
                    "schema": structured_output.model_json_schema(),
                },
            }
            params.pop("tools", None)

            response = await self.aclient.chat.completions.create(**params)
            usage_data = response.usage
            thinking_tokens = getattr(
                getattr(usage_data, "completion_tokens_details", None),
                "reasoning_tokens",
                None,
            ) or getattr(
                getattr(usage_data, "completion_tokens_details", None),
                "thinking_tokens",
                None,
            )
            usage = TokenUsage(
                prompt_tokens=usage_data.prompt_tokens,
                completion_tokens=usage_data.completion_tokens,
                total_tokens=usage_data.total_tokens,
                thinking_tokens=thinking_tokens,
            )

            try:
                parsed = structured_output.model_validate_json(
                    response.choices[0].message.content
                )
                content_dump = parsed.model_dump()
                return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content_dump) if isinstance(content_dump, dict) else str(content_dump), usage=usage)
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse structured output: {e}")
                return LLMEvent(
                    type=LLMEventType.TEXT,
                    content=response.choices[0].message.content or "",
                    usage=usage,
                )

        if json_mode:
            params["response_format"] = {"type": "json_object"}

        response = await self.aclient.chat.completions.create(**params)
        return self._process_response(response)

    @overload
    def stream(
        self,
        messages: list[BaseMessage],
        tools: list[Tool] = [],
        structured_output: BaseModel | None = None,
        json_mode: bool = False,
    ) -> Iterator[LLMStreamEvent]: ...

    def stream(
        self,
        messages: list[BaseMessage],
        tools: list[Tool] = [],
        structured_output: BaseModel | None = None,
        json_mode: bool = False,
    ) -> Iterator[LLMStreamEvent]:
        openai_messages = self._convert_messages(messages)
        openai_tools = self._convert_tools(tools) if tools else None

        params = {
            "model": self._model,
            "messages": openai_messages,
            "stream": True,
            "stream_options": {"include_usage": True},
            **self.kwargs,
        }

        if openai_tools:
            params["tools"] = openai_tools

        if self.temperature is not None:
            params["temperature"] = self.temperature

        if json_mode:
            params["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(**params)

        tool_call_id = None
        tool_call_name = None
        tool_call_args = ""
        usage = None
        
        text_started = False
        think_started = False

        for chunk in response:
            if not chunk.choices:
                if chunk.usage:
                    thinking_tokens = getattr(
                        getattr(chunk.usage, "completion_tokens_details", None),
                        "reasoning_tokens",
                        None,
                    )
                    usage = TokenUsage(
                        prompt_tokens=chunk.usage.prompt_tokens,
                        completion_tokens=chunk.usage.completion_tokens,
                        total_tokens=chunk.usage.total_tokens,
                        thinking_tokens=thinking_tokens,
                    )
                continue

            delta = chunk.choices[0].delta

            reasoning_delta = getattr(delta, "reasoning", None) or getattr(delta, "reasoning_content", None)
            if reasoning_delta:
                if not think_started:
                    think_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_START)
                yield LLMStreamEvent(type=LLMStreamEventType.THINK_DELTA, content=reasoning_delta)
            if delta.content:
                if think_started:
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
                    think_started = False
                if not text_started:
                    text_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.TEXT_START)
                yield LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content=delta.content)

            if hasattr(delta, "tool_calls") and delta.tool_calls:
                if think_started:
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
                    think_started = False
                tc_delta = delta.tool_calls[0]
                if tc_delta.id:
                    tool_call_id = tc_delta.id
                if tc_delta.function:
                    if tc_delta.function.name:
                        tool_call_name = tc_delta.function.name
                    if tc_delta.function.arguments:
                        tool_call_args += tc_delta.function.arguments

        if tool_call_id and tool_call_name:
            if think_started:
                yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
            try:
                params = json.loads(tool_call_args)
            except json.JSONDecodeError:
                params = {}
                
            yield LLMStreamEvent(
                type=LLMStreamEventType.TOOL_CALL,
                tool_call=ToolCall(
                    id=tool_call_id,
                    name=tool_call_name,
                    params=params
                ),
                usage=usage
            )
        else:
            if think_started:
                yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
            if text_started:
                yield LLMStreamEvent(type=LLMStreamEventType.TEXT_END, usage=usage)

    @overload
    async def astream(
        self,
        messages: list[BaseMessage],
        tools: list[Tool] = [],
        structured_output: BaseModel | None = None,
        json_mode: bool = False,
    ) -> AsyncIterator[LLMStreamEvent]: ...

    async def astream(
        self,
        messages: list[BaseMessage],
        tools: list[Tool] = [],
        structured_output: BaseModel | None = None,
        json_mode: bool = False,
    ) -> AsyncIterator[LLMStreamEvent]:
        openai_messages = self._convert_messages(messages)
        openai_tools = self._convert_tools(tools) if tools else None

        params = {
            "model": self._model,
            "messages": openai_messages,
            "stream": True,
            "stream_options": {"include_usage": True},
            **self.kwargs,
        }

        if openai_tools:
            params["tools"] = openai_tools

        if self.temperature is not None:
            params["temperature"] = self.temperature

        if json_mode:
            params["response_format"] = {"type": "json_object"}

        response = await self.aclient.chat.completions.create(**params)

        tool_call_id = None
        tool_call_name = None
        tool_call_args = ""
        usage = None
        
        text_started = False
        think_started = False

        async for chunk in response:
            if not chunk.choices:
                if chunk.usage:
                    thinking_tokens = getattr(
                        getattr(chunk.usage, "completion_tokens_details", None),
                        "reasoning_tokens",
                        None,
                    )
                    usage = TokenUsage(
                        prompt_tokens=chunk.usage.prompt_tokens,
                        completion_tokens=chunk.usage.completion_tokens,
                        total_tokens=chunk.usage.total_tokens,
                        thinking_tokens=thinking_tokens,
                    )
                continue

            delta = chunk.choices[0].delta

            reasoning_delta = getattr(delta, "reasoning", None) or getattr(delta, "reasoning_content", None)
            if reasoning_delta:
                if not think_started:
                    think_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_START)
                yield LLMStreamEvent(type=LLMStreamEventType.THINK_DELTA, content=reasoning_delta)
            if delta.content:
                if think_started:
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
                    think_started = False
                if not text_started:
                    text_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.TEXT_START)
                yield LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content=delta.content)

            if hasattr(delta, "tool_calls") and delta.tool_calls:
                if think_started:
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
                    think_started = False
                tc_delta = delta.tool_calls[0]
                if tc_delta.id:
                    tool_call_id = tc_delta.id
                if tc_delta.function:
                    if tc_delta.function.name:
                        tool_call_name = tc_delta.function.name
                    if tc_delta.function.arguments:
                        tool_call_args += tc_delta.function.arguments

        if tool_call_id and tool_call_name:
            if think_started:
                yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
            try:
                params = json.loads(tool_call_args)
            except json.JSONDecodeError:
                params = {}
                
            yield LLMStreamEvent(
                type=LLMStreamEventType.TOOL_CALL,
                tool_call=ToolCall(
                    id=tool_call_id,
                    name=tool_call_name,
                    params=params
                ),
                usage=usage
            )
        else:
            if think_started:
                yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
            if text_started:
                yield LLMStreamEvent(type=LLMStreamEventType.TEXT_END, usage=usage)

    def get_metadata(self) -> Metadata:
        """Retrieve model metadata from the vLLM server."""
        try:
            model_info = self.client.models.retrieve(self._model)
            context_window = getattr(model_info, "max_model_len", 32768) or 32768
            owned_by = getattr(model_info, "owned_by", "vllm") or "vllm"
            return Metadata(
                name=self._model,
                context_window=context_window,
                owned_by=owned_by,
            )
        except Exception:
            logger.debug(f"Could not retrieve model metadata from vLLM server, using defaults")
            return Metadata(
                name=self._model,
                context_window=32768,
                owned_by="vllm",
            )
