from cerebras.cloud.sdk.types.chat.completion_create_params import (
import os
    MessageSystemMessageRequestTyped, MessageUserMessageRequestTyped, MessageAssistantMessageRequestTyped,
    MessageSystemMessageRequestContentUnionMember1Typed, MessageAssistantMessageRequestContentUnionMember1Typed,
    MessageUserMessageRequestContentUnionMember1Typed
)
from cerebras.cloud.sdk.types.chat.completion_create_params import ResponseFormatResponseFormatJsonSchemaJsonSchemaTyped, ResponseFormatResponseFormatJsonSchemaTyped
from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage, ToolMessage
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage, ModelMetadata
from windows_use.llms.base import BaseChatLLM
from windows_use.tool.service import Tool
from cerebras.cloud.sdk import Cerebras, AsyncCerebras
from typing import Iterator, AsyncIterator
from dataclasses import dataclass
from pydantic import BaseModel
from httpx import Client
import json

@dataclass
class ChatCerebras(BaseChatLLM):
    def __init__(self, model: str, api_key: str|None=None, temperature: float = 0.7, base_url: str | None = None, timeout: float | None = None, max_retries: int = 3, default_headers: dict[str, str] | None = None, default_query: dict[str, object] | None = None, http_client: Client | None = None, strict_response_validation: bool = False, warm_tcp_connection: bool = True):
        self.model = model
        self.api_key = api_key or os.getenv("CEREBRAS_API_KEY")
        self.temperature = temperature
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.default_headers = default_headers
        self.default_query = default_query
        self.http_client = http_client
        self.strict_response_validation = strict_response_validation
        self.warm_tcp_connection = warm_tcp_connection

    @property
    def client(self) -> Cerebras:
        return Cerebras(**{
            "api_key": self.api_key,
            "base_url": self.base_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "default_headers": self.default_headers,
            "default_query": self.default_query,
            "http_client": self.http_client,
            "_strict_response_validation": self.strict_response_validation,
            "warm_tcp_connection": self.warm_tcp_connection
        })

    @property
    def async_client(self) -> AsyncCerebras:
        return AsyncCerebras(**{
            "api_key": self.api_key,
            "base_url": self.base_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "default_headers": self.default_headers,
            "default_query": self.default_query,
            "http_client": self.http_client,
            "_strict_response_validation": self.strict_response_validation,
            "warm_tcp_connection": self.warm_tcp_connection
        })

    @property
    def provider(self) -> str:
        return "cerebras"
    
    @property
    def model_name(self) -> str:
        return self.model
    
    def serialize_messages(self, messages: list[BaseMessage]):
        serialized = []
        for message in messages:
            if isinstance(message, SystemMessage):
                content = [MessageSystemMessageRequestContentUnionMember1Typed(type="text", text=message.content)]
                serialized.append(MessageSystemMessageRequestTyped(role="system", content=content))
            elif isinstance(message, HumanMessage):
                content = [MessageUserMessageRequestContentUnionMember1Typed(type="text", text=message.content)]
                serialized.append(MessageUserMessageRequestTyped(role="user", content=content))
            elif isinstance(message, AIMessage):
                content = [MessageAssistantMessageRequestContentUnionMember1Typed(type="text", text=message.content)]
                serialized.append(MessageAssistantMessageRequestTyped(role="assistant", content=content))
            elif isinstance(message, ToolMessage):
                 serialized.append(MessageAssistantMessageRequestTyped(
                    role="assistant",
                    tool_calls=[{
                        "id": message.id,
                        "type": "function",
                        "function": {
                            "name": message.name,
                            "arguments": json.dumps(message.params)
                        }
                    }]
                ))
                 if message.content:
                      serialized.append({
                         "role": "tool",
                         "tool_call_id": message.id,
                         "content": str(message.content)
                     })
            elif isinstance(message, ImageMessage):
                raise ValueError("Image messages are not supported by Cerebras yet.")
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")
        return serialized
    
    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None) -> ChatLLMResponse:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.serialize_messages(messages),
            temperature=self.temperature,
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
            response_format=ResponseFormatResponseFormatJsonSchemaTyped(
                json_schema=ResponseFormatResponseFormatJsonSchemaJsonSchemaTyped(
                    name=structured_output.__class__.__name__,
                    description="Model output structured as JSON schema",
                    schema=structured_output.model_json_schema()
                ),
                type="json_schema"
            ) if structured_output else None
        )
        message = completion.choices[0].message
        if structured_output:
            content = structured_output.model_validate_json(message.content)
            thinking = None
        elif message.tool_calls:
            tool_call = message.tool_calls[0]
            content = ToolMessage(
                id=tool_call.id,
                name=tool_call.function.name,
                params=json.loads(tool_call.function.arguments),
                content=None
            )
            thinking = getattr(message, 'reasoning', None)
        else:
            content = AIMessage(content=message.content)
            thinking = getattr(message, 'reasoning', None)

        return ChatLLMResponse(
            thinking=thinking,
            content=content,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage.prompt_tokens,
                completion_tokens=completion.usage.completion_tokens,
                total_tokens=completion.usage.total_tokens
            )
        )

    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None) -> ChatLLMResponse:
        completion = await self.async_client.chat.completions.create(
            model=self.model,
            messages=self.serialize_messages(messages),
            temperature=self.temperature,
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
            response_format=ResponseFormatResponseFormatJsonSchemaTyped(
                json_schema=ResponseFormatResponseFormatJsonSchemaJsonSchemaTyped(
                    name=structured_output.__class__.__name__,
                    description="Model output structured as JSON schema",
                    schema=structured_output.model_json_schema()
                ),
                type="json_schema"
            ) if structured_output else None
        )
        message = completion.choices[0].message
        if structured_output:
            content = structured_output.model_validate_json(message.content)
            thinking = None
        elif message.tool_calls:
            tool_call = message.tool_calls[0]
            content = ToolMessage(
                id=tool_call.id,
                name=tool_call.function.name,
                params=json.loads(tool_call.function.arguments),
                content=None
            )
            thinking = getattr(message, 'reasoning', None)
        else:
            content = AIMessage(content=message.content)
            thinking = getattr(message, 'reasoning', None)

        return ChatLLMResponse(
            thinking=thinking,
            content=content,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage.prompt_tokens,
                completion_tokens=completion.usage.completion_tokens,
                total_tokens=completion.usage.total_tokens
            )
        )

    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None) -> Iterator[ChatLLMResponse]:
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=self.serialize_messages(messages),
            temperature=self.temperature,
            stream=True,
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield ChatLLMResponse(content=AIMessage(content=delta.content))
            if hasattr(delta, 'reasoning') and delta.reasoning:
                yield ChatLLMResponse(thinking=delta.reasoning)

    async def astream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None) -> AsyncIterator[ChatLLMResponse]:
        stream = await self.async_client.chat.completions.create(
            model=self.model,
            messages=self.serialize_messages(messages),
            temperature=self.temperature,
            stream=True,
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield ChatLLMResponse(content=AIMessage(content=delta.content))
            if hasattr(delta, 'reasoning') and delta.reasoning:
                yield ChatLLMResponse(thinking=delta.reasoning)

    def get_model_specification(self):
        return ModelMetadata(name=self.model, context_window=8192, owned_by="cerebras")



    
