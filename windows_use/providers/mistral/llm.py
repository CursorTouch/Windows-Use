import os
import json
import logging
from typing import Iterator, AsyncIterator, List, Optional, Any, Union, overload
from mistralai import Mistral
from mistralai.models import AssistantMessage, UserMessage, SystemMessage as MistralSystemMessage, ToolMessage as MistralToolMessage
from pydantic import BaseModel
from windows_use.providers.base import BaseChatLLM
from windows_use.providers.views import TokenUsage, Metadata
from windows_use.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ImageMessage, ToolMessage
from windows_use.tools import Tool
from windows_use.providers.events import LLMEvent, LLMEventType, LLMStreamEvent, LLMStreamEventType, ToolCall, Thinking

logger = logging.getLogger(__name__)


def _mistral_tool_call_id(s: str) -> str:
    """Convert tool call ID to Mistral API format: exactly 9 alphanumeric chars."""
    alnum = "".join(c for c in s if c.isalnum())
    if len(alnum) >= 9:
        return alnum[:9]
    return alnum + "0" * (9 - len(alnum))


class ChatMistral(BaseChatLLM):
    """
    Mistral AI LLM implementation following the BaseChatLLM protocol.
    
    Supports Mistral models including:
    - Mistral Large
    - Mistral Medium
    - Mistral Small
    - Codestral
    """
    
    def __init__(
        self,
        model: str = "mistral-large-latest",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ):
        """
        Initialize the Mistral LLM.

        Args:
            model (str): The model name to use.
            api_key (str, optional): Mistral API key. Defaults to MISTRAL_API_KEY environment variable.
            base_url (str, optional): Base URL for the API.
            timeout (int, optional): Request timeout.
            temperature (float, optional): Sampling temperature.
            **kwargs: Additional arguments for chat completions.
        """
        self._model = model
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        self.temperature = temperature
        self.client = Mistral(api_key=self.api_key, server_url=base_url)
        self.kwargs = kwargs

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def provider(self) -> str:
        return "mistral"

    def _convert_messages(self, messages: List[BaseMessage]) -> List[Any]:
        """
        Convert BaseMessage objects to Mistral-compatible message objects.
        """
        mistral_messages = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                mistral_messages.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                mistral_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, ImageMessage):
                content = []
                if msg.content:
                    content.append({"type": "text", "text": msg.content})
                
                b64_imgs = msg.convert_images(format="base64")
                for b64 in b64_imgs:
                    content.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:{msg.mime_type};base64,{b64}"},
                    })
                mistral_messages.append({"role": "user", "content": content})
            elif isinstance(msg, AIMessage):
                if getattr(msg, "thinking", None):
                    # Magistral models: pass thinking as content chunks for multi-turn continuity
                    content = [{"type": "thinking", "thinking": [{"type": "text", "text": msg.thinking}]}]
                    if msg.content:
                        content.append({"type": "text", "text": msg.content})
                    mistral_messages.append({"role": "assistant", "content": content})
                else:
                    mistral_messages.append({"role": "assistant", "content": msg.content or ""})
            elif isinstance(msg, ToolMessage):
                # Mistral requires assistant message with tool_calls followed by tool message
                # API expects 9 alphanumeric chars; model returns long IDs (toolu_...)
                tool_id = _mistral_tool_call_id(msg.id)
                mistral_messages.append({
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [{
                        "id": tool_id,
                        "type": "function",
                        "function": {
                            "name": msg.name,
                            "arguments": json.dumps(msg.params)
                        }
                    }]
                })
                mistral_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_id,
                    "name": msg.name,
                    "content": msg.content or ""
                })
        return mistral_messages

    def _convert_tools(self, tools: List[Tool]) -> List[dict]:
        """
        Convert Tool objects to Mistral-compatible tool definitions.
        """
        return [
            {
                "type": "function",
                "function": tool.json_schema
            }
            for tool in tools
        ]

    def _extract_content(self, raw_content: Any) -> tuple[str, str | None]:
        """
        Extract text content and thinking from Mistral response content.

        Magistral (thinking) models return content as a list of TextChunk and
        ThinkChunk objects instead of a plain string. This method normalizes
        both formats into a (text, thinking) tuple.

        Args:
            raw_content: The message content from the Mistral API response.

        Returns:
            A tuple of (text_content, thinking_content). thinking_content is
            None when there is no thinking output.
        """
        if isinstance(raw_content, str):
            return raw_content, None
        if not isinstance(raw_content, list):
            return str(raw_content) if raw_content else "", None

        text_parts: list[str] = []
        thinking_parts: list[str] = []

        for chunk in raw_content:
            chunk_type = getattr(chunk, "type", None)
            if chunk_type == "text":
                text_parts.append(chunk.text)
            elif chunk_type == "thinking":
                # ThinkChunk.thinking is a list of TextChunk/ReferenceChunk
                for inner in getattr(chunk, "thinking", []):
                    if hasattr(inner, "text"):
                        thinking_parts.append(inner.text)

        text = "".join(text_parts)
        thinking = "".join(thinking_parts) if thinking_parts else None
        return text, thinking

    def _process_response(self, response: Any) -> LLMEvent:
        """
        Process Mistral API response into AIMessage or ToolMessage.
        """
        choice = response.choices[0]
        message = choice.message
        usage_data = response.usage

        # Mistral API doesn't expose thinking_tokens; check usage.prompt_tokens_details
        # or estimate from thinking content when available
        thinking_tokens = None
        if hasattr(usage_data, "completion_tokens_details") and usage_data.completion_tokens_details:
            thinking_tokens = getattr(
                usage_data.completion_tokens_details, "reasoning_tokens", None
            ) or getattr(
                usage_data.completion_tokens_details, "thinking_tokens", None
            )
        if hasattr(usage_data, "prompt_tokens_details") and usage_data.prompt_tokens_details:
            thinking_tokens = thinking_tokens or getattr(
                usage_data.prompt_tokens_details, "reasoning_tokens", None
            )

        usage = TokenUsage(
            prompt_tokens=usage_data.prompt_tokens,
            completion_tokens=usage_data.completion_tokens,
            total_tokens=usage_data.total_tokens,
            thinking_tokens=thinking_tokens,
        )

        content = None
        thinking = None

        if hasattr(message, 'tool_calls') and message.tool_calls:
            # Extract thinking from content if present (Magistral thinking models)
            if message.content:
                _, thinking = self._extract_content(message.content)

            tool_call = message.tool_calls[0]
            try:
                # Mistral may return arguments as string or dict
                if isinstance(tool_call.function.arguments, str):
                    params = json.loads(tool_call.function.arguments)
                elif isinstance(tool_call.function.arguments, dict):
                    params = tool_call.function.arguments
                else:
                    params = {}
            except (json.JSONDecodeError, TypeError) as e:
                logger.warning(f"Failed to parse tool arguments: {e}")
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
            text, thinking = self._extract_content(message.content)
            thinking_obj = Thinking(content=thinking, signature=None) if thinking else None
            # Estimate thinking_tokens from content when API doesn't provide it
            if thinking and usage.thinking_tokens is None:
                usage = TokenUsage(
                    prompt_tokens=usage.prompt_tokens,
                    completion_tokens=usage.completion_tokens,
                    total_tokens=usage.total_tokens,
                    thinking_tokens=max(1, len(thinking) // 4),  # ~4 chars per token
                )
            content = LLMEvent(type=LLMEventType.TEXT, content=text or "", thinking=thinking_obj, usage=usage)

        return content

    @overload
    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ...

    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        mistral_messages = self._convert_messages(messages)
        mistral_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": mistral_messages,
            **self.kwargs
        }
        
        # Only add tools if they exist
        if mistral_tools:
            params["tools"] = mistral_tools
        
        if self.temperature is not None:
            params["temperature"] = self.temperature
        
        if structured_output or json_mode:
            params["response_format"] = {"type": "json_object"}

        response = self.client.chat.complete(**params)
        
        if structured_output:
            try:
                # Parse JSON response into structured output
                content_text, _ = self._extract_content(response.choices[0].message.content)
                if content_text:
                    parsed = structured_output.model_validate_json(content_text)
                else:
                    parsed = structured_output()

                content = parsed.model_dump() if hasattr(parsed, "model_dump") else str(parsed)
                thinking_tokens = None
                if hasattr(response.usage, "completion_tokens_details") and response.usage.completion_tokens_details:
                    thinking_tokens = getattr(
                        response.usage.completion_tokens_details, "reasoning_tokens", None
                    ) or getattr(
                        response.usage.completion_tokens_details, "thinking_tokens", None
                    )
                usage = TokenUsage(
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens,
                    thinking_tokens=thinking_tokens,
                )
                return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content) if isinstance(content, dict) else content, usage=usage)
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse structured output: {e}")
                # Fall through to normal processing

        return self._process_response(response)

    @overload
    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ...

    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        mistral_messages = self._convert_messages(messages)
        mistral_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": mistral_messages,
            **self.kwargs
        }
        
        if mistral_tools:
            params["tools"] = mistral_tools
        
        if self.temperature is not None:
            params["temperature"] = self.temperature
        
        if structured_output or json_mode:
            params["response_format"] = {"type": "json_object"}

        response = await self.client.chat.complete_async(**params)
        
        if structured_output:
            try:
                content_text, _ = self._extract_content(response.choices[0].message.content)
                if content_text:
                    parsed = structured_output.model_validate_json(content_text)
                else:
                    parsed = structured_output()

                content = parsed.model_dump() if hasattr(parsed, "model_dump") else str(parsed)
                thinking_tokens = None
                if hasattr(response.usage, "completion_tokens_details") and response.usage.completion_tokens_details:
                    thinking_tokens = getattr(
                        response.usage.completion_tokens_details, "reasoning_tokens", None
                    ) or getattr(
                        response.usage.completion_tokens_details, "thinking_tokens", None
                    )
                usage = TokenUsage(
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens,
                    thinking_tokens=thinking_tokens,
                )
                return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content) if isinstance(content, dict) else content, usage=usage)
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse structured output: {e}")

        return self._process_response(response)

    @overload
    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> Iterator[LLMStreamEvent]:
        ...

    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> Iterator[LLMStreamEvent]:
        mistral_messages = self._convert_messages(messages)
        mistral_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": mistral_messages,
            **self.kwargs
        }
        
        if mistral_tools:
            params["tools"] = mistral_tools
        
        if self.temperature is not None:
            params["temperature"] = self.temperature
        
        if json_mode:
            params["response_format"] = {"type": "json_object"}
        
        response = self.client.chat.stream(**params)
        
        # Accumulators for streamed tool calls
        tool_call_id = None
        tool_call_name = None
        tool_call_args = ""
        usage = None
        
        text_started = False
        think_started = False

        for chunk in response:
            if hasattr(chunk, 'data') and hasattr(chunk.data, 'choices') and chunk.data.choices:
                delta = chunk.data.choices[0].delta
                if hasattr(delta, 'content') and delta.content:
                    text, thinking = self._extract_content(delta.content)
                    if thinking:
                        if not think_started:
                            think_started = True
                            yield LLMStreamEvent(type=LLMStreamEventType.THINK_START)
                        yield LLMStreamEvent(type=LLMStreamEventType.THINK_DELTA, content=thinking)
                    if text:
                        if think_started:
                            yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
                            think_started = False
                        if not text_started:
                            text_started = True
                            yield LLMStreamEvent(type=LLMStreamEventType.TEXT_START)
                        yield LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content=text)

                # Accumulate tool call deltas
                if hasattr(delta, 'tool_calls') and delta.tool_calls:
                    tc_delta = delta.tool_calls[0]
                    if hasattr(tc_delta, 'id') and tc_delta.id:
                        tool_call_id = tc_delta.id
                    if hasattr(tc_delta, 'function') and tc_delta.function:
                        if tc_delta.function.name:
                            tool_call_name = tc_delta.function.name
                        if tc_delta.function.arguments:
                            tool_call_args += tc_delta.function.arguments
            
            # Track usage
            if hasattr(chunk, 'data') and hasattr(chunk.data, 'usage') and chunk.data.usage:
                usage_data = chunk.data.usage
                thinking_tokens = None
                if hasattr(usage_data, "completion_tokens_details") and usage_data.completion_tokens_details:
                    thinking_tokens = getattr(
                        usage_data.completion_tokens_details, "reasoning_tokens", None
                    ) or getattr(
                        usage_data.completion_tokens_details, "thinking_tokens", None
                    )
                usage = TokenUsage(
                    prompt_tokens=usage_data.prompt_tokens,
                    completion_tokens=usage_data.completion_tokens,
                    total_tokens=usage_data.total_tokens,
                    thinking_tokens=thinking_tokens,
                )
        
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
        mistral_messages = self._convert_messages(messages)
        mistral_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._model,
            "messages": mistral_messages,
            **self.kwargs
        }
        
        if mistral_tools:
            params["tools"] = mistral_tools
        
        if self.temperature is not None:
            params["temperature"] = self.temperature
        
        if json_mode:
            params["response_format"] = {"type": "json_object"}
        
        response = await self.client.chat.stream_async(**params)
        
        # Accumulators for streamed tool calls
        tool_call_id = None
        tool_call_name = None
        tool_call_args = ""
        usage = None
        
        text_started = False
        think_started = False

        async for chunk in response:
            if hasattr(chunk, 'data') and hasattr(chunk.data, 'choices') and chunk.data.choices:
                delta = chunk.data.choices[0].delta
                if hasattr(delta, 'content') and delta.content:
                    text, thinking = self._extract_content(delta.content)
                    if thinking:
                        if not think_started:
                            think_started = True
                            yield LLMStreamEvent(type=LLMStreamEventType.THINK_START)
                        yield LLMStreamEvent(type=LLMStreamEventType.THINK_DELTA, content=thinking)
                    if text:
                        if think_started:
                            yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
                            think_started = False
                        if not text_started:
                            text_started = True
                            yield LLMStreamEvent(type=LLMStreamEventType.TEXT_START)
                        yield LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content=text)

                # Accumulate tool call deltas
                if hasattr(delta, 'tool_calls') and delta.tool_calls:
                    tc_delta = delta.tool_calls[0]
                    if hasattr(tc_delta, 'id') and tc_delta.id:
                        tool_call_id = tc_delta.id
                    if hasattr(tc_delta, 'function') and tc_delta.function:
                        if tc_delta.function.name:
                            tool_call_name = tc_delta.function.name
                        if tc_delta.function.arguments:
                            tool_call_args += tc_delta.function.arguments
            
            # Track usage
            if hasattr(chunk, 'data') and hasattr(chunk.data, 'usage') and chunk.data.usage:
                usage_data = chunk.data.usage
                thinking_tokens = None
                if hasattr(usage_data, "completion_tokens_details") and usage_data.completion_tokens_details:
                    thinking_tokens = getattr(
                        usage_data.completion_tokens_details, "reasoning_tokens", None
                    ) or getattr(
                        usage_data.completion_tokens_details, "thinking_tokens", None
                    )
                usage = TokenUsage(
                    prompt_tokens=usage_data.prompt_tokens,
                    completion_tokens=usage_data.completion_tokens,
                    total_tokens=usage_data.total_tokens,
                    thinking_tokens=thinking_tokens,
                )
        
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

    def get_metadata(self) -> Metadata:
        # Context windows vary by model
        context_window = 128000  # Default
        
        if "large" in self._model:
            context_window = 128000
        elif "medium" in self._model:
            context_window = 32000
        elif "small" in self._model:
            context_window = 32000
        elif "codestral" in self._model:
            context_window = 32000
        
        return Metadata(
            name=self._model,
            context_window=context_window,
            owned_by="mistral"
        )
