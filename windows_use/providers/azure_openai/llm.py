import os
import json
import logging
from typing import Iterator, AsyncIterator, List, Optional, Any, Union, overload
from openai import AzureOpenAI, AsyncAzureOpenAI
from pydantic import BaseModel
from windows_use.providers.base import BaseChatLLM
from windows_use.providers.views import TokenUsage, Metadata
from windows_use.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ImageMessage, ToolMessage
from windows_use.tools import Tool
from windows_use.providers.events import LLMEvent, LLMEventType, LLMStreamEvent, LLMStreamEventType, ToolCall, Thinking

logger = logging.getLogger(__name__)

class ChatAzureOpenAI(BaseChatLLM):
    """
    Azure OpenAI LLM implementation following the BaseChatLLM protocol.
    """
    
    def __init__(
        self,
        deployment_name: str,
        api_key: Optional[str] = None,
        azure_endpoint: Optional[str] = None,
        api_version: str = "2024-02-01",
        timeout: float = 600.0,
        max_retries: int = 2,
        temperature: Optional[float] = None,
        **kwargs
    ):
        """
        Initialize the Azure OpenAI LLM.

        Args:
            deployment_name (str): The Azure deployment name to use.
            api_key (str, optional): Azure API key. Defaults to AZURE_OPENAI_API_KEY.
            azure_endpoint (str, optional): Azure endpoint URL. Defaults to AZURE_OPENAI_ENDPOINT.
            api_version (str): Azure API version.
            timeout (float): Request timeout.
            max_retries (int): Maximum retries.
            temperature (float, optional): Sampling temperature.
            **kwargs: Additional arguments for chat completions.
        """
        self._deployment = deployment_name
        self.api_key = api_key or os.environ.get("AZURE_OPENAI_API_KEY")
        self.azure_endpoint = azure_endpoint or os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.temperature = temperature
        
        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.azure_endpoint,
            api_version=api_version,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.aclient = AsyncAzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.azure_endpoint,
            api_version=api_version,
            timeout=timeout,
            max_retries=max_retries,
        )
        self.kwargs = kwargs

    @property
    def model_name(self) -> str:
        return self._deployment

    @property
    def provider(self) -> str:
        return "azure_openai"

    def _is_reasoning_model(self) -> bool:
        """Check if the deployment is a reasoning model (o-series: o1, o3, o4, etc.)."""
        return self._deployment.startswith(("o1", "o3", "o4"))

    def _convert_messages(self, messages: List[BaseMessage]) -> List[dict]:
        """
        Convert BaseMessage objects to Azure-compatible message dictionaries.
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
                if self._is_reasoning_model() and getattr(msg, "thinking", None):
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
        Convert Tool objects to Azure-compatible tool definitions.
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
        Process Azure API response into LLMEvent.
        """
        choice = response.choices[0]
        message = choice.message
        usage_data = response.usage

        # Capture reasoning tokens if available (o-series models)
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

        # Extract thinking/reasoning content (for o-series models)
        thinking = None
        if self._is_reasoning_model():
            if hasattr(message, 'reasoning_content'):
                thinking = message.reasoning_content
            elif hasattr(choice, 'reasoning_content'):
                thinking = choice.reasoning_content

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

        # Optional: We could pass thinking back in the event if we want, but currently TEXT_END is just content.
        # If we need thinking attached to the final message, we might need a THINK_END event before this, or just attach it.
        # Following OpenAI pattern, we probably don't need to return it here, but stream will handle it.

        return content

    @overload
    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ...

    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        openai_messages = self._convert_messages(messages)
        openai_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._deployment,
            "messages": openai_messages,
            **self.kwargs
        }
        
        # Only add tools if they exist
        if openai_tools:
            params["tools"] = openai_tools
        
        # Reasoning models don't support temperature
        if self.temperature is not None and not self._is_reasoning_model():
            params["temperature"] = self.temperature
        
        if structured_output:
            # Use beta parse endpoint for structured outputs
            response = self.client.beta.chat.completions.parse(
                **params,
                response_format=structured_output
            )

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

            parsed = response.choices[0].message.parsed
            content_dump = parsed.model_dump()
            return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content_dump) if isinstance(content_dump, dict) else str(content_dump))
        
        if json_mode:
            params["response_format"] = {"type": "json_object"}
            
        response = self.client.chat.completions.create(**params)
        return self._process_response(response)

    @overload
    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ...

    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        openai_messages = self._convert_messages(messages)
        openai_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._deployment,
            "messages": openai_messages,
            **self.kwargs
        }
        
        if openai_tools:
            params["tools"] = openai_tools
        
        # Reasoning models don't support temperature
        if self.temperature is not None and not self._is_reasoning_model():
            params["temperature"] = self.temperature
        
        if structured_output:
            response = await self.aclient.beta.chat.completions.parse(
                **params,
                response_format=structured_output
            )

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

            parsed = response.choices[0].message.parsed
            content_dump = parsed.model_dump()
            return LLMEvent(type=LLMEventType.TEXT, content=json.dumps(content_dump) if isinstance(content_dump, dict) else str(content_dump), usage=usage)
        
        if json_mode:
            params["response_format"] = {"type": "json_object"}
            
        response = await self.aclient.chat.completions.create(**params)
        return self._process_response(response)

    @overload
    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> Iterator[LLMStreamEvent]:
        ...

    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> Iterator[LLMStreamEvent]:
        openai_messages = self._convert_messages(messages)
        openai_tools = self._convert_tools(tools) if tools else None
        
        params = {
            "model": self._deployment,
            "messages": openai_messages,
            "stream": True,
            "stream_options": {"include_usage": True},
            **self.kwargs
        }
        
        if openai_tools:
            params["tools"] = openai_tools
        
        if self.temperature is not None and not self._is_reasoning_model():
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
        usage = None

        for chunk in response:
            if not chunk.choices:
                if chunk.usage:
                    thinking_tokens = None
                    if hasattr(chunk.usage, "completion_tokens_details") and chunk.usage.completion_tokens_details:
                        thinking_tokens = getattr(
                            chunk.usage.completion_tokens_details, "reasoning_tokens", None
                        ) or getattr(
                            chunk.usage.completion_tokens_details, "thinking_tokens", None
                        )
                    usage = TokenUsage(
                        prompt_tokens=chunk.usage.prompt_tokens,
                        completion_tokens=chunk.usage.completion_tokens,
                        total_tokens=chunk.usage.total_tokens,
                        thinking_tokens=thinking_tokens,
                    )
                continue
            
            delta = chunk.choices[0].delta
            
            # Handle reasoning content for o-series models
            if self._is_reasoning_model() and hasattr(delta, 'reasoning_content') and delta.reasoning_content:
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
                )
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
            "model": self._deployment,
            "messages": openai_messages,
            "stream": True,
            "stream_options": {"include_usage": True},
            **self.kwargs
        }
        
        if openai_tools:
            params["tools"] = openai_tools
        
        if self.temperature is not None and not self._is_reasoning_model():
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
        usage = None

        async for chunk in response:
            if not chunk.choices:
                if chunk.usage:
                    thinking_tokens = None
                    if hasattr(chunk.usage, "completion_tokens_details") and chunk.usage.completion_tokens_details:
                        thinking_tokens = getattr(
                            chunk.usage.completion_tokens_details, "reasoning_tokens", None
                        ) or getattr(
                            chunk.usage.completion_tokens_details, "thinking_tokens", None
                        )
                    usage = TokenUsage(
                        prompt_tokens=chunk.usage.prompt_tokens,
                        completion_tokens=chunk.usage.completion_tokens,
                        total_tokens=chunk.usage.total_tokens,
                        thinking_tokens=thinking_tokens,
                    )
                continue
            
            delta = chunk.choices[0].delta
            
            if self._is_reasoning_model() and hasattr(delta, 'reasoning_content') and delta.reasoning_content:
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
            name=self._deployment,
            context_window=128000,
            owned_by="azure_openai"
        )
