import os
import json
import logging
from typing import Iterator, AsyncIterator, List, Optional, Any, overload
import litellm
from pydantic import BaseModel
from windows_use.providers.base import BaseChatLLM
from windows_use.providers.views import TokenUsage, Metadata
from windows_use.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ImageMessage, ToolMessage
from windows_use.tools import Tool
from windows_use.providers.events import LLMEvent, LLMEventType, LLMStreamEvent, LLMStreamEventType, ToolCall, Thinking

logger = logging.getLogger(__name__)


class ChatLiteLLM(BaseChatLLM):
    """
    LiteLLM wrapper implementation following the BaseChatLLM protocol.

    LiteLLM provides a unified interface to 100+ LLM providers using the OpenAI format.
    Model names follow the LiteLLM convention: "provider/model-name"
    (e.g., "anthropic/claude-3-5-sonnet-latest", "openai/gpt-4o", "gemini/gemini-2.0-flash").

    Supports:
    - Standard chat completions via any LiteLLM-supported provider
    - Tool/function calling
    - Structured outputs (via JSON mode fallback)
    - Streaming (sync and async)
    - Vision (image inputs)
    - Custom API keys and base URLs per provider
    """

    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 600.0,
        max_retries: int = 2,
        temperature: Optional[float] = None,
        drop_params: bool = True,
        **kwargs,
    ):
        """
        Initialize the LiteLLM wrapper.

        Args:
            model: The model name in LiteLLM format (e.g., "anthropic/claude-3-5-sonnet-latest").
            api_key: API key for the provider. If not set, LiteLLM will use the
                     appropriate environment variable (e.g., OPENAI_API_KEY, ANTHROPIC_API_KEY).
            base_url: Custom base URL for the provider API.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries for failed requests.
            temperature: Sampling temperature.
            drop_params: If True, LiteLLM will silently drop unsupported params instead of raising.
            **kwargs: Additional arguments passed through to litellm.completion().
        """
        self._model = model
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.temperature = temperature
        self.drop_params = drop_params
        self.kwargs = kwargs

        # Configure LiteLLM settings
        litellm.drop_params = self.drop_params

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def provider(self) -> str:
        return "litellm"

    def _convert_messages(self, messages: List[BaseMessage]) -> List[dict]:
        """
        Convert BaseMessage objects to OpenAI-compatible message dictionaries.
        LiteLLM uses the OpenAI message format for all providers.
        """
        converted = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                converted.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                converted.append({"role": "user", "content": msg.content})
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
                converted.append({"role": "user", "content": content_list})
            elif isinstance(msg, AIMessage):
                msg_dict: dict = {"role": "assistant", "content": msg.content or ""}
                thinking = getattr(msg, "thinking", None)
                if thinking:
                    # OpenAI/o1, Groq, etc.: reasoning_content
                    msg_dict["reasoning_content"] = thinking
                    # Anthropic: thinking_blocks (required for multi-turn with tools)
                    sig = getattr(msg, "thinking_signature", None) or ""
                    if isinstance(sig, bytes):
                        sig = sig.decode("utf-8", errors="replace")
                    msg_dict["thinking_blocks"] = [
                        {"type": "thinking", "thinking": thinking, "signature": sig}
                    ]
                converted.append(msg_dict)
            elif isinstance(msg, ToolMessage):
                # Reconstruct the tool call and result for history consistency
                tool_call = {
                    "id": msg.id,
                    "type": "function",
                    "function": {
                        "name": msg.name,
                        "arguments": json.dumps(msg.params),
                    },
                }
                asst_msg: dict = {"role": "assistant", "content": None, "tool_calls": [tool_call]}
                thinking = getattr(msg, "thinking", None)
                if thinking:
                    asst_msg["reasoning_content"] = thinking
                    sig = getattr(msg, "thinking_signature", None) or ""
                    if isinstance(sig, bytes):
                        sig = sig.decode("utf-8", errors="replace")
                    asst_msg["thinking_blocks"] = [
                        {"type": "thinking", "thinking": thinking, "signature": sig}
                    ]
                converted.append(asst_msg)
                converted.append({
                    "role": "tool",
                    "tool_call_id": msg.id,
                    "content": msg.content or "",
                })
        return converted

    def _convert_tools(self, tools: List[Tool]) -> List[dict]:
        """
        Convert Tool objects to OpenAI-compatible tool definitions.
        """
        return [
            {
                "type": "function",
                "function": tool.json_schema,
            }
            for tool in tools
        ]

    def _build_params(
        self,
        messages: List[dict],
        tools: Optional[List[dict]] = None,
        stream: bool = False,
        json_mode: bool = False,
    ) -> dict:
        """
        Build the common parameters dict for litellm calls.
        """
        params: dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            "timeout": self.timeout,
            "num_retries": self.max_retries,
            **self.kwargs,
        }

        if self.api_key:
            params["api_key"] = self.api_key
        if self.base_url:
            params["api_base"] = self.base_url
        if self.temperature is not None:
            params["temperature"] = self.temperature
        if tools:
            params["tools"] = tools
        if stream:
            params["stream"] = True
            params["stream_options"] = {"include_usage": True}
        if json_mode:
            params["response_format"] = {"type": "json_object"}

        return params

    def _extract_usage(self, usage_data: Any) -> TokenUsage:
        """
        Extract usage information from a LiteLLM response.
        """
        prompt_tokens = getattr(usage_data, "prompt_tokens", 0) or 0
        completion_tokens = getattr(usage_data, "completion_tokens", 0) or 0
        total_tokens = getattr(usage_data, "total_tokens", 0) or 0

        # Extract reasoning/thinking tokens if available
        thinking_tokens = None
        if hasattr(usage_data, "completion_tokens_details") and usage_data.completion_tokens_details:
            thinking_tokens = getattr(
                usage_data.completion_tokens_details, "reasoning_tokens", None
            ) or getattr(
                usage_data.completion_tokens_details, "thinking_tokens", None
            )

        # Extract cache tokens if available
        cache_creation = None
        cache_read = None
        if hasattr(usage_data, "cache_creation_input_tokens"):
            cache_creation = getattr(usage_data, "cache_creation_input_tokens", None)
        if hasattr(usage_data, "cache_read_input_tokens"):
            cache_read = getattr(usage_data, "cache_read_input_tokens", None)

        return TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            thinking_tokens=thinking_tokens,
            cache_creation_input_tokens=cache_creation,
            cache_read_input_tokens=cache_read,
        )

    def _process_response(self, response: Any) -> LLMEvent:
        """
        Process a LiteLLM response (OpenAI-compatible format) into AIMessage or ToolMessage.
        """
        choice = response.choices[0]
        message = choice.message
        usage = self._extract_usage(response.usage) if response.usage else None

        # Check for thinking/reasoning content
        thinking = None
        if hasattr(message, "reasoning_content") and message.reasoning_content:
            thinking = message.reasoning_content

        thinking_obj = Thinking(content=thinking, signature=None) if thinking else None

        content = None
        if hasattr(message, "tool_calls") and message.tool_calls:
            tool_call = message.tool_calls[0]
            try:
                params = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse tool arguments: {tool_call.function.arguments}")
                params = {}

            content = LLMEvent(
                type=LLMEventType.TOOL_CALL,
                tool_call=ToolCall(
                    id=tool_call.id,
                    name=tool_call.function.name,
                    params=params
                ),
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
        converted_messages = self._convert_messages(messages)
        converted_tools = self._convert_tools(tools) if tools else None

        if structured_output:
            # Use JSON mode and parse the output into the structured model
            params = self._build_params(
                converted_messages, converted_tools, json_mode=True
            )
            response = litellm.completion(**params)

            try:
                content_text = response.choices[0].message.content
                parsed_data = json.loads(content_text)
                parsed_obj = structured_output(**parsed_data)

                content_dump = parsed_obj.model_dump()
                usage = self._extract_usage(response.usage) if response.usage else None
                return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content_dump) if isinstance(content_dump, dict) else str(content_dump), usage=usage)
            except (json.JSONDecodeError, TypeError, ValueError) as e:
                logger.error(f"Failed to parse structured output: {e}")
                # Fall through to normal processing

        params = self._build_params(converted_messages, converted_tools, json_mode=json_mode)
        response = litellm.completion(**params)
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
        converted_messages = self._convert_messages(messages)
        converted_tools = self._convert_tools(tools) if tools else None

        if structured_output:
            params = self._build_params(
                converted_messages, converted_tools, json_mode=True
            )
            response = await litellm.acompletion(**params)

            try:
                content_text = response.choices[0].message.content
                parsed_data = json.loads(content_text)
                parsed_obj = structured_output(**parsed_data)

                content_dump = parsed_obj.model_dump()
                usage = self._extract_usage(response.usage) if response.usage else None
                return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content_dump) if isinstance(content_dump, dict) else str(content_dump), usage=usage)
            except (json.JSONDecodeError, TypeError, ValueError) as e:
                logger.error(f"Failed to parse structured output: {e}")

        params = self._build_params(converted_messages, converted_tools, json_mode=json_mode)
        response = await litellm.acompletion(**params)
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
        converted_messages = self._convert_messages(messages)
        converted_tools = self._convert_tools(tools) if tools else None
        params = self._build_params(
            converted_messages, converted_tools, stream=True, json_mode=json_mode
        )

        response = litellm.completion(**params)

        # Accumulators for streamed tool calls
        tool_call_id = None
        tool_call_name = None
        tool_call_args = ""
        usage = None

        text_started = False
        think_started = False
        usage = None

        for chunk in response:
            if not chunk.choices:
                if chunk.usage:
                    usage = self._extract_usage(chunk.usage)
                continue

            delta = chunk.choices[0].delta

            if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                if not think_started:
                    think_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_START)
                yield LLMStreamEvent(type=LLMStreamEventType.THINK_DELTA, content=delta.reasoning_content)

            if hasattr(delta, "content") and delta.content:
                if think_started:
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
                    think_started = False
                if not text_started:
                    text_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.TEXT_START)
                yield LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content=delta.content)

            # Accumulate tool call deltas
            if hasattr(delta, "tool_calls") and delta.tool_calls:
                tc_delta = delta.tool_calls[0]
                if tc_delta.id:
                    tool_call_id = tc_delta.id
                if tc_delta.function:
                    if tc_delta.function.name:
                        tool_call_name = tc_delta.function.name
                    if tc_delta.function.arguments:
                        tool_call_args += tc_delta.function.arguments

        # Yield accumulated tool call as final response
        if tool_call_id and tool_call_name:
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
                )
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
        converted_messages = self._convert_messages(messages)
        converted_tools = self._convert_tools(tools) if tools else None
        params = self._build_params(
            converted_messages, converted_tools, stream=True, json_mode=json_mode
        )

        response = await litellm.acompletion(**params)

        # Accumulators for streamed tool calls
        tool_call_id = None
        tool_call_name = None
        tool_call_args = ""
        usage = None

        text_started = False
        think_started = False
        usage = None

        async for chunk in response:
            if not chunk.choices:
                if chunk.usage:
                    usage = self._extract_usage(chunk.usage)
                continue

            delta = chunk.choices[0].delta

            if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                if not think_started:
                    think_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_START)
                yield LLMStreamEvent(type=LLMStreamEventType.THINK_DELTA, content=delta.reasoning_content)

            if hasattr(delta, "content") and delta.content:
                if think_started:
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
                    think_started = False
                if not text_started:
                    text_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.TEXT_START)
                yield LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content=delta.content)

            # Accumulate tool call deltas
            if hasattr(delta, "tool_calls") and delta.tool_calls:
                tc_delta = delta.tool_calls[0]
                if tc_delta.id:
                    tool_call_id = tc_delta.id
                if tc_delta.function:
                    if tc_delta.function.name:
                        tool_call_name = tc_delta.function.name
                    if tc_delta.function.arguments:
                        tool_call_args += tc_delta.function.arguments

        # Yield accumulated tool call as final response
        if tool_call_id and tool_call_name:
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
        # Try to get model info from LiteLLM's model registry
        try:
            model_info = litellm.get_model_info(self._model)
            context_window = model_info.get("max_input_tokens", 128000)
            owned_by = model_info.get("litellm_provider", "unknown")
        except Exception:
            context_window = 128000  # Safe default
            owned_by = "unknown"

        return Metadata(
            name=self._model,
            context_window=context_window,
            owned_by=owned_by,
        )
