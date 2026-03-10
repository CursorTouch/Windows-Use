import os
import json
import logging
from typing import Iterator, AsyncIterator, List, Optional, Any, Union, overload
from openai import OpenAI, AsyncOpenAI
from pydantic import BaseModel
from windows_use.providers.base import BaseChatLLM
from windows_use.providers.views import TokenUsage, Metadata
from windows_use.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ImageMessage, ToolMessage
from windows_use.tools import Tool
from windows_use.providers.events import LLMEvent, LLMEventType, LLMStreamEvent, LLMStreamEventType, ToolCall, Thinking

logger = logging.getLogger(__name__)

class ChatOpenRouter(BaseChatLLM):
    """
    OpenRouter LLM implementation following the BaseChatLLM protocol.
    Uses OpenAI SDK with OpenRouter base URL.
    
    OpenRouter provides access to multiple LLM providers through a unified API.
    """
    
    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        base_url: str = "https://openrouter.ai/api/v1",
        timeout: float = 600.0,
        max_retries: int = 2,
        temperature: Optional[float] = None,
        default_headers: Optional[dict] = None,
        **kwargs
    ):
        """
        Initialize the OpenRouter LLM.

        Args:
            model (str): The model name (e.g., 'anthropic/claude-3-sonnet').
            api_key (str, optional): OpenRouter API key. Defaults to OPENROUTER_API_KEY.
            base_url (str): OpenRouter base URL.
            timeout (float): Request timeout.
            max_retries (int): Maximum retries.
            temperature (float, optional): Sampling temperature..
            **kwargs: Additional arguments for chat completions.
        """
        self._model = model
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        self.temperature = temperature
        
        # Build headers
        headers = default_headers or {}
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=headers
        )
        self.aclient = AsyncOpenAI(
            api_key=self.api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=headers
        )
        self.kwargs = kwargs

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def provider(self) -> str:
        return "open_router"

    def _convert_messages(self, messages: List[BaseMessage]) -> List[dict]:
        """
        Convert BaseMessage objects to OpenRouter-compatible message dictionaries.
        """
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
                        "image_url": {"url": f"data:{msg.mime_type};base64,{b64}"}
                    })
                openai_messages.append({"role": "user", "content": content_list})
            elif isinstance(msg, AIMessage):
                msg_dict: dict = {"role": "assistant", "content": msg.content or ""}
                if getattr(msg, "thinking", None):
                    msg_dict["reasoning_content"] = msg.thinking
                openai_messages.append(msg_dict)
            elif isinstance(msg, ToolMessage):
                # Reconstruct for history consistency
                tool_call = {
                    "id": msg.id,
                    "type": "function",
                    "function": {
                        "name": msg.name,
                        "arguments": json.dumps(msg.params)
                    }
                }
                openai_messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [tool_call]
                })
                openai_messages.append({
                    "role": "tool",
                    "tool_call_id": msg.id,
                    "content": msg.content or ""
                })
        return openai_messages

    def _convert_tools(self, tools: List[Tool]) -> List[dict]:
        """
        Convert Tool objects to OpenRouter-compatible tool definitions.
        """
        return [
            {
                "type": "function",
                "function": tool.json_schema
            }
            for tool in tools
        ]

    def _process_response(self, response: Any) -> LLMEvent:
        """Process OpenRouter API response into AIMessage or ToolMessage."""
        choice = response.choices[0]
        message = choice.message
        usage_data = response.usage

        usage = TokenUsage(
            prompt_tokens=getattr(usage_data, "prompt_tokens", 0),
            completion_tokens=getattr(usage_data, "completion_tokens", 0),
            total_tokens=getattr(usage_data, "total_tokens", 0),
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

        thinking = None
        if hasattr(message, "reasoning_content") and message.reasoning_content:
            thinking = message.reasoning_content
        thinking_obj = Thinking(content=thinking, signature=None) if thinking else None

        if hasattr(message, "tool_calls") and message.tool_calls:
            tool_call = message.tool_calls[0]
            try:
                params = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse tool arguments: {tool_call.function.arguments}")
                params = {}
            return LLMEvent(
                type=LLMEventType.TOOL_CALL,
                tool_call=ToolCall(
                    id=tool_call.id,
                    name=tool_call.function.name,
                    params=params
                ),
                usage=usage
            )
        return LLMEvent(type=LLMEventType.TEXT, content=message.content or "", thinking=thinking_obj, usage=usage)

    @overload
    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ...

    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        openai_messages = self._convert_messages(messages)
        openai_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": openai_messages,
            **self.kwargs
        }
        
        # Only add tools if they exist
        if openai_tools:
            params["tools"] = openai_tools
        
        if self.temperature is not None:
            params["temperature"] = self.temperature
        
        if json_mode:
            params["response_format"] = {"type": "json_object"}
        
        # Note: OpenRouter doesn't support structured_output via beta.parse
        if structured_output:
            logger.warning("OpenRouter does not support structured_output via beta.parse. Using json_mode instead.")
            params["response_format"] = {"type": "json_object"}
            
        response = self.client.chat.completions.create(**params)
        
        if structured_output:
            # Try to parse the JSON response into the structured output
            try:
                content_text = response.choices[0].message.content
                parsed_data = json.loads(content_text)
                parsed_obj = structured_output(**parsed_data)
                
                thinking_tokens = getattr(
                    getattr(response.usage, "completion_tokens_details", None),
                    "reasoning_tokens",
                    None,
                ) or getattr(
                    getattr(response.usage, "completion_tokens_details", None),
                    "thinking_tokens",
                    None,
                )
                content = parsed_obj.model_dump() if hasattr(parsed_obj, "model_dump") else str(parsed_obj)
                usage = TokenUsage(
                    prompt_tokens=getattr(response.usage, "prompt_tokens", 0),
                    completion_tokens=getattr(response.usage, "completion_tokens", 0),
                    total_tokens=getattr(response.usage, "total_tokens", 0),
                    thinking_tokens=thinking_tokens,
                )
                return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content) if isinstance(content, dict) else content, usage=usage)
            except (json.JSONDecodeError, TypeError, ValueError) as e:
                logger.error(f"Failed to parse structured output: {e}")
                # Fall through to normal response processing
        
        return self._process_response(response)

    @overload
    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ...

    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        openai_messages = self._convert_messages(messages)
        openai_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": openai_messages,
            **self.kwargs
        }
        
        if openai_tools:
            params["tools"] = openai_tools
        
        if self.temperature is not None:
            params["temperature"] = self.temperature
        
        if json_mode:
            params["response_format"] = {"type": "json_object"}
        
        if structured_output:
            logger.warning("OpenRouter does not support structured_output via beta.parse. Using json_mode instead.")
            params["response_format"] = {"type": "json_object"}
            
        response = await self.aclient.chat.completions.create(**params)
        
        if structured_output:
            try:
                content_text = response.choices[0].message.content
                parsed_data = json.loads(content_text)
                parsed_obj = structured_output(**parsed_data)
                
                thinking_tokens = getattr(
                    getattr(response.usage, "completion_tokens_details", None),
                    "reasoning_tokens",
                    None,
                ) or getattr(
                    getattr(response.usage, "completion_tokens_details", None),
                    "thinking_tokens",
                    None,
                )
                content = parsed_obj.model_dump() if hasattr(parsed_obj, "model_dump") else str(parsed_obj)
                usage = TokenUsage(
                    prompt_tokens=getattr(response.usage, "prompt_tokens", 0),
                    completion_tokens=getattr(response.usage, "completion_tokens", 0),
                    total_tokens=getattr(response.usage, "total_tokens", 0),
                    thinking_tokens=thinking_tokens,
                )
                return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content) if isinstance(content, dict) else content, usage=usage)
            except (json.JSONDecodeError, TypeError, ValueError) as e:
                logger.error(f"Failed to parse structured output: {e}")
        
        return self._process_response(response)

    @overload
    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> Iterator[LLMStreamEvent]:
        ...

    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> Iterator[LLMStreamEvent]:
        openai_messages = self._convert_messages(messages)
        openai_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": openai_messages,
            "stream": True,
            "stream_options": {"include_usage": True},
            **self.kwargs
        }
        
        if openai_tools:
            params["tools"] = openai_tools
        
        if self.temperature is not None:
            params["temperature"] = self.temperature
        
        if json_mode:
            params["response_format"] = {"type": "json_object"}
        
        response = self.client.chat.completions.create(**params)
        
        # Accumulators for streamed tool calls
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
                    ) or getattr(
                        getattr(chunk.usage, "completion_tokens_details", None),
                        "thinking_tokens",
                        None,
                    )
                    usage = TokenUsage(
                        prompt_tokens=getattr(chunk.usage, "prompt_tokens", 0),
                        completion_tokens=getattr(chunk.usage, "completion_tokens", 0),
                        total_tokens=getattr(chunk.usage, "total_tokens", 0),
                        thinking_tokens=thinking_tokens,
                    )
                continue
            
            delta = chunk.choices[0].delta
            
            if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                if not think_started:
                    think_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_START)
                yield LLMStreamEvent(type=LLMStreamEventType.THINK_DELTA, content=delta.reasoning_content)
            if delta.content:
                if think_started:
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
                    think_started = False
                if not text_started:
                    text_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.TEXT_START)
                yield LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content=delta.content)
            
            # Accumulate tool call deltas
            if hasattr(delta, 'tool_calls') and delta.tool_calls:
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

    @overload
    async def astream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> AsyncIterator[LLMStreamEvent]:
        ...

    async def astream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> AsyncIterator[LLMStreamEvent]:
        openai_messages = self._convert_messages(messages)
        openai_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": openai_messages,
            "stream": True,
            "stream_options": {"include_usage": True},
            **self.kwargs
        }
        
        if openai_tools:
            params["tools"] = openai_tools
        
        if self.temperature is not None:
            params["temperature"] = self.temperature
        
        if json_mode:
            params["response_format"] = {"type": "json_object"}
        
        response = await self.aclient.chat.completions.create(**params)
        
        # Accumulators for streamed tool calls
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
                    ) or getattr(
                        getattr(chunk.usage, "completion_tokens_details", None),
                        "thinking_tokens",
                        None,
                    )
                    usage = TokenUsage(
                        prompt_tokens=getattr(chunk.usage, "prompt_tokens", 0),
                        completion_tokens=getattr(chunk.usage, "completion_tokens", 0),
                        total_tokens=getattr(chunk.usage, "total_tokens", 0),
                        thinking_tokens=thinking_tokens,
                    )
                continue
            
            delta = chunk.choices[0].delta

            if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                if not think_started:
                    think_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_START)
                yield LLMStreamEvent(type=LLMStreamEventType.THINK_DELTA, content=delta.reasoning_content)
            if delta.content:
                if think_started:
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
                    think_started = False
                if not text_started:
                    text_started = True
                    yield LLMStreamEvent(type=LLMStreamEventType.TEXT_START)
                yield LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content=delta.content)
            
            # Accumulate tool call deltas
            if hasattr(delta, 'tool_calls') and delta.tool_calls:
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
        return Metadata(
            name=self._model,
            context_window=128000,  # Varies by model, this is a safe default
            owned_by="open_router"
        )
