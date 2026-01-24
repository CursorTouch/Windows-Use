from anthropic.types import Message,MessageParam,ImageBlockParam,Base64ImageSourceParam,TextBlockParam,CacheControlEphemeralParam,ToolUseBlockParam,ToolResultBlockParam
from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage, ToolMessage
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage, ModelMetadata
from anthropic import Anthropic,AsyncAnthropic
from typing import Iterator, AsyncIterator
from windows_use.llms.base import BaseChatLLM
from windows_use.tool.service import Tool
from dataclasses import dataclass
from pydantic import BaseModel
from httpx import Client
import json
import os

@dataclass
class ChatAnthropic(BaseChatLLM):
    def __init__(self, model: str, api_key: str|None=None, thinking_budget:int=-1, temperature: float = 0.7, max_tokens: int = 8192, auth_token: str | None = None, base_url: str | None = None, timeout: float | None = None, max_retries: int = 3, default_headers: dict[str, str] | None = None, default_query: dict[str, object] | None = None, http_client: Client | None = None, strict_response_validation: bool = False):
        self.model = model
        if not api_key and not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY is not set")
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.auth_token = auth_token
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.base_url = base_url
        self.thinking_budget=thinking_budget
        self.timeout = timeout
        self.max_retries = max_retries
        self.default_headers = default_headers
        self.default_query = default_query
        self.http_client = http_client
        self.strict_response_validation = strict_response_validation

    @property
    def client(self):
        return Anthropic(**{
            "api_key": self.api_key or os.getenv("ANTHROPIC_API_KEY"),
            "auth_token": self.auth_token,
            "base_url": self.base_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "default_headers": self.default_headers,
            "default_query": self.default_query,
            "http_client": self.http_client,
            "_strict_response_validation": self.strict_response_validation
        })
    
    @property
    def async_client(self):
        return AsyncAnthropic(**{
            "api_key": self.api_key,
            "auth_token": self.auth_token,
            "base_url": self.base_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "default_headers": self.default_headers,
            "default_query": self.default_query,
            "http_client": self.http_client,
            "_strict_response_validation": self.strict_response_validation
        })

    @property
    def provider(self):
        return "anthropic"

    @property
    def model_name(self):
        return self.model
    
    def serialize_messages(self, messages: list[BaseMessage]):
        system_instruction = None
        serialized = []
        for message in messages:
            if isinstance(message, SystemMessage):
                system_instruction = [TextBlockParam(
                    type="text",text=message.content,
                    cache_control=CacheControlEphemeralParam(type="ephemeral",ttl='5m')
                )]
            elif isinstance(message, HumanMessage):
                content=[TextBlockParam(type="text",text=message.content)]
                serialized.append(MessageParam(role="user",content=content))
            elif isinstance(message, AIMessage):
                content=[TextBlockParam(type="text",text=message.content)]
                serialized.append(MessageParam(role="assistant",content=content))
            elif isinstance(message, ToolMessage):
                # 1. The Assistant's Tool Use Request
                tool_use_block = ToolUseBlockParam(
                    type="tool_use",
                    id=message.id,
                    name=message.name,
                    input=message.params
                )
                serialized.append(MessageParam(role="assistant", content=[tool_use_block]))
                
                # 2. The User's Tool Result (if executed)
                if message.content is not None:
                    tool_result_block = ToolResultBlockParam(
                        type="tool_result",
                        tool_use_id=message.id,
                        content=str(message.content)
                    )
                    serialized.append(MessageParam(role="user", content=[tool_result_block]))

            elif isinstance(message, ImageMessage):
                message.scale_images(scale=0.7)
                images=[f"data:{message.mime_type};base64,{image}" for image in message.convert_images("base64")]
                content=[
                    TextBlockParam(type="text",text=message.content),
                    *[ImageBlockParam(type="image",source=Base64ImageSourceParam(
                        type="base64",data=image,media_type=message.mime_type
                    )) for image in images]
                ]
                serialized.append(MessageParam(role="user",content=content))
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")
        return system_instruction,serialized
    
    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None = None, json_mode: bool = False):
        system_instruction, messages = self.serialize_messages(messages)
        
        anthropic_tools = []
        if tools:
            for tool in tools:
                anthropic_tools.append({
                    "name": tool.json_schema["name"],
                    "description": tool.json_schema["description"],
                    "input_schema": tool.json_schema["parameters"]
                })

        completion = self.client.messages.create(
            max_tokens=self.max_tokens,
            model=self.model,
            system=system_instruction,
            messages=messages,
            tools=anthropic_tools if anthropic_tools else None,
            temperature=self.temperature,
        )

        if not isinstance(completion,Message):
            raise ValueError("Unexpected response type from Anthropic API")
        
        content = ""
        tool_message = None
        thinking = None
        
        for block in completion.content:
            if block.type == "text":
                content += block.text
            elif block.type == "tool_use":
                tool_message = ToolMessage(
                    id=block.id,
                    name=block.name,
                    params=block.input,
                    content=None
                )
        
        if tool_message:
            thinking = content
            response_content = tool_message
        else:
            response_content = AIMessage(content=content)

        return ChatLLMResponse(
            content=response_content,
            thinking=thinking,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage.input_tokens,
                completion_tokens=completion.usage.output_tokens,
                total_tokens=completion.usage.input_tokens+completion.usage.output_tokens
            )
        )

    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None = None, json_mode: bool = False):
        system_instruction, messages = self.serialize_messages(messages)

        anthropic_tools = []
        if tools:
            for tool in tools:
                anthropic_tools.append({
                    "name": tool.json_schema["name"],
                    "description": tool.json_schema["description"],
                    "input_schema": tool.json_schema["parameters"]
                })

        completion = await self.async_client.messages.create(
            max_tokens=self.max_tokens,
            model=self.model,
            system=system_instruction,
            messages=messages,
            tools=anthropic_tools if anthropic_tools else None,
            temperature=self.temperature,
        )

        if not isinstance(completion,Message):
            raise ValueError("Unexpected response type from Anthropic API")
        
        content = ""
        tool_message = None
        thinking = None
        
        for block in completion.content:
            if block.type == "text":
                content += block.text
            elif block.type == "tool_use":
                tool_message = ToolMessage(
                    id=block.id,
                    name=block.name,
                    params=block.input,
                    content=None
                )
        
        if tool_message:
            thinking = content
            response_content = tool_message
        else:
            response_content = AIMessage(content=content)

        return ChatLLMResponse(
            content=response_content,
            thinking=thinking,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage.input_tokens,
                completion_tokens=completion.usage.output_tokens,
                total_tokens=completion.usage.input_tokens+completion.usage.output_tokens
            )
        )

    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None = None, json_mode: bool = False) -> Iterator[ChatLLMResponse]:
        system_instruction, messages = self.serialize_messages(messages)
        anthropic_tools = []
        if tools:
            for tool in tools:
                anthropic_tools.append({
                    "name": tool.json_schema["name"],
                    "description": tool.json_schema["description"],
                    "input_schema": tool.json_schema["parameters"]
                })

        with self.client.messages.stream(
            max_tokens=self.max_tokens,
            model=self.model,
            system=system_instruction,
            messages=messages,
            tools=anthropic_tools if anthropic_tools else None,
            temperature=self.temperature,
        ) as stream:
            for event in stream:
                 if event.type == "content_block_delta" and event.delta.type == "text_delta":
                     yield ChatLLMResponse(content=AIMessage(content=event.delta.text))
                 # Add thinking support if Anthropic adds it in future or if using a specific beta
                 # Currently standard Anthropic stream doesn't separate thinking.

    async def astream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None = None, json_mode: bool = False) -> AsyncIterator[ChatLLMResponse]:
        system_instruction, messages = self.serialize_messages(messages)
        anthropic_tools = []
        if tools:
            for tool in tools:
                anthropic_tools.append({
                    "name": tool.json_schema["name"],
                    "description": tool.json_schema["description"],
                    "input_schema": tool.json_schema["parameters"]
                })
                
        async with self.async_client.messages.stream(
            max_tokens=self.max_tokens,
            model=self.model,
            system=system_instruction,
            messages=messages,
            tools=anthropic_tools if anthropic_tools else None,
            temperature=self.temperature,
        ) as stream:
            async for event in stream:
                if event.type == "content_block_delta" and event.delta.type == "text_delta":
                     yield ChatLLMResponse(content=AIMessage(content=event.delta.text))

    def get_model_specification(self):
        # response = self.client.models.retrieve(model_id=self.model)
        return ModelMetadata(name=self.model,context_window=200000,owned_by="anthropic")
