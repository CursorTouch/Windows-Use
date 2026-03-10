import os
import json
import logging
from typing import Iterator, AsyncIterator, List, Optional, Any, Union, overload
from anthropic import Anthropic, AsyncAnthropic
from pydantic import BaseModel
from windows_use.providers.base import BaseChatLLM
from windows_use.providers.views import TokenUsage, Metadata
from windows_use.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ImageMessage, ToolMessage
from windows_use.tools import Tool
from windows_use.providers.events import LLMEvent, LLMEventType, LLMStreamEvent, LLMStreamEventType, ToolCall, Thinking

logger = logging.getLogger(__name__)

class ChatAnthropic(BaseChatLLM):
    """
    Anthropic LLM implementation following the BaseChatLLM protocol.
    """
    
    def __init__(
        self,
        model: str = "claude-3-5-sonnet-latest",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 600.0,
        max_retries: int = 2,
        temperature: Optional[float] = None,
        thinking_budget: Optional[int] = None,
        max_tokens: int = 4096,
        enable_prompt_caching: bool = True,
        cache_system_prompt: bool = True,
        cache_tools: bool = True,
        cache_recent_messages: int = 2,  # Number of recent messages to cache
        **kwargs
    ):
        """
        Initialize the Anthropic LLM with prompt caching and extended thinking support.

        Args:
            model (str): The model name to use.
            api_key (str, optional): Anthropic API key.
            base_url (str, optional): Base URL for the API.
            timeout (float): Request timeout in seconds.
            max_retries (int): Maximum number of retries.
            temperature (float, optional): Sampling temperature. Ignored when thinking is enabled
                (Anthropic requires temperature=1 for extended thinking).
            thinking_budget (int, optional): Token budget for extended thinking. Set to enable
                extended thinking (minimum 1024). Must be less than max_tokens.
                When set, temperature is automatically ignored.
            max_tokens (int): Maximum output tokens. When thinking is enabled, this should be
                larger than thinking_budget (defaults to thinking_budget + 4096 if too small).
            enable_prompt_caching (bool): Enable prompt caching feature.
            cache_system_prompt (bool): Add cache control to system prompt.
            cache_tools (bool): Add cache control to tools.
            cache_recent_messages (int): Number of recent messages to mark for caching.
            **kwargs: Additional arguments for messages.create.
        """
        self._model = model
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.base_url = base_url or os.environ.get("ANTHROPIC_BASE_URL")
        self.temperature = temperature
        self.thinking_budget = thinking_budget
        self.max_tokens = max_tokens
        self.enable_prompt_caching = enable_prompt_caching
        self.cache_system_prompt = cache_system_prompt
        self.cache_tools = cache_tools
        self.cache_recent_messages = cache_recent_messages

        # Auto-adjust max_tokens when thinking is enabled
        if self.thinking_budget is not None:
            if self.thinking_budget < 1024:
                logger.warning(
                    f"thinking_budget ({self.thinking_budget}) is below the minimum of 1024. "
                    f"Setting to 1024."
                )
                self.thinking_budget = 1024
            if self.max_tokens <= self.thinking_budget:
                self.max_tokens = self.thinking_budget + 4096
                logger.info(
                    f"max_tokens auto-adjusted to {self.max_tokens} "
                    f"(thinking_budget={self.thinking_budget} + 4096 for response)."
                )
            if self.temperature is not None:
                logger.warning(
                    "temperature is ignored when extended thinking is enabled "
                    "(Anthropic requires temperature=1)."
                )
        
        self.client = Anthropic(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.aclient = AsyncAnthropic(
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
        return "anthropic"

    def _convert_messages(self, messages: List[BaseMessage]) -> tuple[Optional[Union[str, List[dict]]], List[dict]]:
        """
        Convert BaseMessage objects to Anthropic-compatible message dictionaries.
        Returns (system_prompt, messages).
        
        Adds cache control breakpoints based on configuration.
        """
        anthropic_messages = []
        system_prompt = None
        
        for msg in messages:
            if isinstance(msg, SystemMessage):
                system_prompt = msg.content
            elif isinstance(msg, HumanMessage):
                anthropic_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, ImageMessage):
                content = []
                if msg.content:
                    content.append({"type": "text", "text": msg.content})
                
                b64_imgs = msg.convert_images(format="base64")
                for b64 in b64_imgs:
                    content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": msg.mime_type,
                            "data": b64
                        }
                    })
                anthropic_messages.append({"role": "user", "content": content})
            elif isinstance(msg, AIMessage):
                content = []
                if msg.thinking:
                    content.append({
                        "type": "thinking", 
                        "thinking": msg.thinking, 
                        "signature": msg.thinking_signature
                    })
                if msg.content:
                    content.append({"type": "text", "text": msg.content})
                anthropic_messages.append({"role": "assistant", "content": content if content else ""})
            elif isinstance(msg, ToolMessage):
                # Build content blocks for the assistant turn
                content_blocks = []
                if msg.thinking:
                    content_blocks.append({
                        "type": "thinking",
                        "thinking": msg.thinking,
                        "signature": msg.thinking_signature
                    })
                content_blocks.append({
                    "type": "tool_use",
                    "id": msg.id,
                    "name": msg.name,
                    "input": msg.params
                })
                
                # Anthropic requires a tool_use block followed by a tool_result block
                if anthropic_messages and anthropic_messages[-1]["role"] == "assistant":
                    last_content = anthropic_messages[-1]["content"]
                    if isinstance(last_content, str):
                        last_content = [{"type": "text", "text": last_content}] if last_content else []
                    if isinstance(last_content, list):
                        last_content.extend(content_blocks)
                    anthropic_messages[-1]["content"] = last_content
                else:
                    anthropic_messages.append({
                        "role": "assistant",
                        "content": content_blocks
                    })
                
                # Add the tool result
                anthropic_messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": msg.id,
                        "content": msg.content or ""
                    }]
                })
        
        # Apply prompt caching to system prompt
        if system_prompt and self.enable_prompt_caching and self.cache_system_prompt:
            system_prompt = [
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        
        # Apply prompt caching to recent messages
        if self.enable_prompt_caching and self.cache_recent_messages > 0 and anthropic_messages:
            # Cache the last N user messages (caching works best on user turns)
            user_message_indices = [
                i for i, msg in enumerate(anthropic_messages) 
                if msg["role"] == "user"
            ]
            
            # Get the indices to cache (last N user messages)
            indices_to_cache = user_message_indices[-self.cache_recent_messages:]
            
            for idx in indices_to_cache:
                msg = anthropic_messages[idx]
                content = msg["content"]
                
                # Convert string content to list format for cache control
                if isinstance(content, str):
                    content = [{"type": "text", "text": content}]
                
                # Add cache control to the last content block
                if isinstance(content, list) and len(content) > 0:
                    # Only add cache control to the last block in the message
                    content[-1]["cache_control"] = {"type": "ephemeral"}
                    msg["content"] = content
        
        return system_prompt, anthropic_messages

    def _build_params(self, anthropic_messages: List[dict], system_prompt: Any, anthropic_tools: Optional[List[dict]]) -> dict:
        """Build the common API parameters for all invoke/stream methods."""
        params = {
            "model": self._model,
            "messages": anthropic_messages,
            "max_tokens": self.max_tokens,
            **self.kwargs
        }

        if system_prompt is not None:
            params["system"] = system_prompt

        if anthropic_tools:
            params["tools"] = anthropic_tools

        # Extended thinking configuration
        if self.thinking_budget is not None:
            params["thinking"] = {
                "type": "enabled",
                "budget_tokens": self.thinking_budget,
            }
            # Temperature must not be set when thinking is enabled
        elif self.temperature is not None:
            params["temperature"] = self.temperature

        return params

    def _convert_tools(self, tools: List[Tool]) -> List[dict]:
        """
        Convert Tool objects to Anthropic-compatible tool definitions.
        Adds cache control to tools if enabled.
        """
        tool_defs = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.json_schema["parameters"]
            }
            for tool in tools
        ]
        
        # Add cache control to the last tool definition
        if self.enable_prompt_caching and self.cache_tools and tool_defs:
            tool_defs[-1]["cache_control"] = {"type": "ephemeral"}
        
        return tool_defs

    def _process_response(self, response: Any) -> LLMEvent:
        """
        Process Anthropic API response into AIMessage or ToolMessage.
        Includes cache usage metrics.
        """
        content_blocks = response.content
        usage_data = response.usage

        # Extract cache metrics
        cache_creation_tokens = getattr(usage_data, 'cache_creation_input_tokens', None) or 0
        cache_read_tokens = getattr(usage_data, 'cache_read_input_tokens', None) or 0

        usage = TokenUsage(
            prompt_tokens=usage_data.input_tokens,
            completion_tokens=usage_data.output_tokens,
            total_tokens=usage_data.input_tokens + usage_data.output_tokens,
            thinking_tokens=getattr(usage_data, "thinking_tokens", None),
            cache_creation_input_tokens=cache_creation_tokens or None,
            cache_read_input_tokens=cache_read_tokens or None,
        )

        # Log cache usage
        if cache_creation_tokens > 0:
            logger.debug(f"Cache created: {cache_creation_tokens} tokens")
        if cache_read_tokens > 0:
            logger.debug(f"Cache hit: {cache_read_tokens} tokens (saved ~{cache_read_tokens * 0.9:.0f} tokens worth of cost)")

        text_content = ""
        thinking_parts: list[str] = []
        thinking_signature = None
        tool_message = None

        for block in content_blocks:
            if block.type == "text":
                text_content += block.text
            elif block.type == "thinking":
                thinking_parts.append(block.thinking)
                thinking_signature = getattr(block, "signature", None)
            elif block.type == "tool_use":
                # Take the first tool use as per Agent logic
                if not tool_message:
                    tool_message = True
                    thinking = Thinking(
                        content="\n".join(thinking_parts) if thinking_parts else None,
                        signature=thinking_signature,
                    ) if thinking_parts or thinking_signature else None
                    return LLMEvent(
                        type=LLMEventType.TOOL_CALL,
                        tool_call=ToolCall(
                            id=block.id,
                            name=block.name,
                            params=block.input
                        ),
                        thinking=thinking,
                        usage=usage
                    )

        thinking = Thinking(
            content="\n".join(thinking_parts) if thinking_parts else None,
            signature=thinking_signature,
        ) if thinking_parts or thinking_signature else None
        return LLMEvent(type=LLMEventType.TEXT, content=text_content, thinking=thinking, usage=usage)

    @overload
    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ...

    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        system_prompt, anthropic_messages = self._convert_messages(messages)
        anthropic_tools = self._convert_tools(tools) if tools else None
        params = self._build_params(anthropic_messages, system_prompt, anthropic_tools)
        
        if structured_output:
            # Simulate structured output via tool calling
            structured_tool = {
                "name": "record_result",
                "description": f"Record the structured result: {structured_output.__name__}",
                "input_schema": structured_output.model_json_schema()
            }
            
            # Add cache control to structured output tool if caching enabled
            if self.enable_prompt_caching and self.cache_tools:
                structured_tool["cache_control"] = {"type": "ephemeral"}
            
            params["tools"] = [structured_tool]
            params["tool_choice"] = {"type": "tool", "name": "record_result"}
            # Forced tool_choice is incompatible with extended thinking
            params.pop("thinking", None)
            
            response = self.client.messages.create(**params)
            tool_use = next(b for b in response.content if b.type == "tool_use")
            parsed = structured_output(**tool_use.input)
            
            # Extract cache metrics
            cache_creation_tokens = getattr(response.usage, 'cache_creation_input_tokens', None) or 0
            cache_read_tokens = getattr(response.usage, 'cache_read_input_tokens', None) or 0
            
            usage = TokenUsage(
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens,
                thinking_tokens=getattr(response.usage, "thinking_tokens", None),
                cache_creation_input_tokens=cache_creation_tokens or None,
                cache_read_input_tokens=cache_read_tokens or None,
            )

            content = parsed.model_dump() if hasattr(parsed, "model_dump") else str(parsed)
            return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content) if isinstance(content, dict) else content, usage=usage)

        response = self.client.messages.create(**params)
        return self._process_response(response)

    @overload
    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ...

    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        system_prompt, anthropic_messages = self._convert_messages(messages)
        anthropic_tools = self._convert_tools(tools) if tools else None
        params = self._build_params(anthropic_messages, system_prompt, anthropic_tools)
        
        if structured_output:
            structured_tool = {
                "name": "record_result",
                "description": f"Record the structured result: {structured_output.__name__}",
                "input_schema": structured_output.model_json_schema()
            }
            
            if self.enable_prompt_caching and self.cache_tools:
                structured_tool["cache_control"] = {"type": "ephemeral"}
            
            params["tools"] = [structured_tool]
            params["tool_choice"] = {"type": "tool", "name": "record_result"}
            # Forced tool_choice is incompatible with extended thinking
            params.pop("thinking", None)
            
            response = await self.aclient.messages.create(**params)
            tool_use = next(b for b in response.content if b.type == "tool_use")
            parsed = structured_output(**tool_use.input)
            
            cache_creation_tokens = getattr(response.usage, 'cache_creation_input_tokens', None) or 0
            cache_read_tokens = getattr(response.usage, 'cache_read_input_tokens', None) or 0
            
            usage = TokenUsage(
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens,
                thinking_tokens=getattr(response.usage, "thinking_tokens", None),
                cache_creation_input_tokens=cache_creation_tokens or None,
                cache_read_input_tokens=cache_read_tokens or None,
            )

            content = parsed.model_dump() if hasattr(parsed, "model_dump") else str(parsed)
            return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content) if isinstance(content, dict) else content, usage=usage)

        response = await self.aclient.messages.create(**params)
        return self._process_response(response)

    @overload
    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> Iterator[LLMStreamEvent]:
        ...

    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> Iterator[LLMStreamEvent]:
        system_prompt, anthropic_messages = self._convert_messages(messages)
        anthropic_tools = self._convert_tools(tools) if tools else None
        params = self._build_params(anthropic_messages, system_prompt, anthropic_tools)
        
        text_started = False
        think_started = False
        usage = None

        with self.client.messages.stream(**params) as stream:
            for event in stream:
                if event.type == "thinking":
                    if not think_started:
                        think_started = True
                        yield LLMStreamEvent(type=LLMStreamEventType.THINK_START)
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_DELTA, content=event.thinking)
                elif event.type == "text":
                    if think_started:
                        yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
                        think_started = False
                    if not text_started:
                        text_started = True
                        yield LLMStreamEvent(type=LLMStreamEventType.TEXT_START)
                    yield LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content=event.text)

            if think_started:
                yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)

            # Extract usage and thinking (with signature) from final message
            final_message = stream.get_final_message()
            if final_message.usage:
                cache_creation = getattr(final_message.usage, 'cache_creation_input_tokens', None) or 0
                cache_read = getattr(final_message.usage, 'cache_read_input_tokens', None) or 0
                usage = TokenUsage(
                    prompt_tokens=final_message.usage.input_tokens,
                    completion_tokens=final_message.usage.output_tokens,
                    total_tokens=final_message.usage.input_tokens + final_message.usage.output_tokens,
                    thinking_tokens=getattr(final_message.usage, "thinking_tokens", None),
                    cache_creation_input_tokens=cache_creation or None,
                    cache_read_input_tokens=cache_read or None,
                )

            final_content = self._process_response(final_message)
            if final_content.type == LLMEventType.TOOL_CALL:
                yield LLMStreamEvent(
                    type=LLMStreamEventType.TOOL_CALL,
                    tool_call=final_content.tool_call,
                    thinking=final_content.thinking,
                    usage=final_content.usage
                )
            elif text_started:
                yield LLMStreamEvent(
                    type=LLMStreamEventType.TEXT_END,
                    thinking=final_content.thinking,
                    usage=usage
                )

    @overload
    async def astream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> AsyncIterator[LLMStreamEvent]:
        ...

    async def astream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> AsyncIterator[LLMStreamEvent]:
        system_prompt, anthropic_messages = self._convert_messages(messages)
        anthropic_tools = self._convert_tools(tools) if tools else None
        params = self._build_params(anthropic_messages, system_prompt, anthropic_tools)
        
        text_started = False
        think_started = False
        usage = None

        async with self.aclient.messages.stream(**params) as stream:
            async for event in stream:
                if event.type == "thinking":
                    if not think_started:
                        think_started = True
                        yield LLMStreamEvent(type=LLMStreamEventType.THINK_START)
                    yield LLMStreamEvent(type=LLMStreamEventType.THINK_DELTA, content=event.thinking)
                elif event.type == "text":
                    if think_started:
                        yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)
                        think_started = False
                    if not text_started:
                        text_started = True
                        yield LLMStreamEvent(type=LLMStreamEventType.TEXT_START)
                    yield LLMStreamEvent(type=LLMStreamEventType.TEXT_DELTA, content=event.text)

            if think_started:
                yield LLMStreamEvent(type=LLMStreamEventType.THINK_END)

            # Extract usage from final message
            final_message = await stream.get_final_message()
            if final_message.usage:
                cache_creation = getattr(final_message.usage, 'cache_creation_input_tokens', None) or 0
                cache_read = getattr(final_message.usage, 'cache_read_input_tokens', None) or 0
                usage = TokenUsage(
                    prompt_tokens=final_message.usage.input_tokens,
                    completion_tokens=final_message.usage.output_tokens,
                    total_tokens=final_message.usage.input_tokens + final_message.usage.output_tokens,
                    thinking_tokens=getattr(final_message.usage, "thinking_tokens", None),
                    cache_creation_input_tokens=cache_creation or None,
                    cache_read_input_tokens=cache_read or None,
                )

            final_content = self._process_response(final_message)
            if final_content.type == LLMEventType.TOOL_CALL:
                yield LLMStreamEvent(
                    type=LLMStreamEventType.TOOL_CALL,
                    tool_call=final_content.tool_call,
                    thinking=final_content.thinking,
                    usage=final_content.usage
                )
            elif text_started:
                yield LLMStreamEvent(
                    type=LLMStreamEventType.TEXT_END,
                    thinking=final_content.thinking,
                    usage=usage
                )

    def get_metadata(self) -> Metadata:
        return Metadata(
            name=self._model,
            context_window=200000,
            owned_by="anthropic"
        )

    def get_cache_stats(self) -> dict:
        """
        Return information about the current caching configuration.
        
        Returns:
            dict: Cache configuration details
        """
        return {
            "enabled": self.enable_prompt_caching,
            "cache_system_prompt": self.cache_system_prompt,
            "cache_tools": self.cache_tools,
            "cache_recent_messages": self.cache_recent_messages,
            "model": self._model
        }
