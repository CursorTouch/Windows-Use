from openai import AzureOpenAI, AsyncAzureOpenAI
from openai.types.chat import ChatCompletionAssistantMessageParam, ChatCompletionUserMessageParam, ChatCompletionContentPartTextParam, ChatCompletionContentPartImageParam, ChatCompletionSystemMessageParam
from openai.types.shared_params.response_format_json_schema import JSONSchema, ResponseFormatJSONSchema
from openai.types.chat.chat_completion_content_part_image_param import ImageURL
from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage, ToolMessage
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage, ModelMetadata
from windows_use.llms.base import BaseChatLLM
from windows_use.tool.service import Tool
from typing import Iterator, AsyncIterator
from dataclasses import dataclass
from pydantic import BaseModel
from httpx import Client
import json
import os

@dataclass
class ChatAzureOpenAI(BaseChatLLM):
    def __init__(
        self,
        endpoint: str,
        deployment_name: str,
        api_key: str|None=None,
        model: str | None = None,
        api_version: str = "2024-10-21",
        temperature: float = 0.7,
        max_retries: int = 3,
        timeout: float | None = None,
        default_headers: dict[str, str] | None = None,
        default_query: dict[str, object] | None = None,
        http_client: Client | None = None,
        strict_response_validation: bool = False
    ):
        self.endpoint = endpoint.rstrip('/')
        self.deployment_name = deployment_name
        if not api_key and not os.getenv("AZURE_OPENAI_API_KEY"):
            raise ValueError("AZURE_OPENAI_API_KEY is not set")
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.model = model
        self.api_version = api_version
        self.temperature = temperature
        self.max_retries = max_retries
        self.timeout = timeout
        self.default_headers = default_headers
        self.default_query = default_query
        self.http_client = http_client
        self.strict_response_validation = strict_response_validation

    @property
    def client(self) -> AzureOpenAI:
        return AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version=self.api_version,
            azure_deployment=self.deployment_name,
            max_retries=self.max_retries,
            timeout=self.timeout,
            default_headers=self.default_headers,
            default_query=self.default_query,
            http_client=self.http_client,
            _strict_response_validation=self.strict_response_validation
        )

    @property
    def async_client(self) -> AsyncAzureOpenAI:
        return AsyncAzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version=self.api_version,
            azure_deployment=self.deployment_name,
            max_retries=self.max_retries,
            timeout=self.timeout,
            default_headers=self.default_headers,
            default_query=self.default_query,
            http_client=self.http_client,
            _strict_response_validation=self.strict_response_validation
        )

    @property
    def provider(self) -> str:
        return "azure_openai"

    @property
    def model_name(self) -> str:
        return self.model or self.deployment_name

    def serialize_messages(self, messages: list[BaseMessage]) -> list:
        serialized = []
        for message in messages:
            if isinstance(message, SystemMessage):
                content = [ChatCompletionContentPartTextParam(type="text", text=message.content)]
                serialized.append(ChatCompletionSystemMessageParam(role="system", content=content))
            elif isinstance(message, HumanMessage):
                content = [ChatCompletionContentPartTextParam(type="text", text=message.content)]
                serialized.append(ChatCompletionUserMessageParam(role="user", content=content))
            elif isinstance(message, AIMessage):
                content = [ChatCompletionContentPartTextParam(type="text", text=message.content)]
                serialized.append(ChatCompletionAssistantMessageParam(role="assistant", content=content))
            elif isinstance(message, ToolMessage):
                # Assistant Tool Call
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
                # Tool Result
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
                    ChatCompletionContentPartTextParam(type="text", text=message.content),
                    *[ChatCompletionContentPartImageParam(type="image_url", image_url=ImageURL(url=image, detail="auto")) for image in images]
                ]
                serialized.append(ChatCompletionUserMessageParam(role="user", content=content))
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")
        return serialized

    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None) -> ChatLLMResponse:
        completion = self.client.chat.completions.create(
            model=self.deployment_name,
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

    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None) -> ChatLLMResponse:
        completion = await self.async_client.chat.completions.create(
            model=self.deployment_name,
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

    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None) -> Iterator[ChatLLMResponse]:
        stream = self.client.chat.completions.create(
            model=self.deployment_name,
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

    async def astream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None) -> AsyncIterator[ChatLLMResponse]:
        stream = await self.async_client.chat.completions.create(
            model=self.deployment_name,
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
        return ModelMetadata(
            name=self.model or self.deployment_name,
            context_window=128000, # Default for most Azure deployments
            owned_by="microsoft"
        )

