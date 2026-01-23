from openai.types.chat import ChatCompletionAssistantMessageParam,ChatCompletionUserMessageParam,ChatCompletionContentPartTextParam,ChatCompletionContentPartImageParam,ChatCompletionSystemMessageParam
from openai.types.shared_params.response_format_json_schema import JSONSchema, ResponseFormatJSONSchema
from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage, ToolMessage
from openai.types.chat.chat_completion_content_part_image_param import ImageURL
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage, ModelMetadata
from typing import Iterator, AsyncIterator
from windows_use.llms.base import BaseChatLLM
from windows_use.tool.service import Tool
from openai import OpenAI, AsyncOpenAI
from dataclasses import dataclass
from pydantic import BaseModel
from httpx import Client
import requests
import json
import os

@dataclass
class ChatOpenRouter(BaseChatLLM):
    def __init__(self, model: str, base_url: str|None=None, api_key: str|None=None, temperature: float = 0.7,max_retries: int = 3,timeout: int|None=None, default_headers: dict[str, str] | None = None, default_query: dict[str, object] | None = None, http_client: Client | None = None, strict_response_validation: bool = False):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.max_retries = max_retries
        self.base_url = base_url or 'https://openrouter.ai/api/v1'
        self.timeout = timeout
        self.default_headers = default_headers
        self.default_query = default_query
        self.http_client = http_client
        self.strict_response_validation = strict_response_validation
    
    @property
    def client(self):
        return OpenAI(**{
            "api_key": self.api_key or os.getenv("OPENROUTER_API_KEY"),
            "base_url": self.base_url,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "default_headers": self.default_headers,
            "default_query": self.default_query,
            "http_client": self.http_client,
            "_strict_response_validation": self.strict_response_validation
        })
    
    @property
    def async_client(self):
        return AsyncOpenAI(**{
            "api_key": self.api_key,
            "base_url": self.base_url or 'https://openrouter.ai/api/v1',
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "default_headers": self.default_headers,
            "default_query": self.default_query,
            "http_client": self.http_client,
            "_strict_response_validation": self.strict_response_validation
        })
    
    @property
    def provider(self):
        return "openrouter"
    
    @property
    def model_name(self):
        return self.model
    
    def serialize_messages(self, messages: list[BaseMessage]):
        serialized = []
        for message in messages:
            if isinstance(message, SystemMessage):
                content=[ChatCompletionContentPartTextParam(type="text",text=message.content)]
                serialized.append(ChatCompletionSystemMessageParam(role="system",content=content))
            elif isinstance(message, HumanMessage):
                content=[ChatCompletionContentPartTextParam(type="text",text=message.content)]
                serialized.append(ChatCompletionUserMessageParam(role="user",content=content))
            elif isinstance(message, AIMessage):
                content=[ChatCompletionContentPartTextParam(type="text",text=message.content)]
                serialized.append(ChatCompletionAssistantMessageParam(role="assistant",content=content))
            elif isinstance(message, ToolMessage):
                serialized.append(ChatCompletionAssistantMessageParam(
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
                message.scale_images(scale=0.7)
                images=[f"data:{message.mime_type};base64,{image}" for image in message.convert_images("base64")]
                content=[
                    ChatCompletionContentPartTextParam(type="text",text=message.content),
                    *[ChatCompletionContentPartImageParam(type="image_url",url=ImageURL(url=image,detail="auto")) for image in images]
                ]
                serialized.append(ChatCompletionUserMessageParam(role="user",content=content))
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")
        return serialized
    
    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None=None) -> ChatLLMResponse:
        completion=self.client.chat.completions.create(
            model=self.model,
            messages=self.serialize_messages(messages),
            temperature=self.temperature,
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
            response_format=ResponseFormatJSONSchema(
                type="json_schema",
                json_schema=JSONSchema(
                    name=structured_output.__class__.__name__,
                    description="Model output structured as JSON schema",
                    schema=structured_output.model_json_schema()
                )
            ) if structured_output else None
        )
        message = completion.choices[0].message
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            content = ToolMessage(
                id=tool_call.id,
                name=tool_call.function.name,
                params=json.loads(tool_call.function.arguments),
                content=None
            )
            thinking = getattr(message, 'reasoning_content', None)
        else:
            content=AIMessage(content=message.content)
            thinking = getattr(message, 'reasoning_content', None)
            
        return ChatLLMResponse(
            content=content,
            thinking=thinking,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage.prompt_tokens,
                completion_tokens=completion.usage.completion_tokens,
                total_tokens=completion.usage.total_tokens
            )
        )

    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None=None) -> ChatLLMResponse:
        completion=await self.async_client.chat.completions.create(
            model=self.model,
            messages=self.serialize_messages(messages),
            temperature=self.temperature,
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
            response_format=ResponseFormatJSONSchema(
                type="json_schema",
                json_schema=JSONSchema(
                    name=structured_output.__class__.__name__,
                    description="Model output structured as JSON schema",
                    schema=structured_output.model_json_schema()
                )
            ) if structured_output else None
        )
        message = completion.choices[0].message
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            content = ToolMessage(
                id=tool_call.id,
                name=tool_call.function.name,
                params=json.loads(tool_call.function.arguments),
                content=None
            )
            thinking = getattr(message, 'reasoning_content', None)
        else:
            content=AIMessage(content=message.content)
            thinking = getattr(message, 'reasoning_content', None)
            
        return ChatLLMResponse(
            content=content,
            thinking=thinking,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage.prompt_tokens,
                completion_tokens=completion.usage.completion_tokens,
                total_tokens=completion.usage.total_tokens
            )
        )

    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None=None) -> Iterator[ChatLLMResponse]:
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=self.serialize_messages(messages),
            temperature=self.temperature,
            stream=True,
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
            response_format=ResponseFormatJSONSchema(
                type="json_schema",
                json_schema=JSONSchema(
                    name=structured_output.__class__.__name__,
                    description="Model output structured as JSON schema",
                    schema=structured_output.model_json_schema()
                )
            ) if structured_output else None
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield ChatLLMResponse(content=AIMessage(content=delta.content))
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
                yield ChatLLMResponse(thinking=delta.reasoning_content)

    async def astream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None=None) -> AsyncIterator[ChatLLMResponse]:
        stream = await self.async_client.chat.completions.create(
            model=self.model,
            messages=self.serialize_messages(messages),
            temperature=self.temperature,
            stream=True,
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
            response_format=ResponseFormatJSONSchema(
                type="json_schema",
                json_schema=JSONSchema(
                    name=structured_output.__class__.__name__,
                    description="Model output structured as JSON schema",
                    schema=structured_output.model_json_schema()
                )
            ) if structured_output else None
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield ChatLLMResponse(content=AIMessage(content=delta.content))
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
                yield ChatLLMResponse(thinking=delta.reasoning_content)
    
    def get_model_specification(self):
        response = requests.get(self.base_url+"/models/",headers={"Authorization": f"Bearer {self.api_key}"})
        model=[model for model in response.json()['data'] if model.get("id")==self.model][0]
        return ModelMetadata(name=self.model,context_window=model["context_length"],owned_by=self.model.split("/")[0])
