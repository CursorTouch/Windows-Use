import os
import json
import logging
from typing import Iterator, AsyncIterator, List, Optional, Any, overload
from cerebras.cloud.sdk import Cerebras, AsyncCerebras
from pydantic import BaseModel
from windows_use.providers.base import BaseChatLLM
from windows_use.providers.views import TokenUsage, Metadata
from windows_use.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ImageMessage, ToolMessage
from windows_use.tools import Tool
from windows_use.providers.events import LLMEvent, LLMEventType, LLMStreamEvent, LLMStreamEventType, ToolCall, Thinking

logger = logging.getLogger(__name__)

class ChatCerebras(BaseChatLLM):
    """
    Cerebras LLM implementation following the BaseChatLLM protocol.
    """
    
    def __init__(
        self,
        model: str = "llama-3.3-70b",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 60.0,
        max_retries: int = 2,
        temperature: Optional[float] = None,
        **kwargs
    ):
        """
        Initialize the Cerebras LLM.

        Args:
            model (str): The model name to use.
            api_key (str, optional): Cerebras API key. Defaults to CEREBRAS_API_KEY environment variable.
            base_url (str, optional): Base URL for the API.
            timeout (float): Request timeout.
            max_retries (int): Maximum number of retries.
            temperature (float, optional): Sampling temperature.
            **kwargs: Additional arguments for chat completions.
        """
        self._model = model
        self.api_key = api_key or os.environ.get("CEREBRAS_API_KEY")
        self.temperature = temperature
        
        self.client = Cerebras(
            api_key=self.api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.aclient = AsyncCerebras(
            api_key=self.api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.kwargs = kwargs

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def provider(self) -> str:
        return "cerebras"

    def _is_reasoning_model(self) -> bool:
        """Check if the model supports reasoning (gpt-oss, zai-glm, qwen3)."""
        m = self._model.lower()
        return any(p in m for p in ("gpt-oss", "zai-glm", "qwen3"))

    def _format_assistant_content(self, content: str | None, thinking: str | None) -> str:
        """Format assistant content with thinking for Cerebras multi-turn.
        GPT-OSS: reasoning prepended; GLM/Qwen: <think> tags."""
        text = content or ""
        if not thinking:
            return text
        if "gpt-oss" in self._model.lower():
            return f"{thinking} {text}".strip() if text else thinking
        return f"<think>{thinking}</think>{text}" if text else f"<think>{thinking}</think>"

    def _convert_messages(self, messages: List[BaseMessage]) -> List[dict]:
        """
        Convert BaseMessage objects to Cerebras-compatible message dictionaries.
        """
        cerebras_messages = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                cerebras_messages.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                cerebras_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, ImageMessage):
                # Cerebras might not support images yet in the same way, but following OpenAI format
                content_list = []
                if msg.content:
                    content_list.append({"type": "text", "text": msg.content})
                
                b64_imgs = msg.convert_images(format="base64")
                for b64 in b64_imgs:
                    content_list.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:{msg.mime_type};base64,{b64}"}
                    })
                cerebras_messages.append({"role": "user", "content": content_list})
            elif isinstance(msg, AIMessage):
                thinking = getattr(msg, "thinking", None)
                content = self._format_assistant_content(msg.content, thinking)
                cerebras_messages.append({"role": "assistant", "content": content})
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
                cerebras_messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [tool_call]
                })
                cerebras_messages.append({
                    "role": "tool",
                    "tool_call_id": msg.id,
                    "content": msg.content or ""
                })
        return cerebras_messages

    def _convert_tools(self, tools: List[Tool]) -> List[dict]:
        """
        Convert Tool objects to Cerebras-compatible tool definitions.
        """
        return [
            {
                "type": "function",
                "function": tool.json_schema
            }
            for tool in tools
        ]

    def _process_response(self, response: Any) -> LLMEvent:
        """
        Process Cerebras API response into LLMEvent.
        """
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

        thinking = getattr(message, "reasoning", None)
        thinking_obj = Thinking(content=thinking, signature=None) if thinking else None

        content = None
        if hasattr(message, 'tool_calls') and message.tool_calls:
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
                usage=usage
            )
        else:
            content = LLMEvent(type=LLMEventType.TEXT, content=message.content or "", thinking=thinking_obj, usage=usage)

        return content

    @overload
    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ...

    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        cerebras_messages = self._convert_messages(messages)
        cerebras_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": cerebras_messages,
            **self.kwargs
        }
        
        # Only add tools if they exist
        if cerebras_tools:
            params["tools"] = cerebras_tools
        if self._is_reasoning_model():
            params["reasoning_format"] = "parsed"
            if "gpt-oss" in self._model.lower():
                params["reasoning_effort"] = params.get("reasoning_effort", "medium")
        
        if self.temperature is not None:
            params["temperature"] = self.temperature
        
        if structured_output or json_mode:
            params["response_format"] = {"type": "json_object"}
            
        response = self.client.chat.completions.create(**params)
        
        if structured_output:
            try:
                parsed = structured_output.model_validate_json(response.choices[0].message.content)
                content_dump = parsed.model_dump()
                thinking_tokens = getattr(
                    getattr(response.usage, "completion_tokens_details", None),
                    "reasoning_tokens",
                    None,
                ) or getattr(
                    getattr(response.usage, "completion_tokens_details", None),
                    "thinking_tokens",
                    None,
                )
                usage = TokenUsage(
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens,
                    thinking_tokens=thinking_tokens,
                )
                return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content_dump) if isinstance(content_dump, dict) else str(content_dump), usage=usage)
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse structured output: {e}")
                # Fall through to normal response processing

        return self._process_response(response)

    @overload
    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ...

    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        cerebras_messages = self._convert_messages(messages)
        cerebras_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": cerebras_messages,
            **self.kwargs
        }
        
        if cerebras_tools:
            params["tools"] = cerebras_tools
        if self._is_reasoning_model():
            params["reasoning_format"] = "parsed"
            if "gpt-oss" in self._model.lower():
                params["reasoning_effort"] = params.get("reasoning_effort", "medium")
        
        if self.temperature is not None:
            params["temperature"] = self.temperature
        
        if structured_output or json_mode:
            params["response_format"] = {"type": "json_object"}
            
        response = await self.aclient.chat.completions.create(**params)
        
        if structured_output:
            try:
                parsed = structured_output.model_validate_json(response.choices[0].message.content)
                content_dump = parsed.model_dump()
                usage = TokenUsage(
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens,
                )
                return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content_dump) if isinstance(content_dump, dict) else str(content_dump), usage=usage)
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse structured output: {e}")

        return self._process_response(response)

    @overload
    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> Iterator[LLMStreamEvent]:
        ...

    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> Iterator[LLMStreamEvent]:
        cerebras_messages = self._convert_messages(messages)
        cerebras_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": cerebras_messages,
            "stream": True,
            **self.kwargs
        }
        
        if cerebras_tools:
            params["tools"] = cerebras_tools
        if self._is_reasoning_model():
            params["reasoning_format"] = "parsed"
            if "gpt-oss" in self._model.lower():
                params["reasoning_effort"] = params.get("reasoning_effort", "medium")
        
        if self.temperature is not None:
            params["temperature"] = self.temperature
        
        if structured_output or json_mode:
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
                        prompt_tokens=chunk.usage.prompt_tokens,
                        completion_tokens=chunk.usage.completion_tokens,
                        total_tokens=chunk.usage.total_tokens,
                        thinking_tokens=thinking_tokens,
                    )
                continue
            
            delta = chunk.choices[0].delta
            
            reasoning_delta = getattr(delta, "reasoning", None)
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
        cerebras_messages = self._convert_messages(messages)
        cerebras_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": cerebras_messages,
            "stream": True,
            **self.kwargs
        }
        
        if cerebras_tools:
            params["tools"] = cerebras_tools
        if self._is_reasoning_model():
            params["reasoning_format"] = "parsed"
            if "gpt-oss" in self._model.lower():
                params["reasoning_effort"] = params.get("reasoning_effort", "medium")
        
        if self.temperature is not None:
            params["temperature"] = self.temperature
        
        if structured_output or json_mode:
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
                        prompt_tokens=chunk.usage.prompt_tokens,
                        completion_tokens=chunk.usage.completion_tokens,
                        total_tokens=chunk.usage.total_tokens,
                        thinking_tokens=thinking_tokens,
                    )
                continue
            
            delta = chunk.choices[0].delta

            reasoning_delta = getattr(delta, "reasoning", None)
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
            context_window=8192,  # Typical for llama3 on Cerebras, can be adjusted
            owned_by="cerebras"
        )
