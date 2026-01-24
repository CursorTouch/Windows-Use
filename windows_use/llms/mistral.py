from mistralai import HttpClient,AsyncHttpClient,RetryConfig,OptionalNullable, UserMessage, AssistantMessage, SystemMessage as MainMessage, TextChunk, ThinkChunk, ImageURL,ImageURLChunk, ResponseFormat, JSONSchema, ToolMessage as MistralToolMessage
from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage, ToolMessage
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage, ModelMetadata
from typing import Union,Dict,Type, Iterator, AsyncIterator
from windows_use.llms.base import BaseChatLLM
from windows_use.tool.service import Tool
from dataclasses import dataclass
from mistralai import Mistral
from pydantic import BaseModel
import logging
import json
import os

@dataclass
class ChatMistral(BaseChatLLM):
    def __init__(self, model: str, api_key: str|None=None, max_tokens: int|None=None, temperature: float = 0.7, server: Union[str, None] = None, server_url: Union[str, None] = None, url_params: Dict[str, str] = None, client: Type[HttpClient] = None, async_client: Type[AsyncHttpClient] = None,retry_config: OptionalNullable[RetryConfig] = None,timeout_ms: Union[int, None] = None,debug_logger: Union[logging.Logger, None] = None):
        self.model = model
        if not api_key and not os.getenv("MISTRAL_API_KEY"):
            raise ValueError("MISTRAL_API_KEY is not set")
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        self.temperature = temperature
        self.server = server
        self.max_tokens = max_tokens
        self.server_url = server_url
        self.url_params = url_params
        self._client = client
        self.async_client = async_client
        self.retry_config = retry_config
        self.timeout_ms = timeout_ms
        self.debug_logger = debug_logger

    @property
    def client(self) -> Mistral:
        return Mistral(**{
            "api_key": self.api_key,
            "server": self.server,
            "server_url": self.server_url,
            "url_params": self.url_params,
            "client": self._client,
            "async_client": self.async_client,
            "retry_config": self.retry_config,
            "timeout_ms": self.timeout_ms,
            "debug_logger": self.debug_logger
        })

    @property
    def provider(self) -> str:
        return "mistral"
    
    @property
    def model_name(self) -> str:
        return self.model
    
    def serialize_messages(self, messages: list[BaseMessage]):
        serialized = []
        for message in messages:
            if isinstance(message, SystemMessage):
                content=[TextChunk(text=message.content)]
                serialized.append(MainMessage(content=content))
            elif isinstance(message, HumanMessage):
                content=[TextChunk(text=message.content)]
                serialized.append(UserMessage(content=content))
            elif isinstance(message, AIMessage):
                content=[TextChunk(text=message.content)]
                serialized.append(AssistantMessage(content=content))
            elif isinstance(message, ToolMessage):
                # Assistant Tool Call
                serialized.append(AssistantMessage(
                    tool_calls=[{
                        "id": message.id,
                        "type": "function",
                        "function": {
                            "name": message.name,
                            "arguments": json.dumps(message.params)
                        }
                    }]
                ))
                # Tool Result (if content exists)
                if message.content:
                     serialized.append(MistralToolMessage(
                        tool_call_id=message.id,
                        content=str(message.content)
                    ))
            elif isinstance(message, ImageMessage):
                message.scale_images(scale=0.7)
                images=[f"data:{message.mime_type};base64,{image}" for image in message.convert_images("base64")]
                content=[
                    TextChunk(text=message.content),
                    *[ImageURLChunk(type="image_url",url=ImageURL(url=image,detail="auto")) for image in images]
                ]
                serialized.append(UserMessage(role="user",content=content))
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")
        return serialized
    
    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None=None, json_mode: bool = False) -> ChatLLMResponse:
        completion=self.client.chat.complete(
            model=self.model,
            messages=self.serialize_messages(messages),
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=False,
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
            response_format=ResponseFormat(
                json_schema=JSONSchema(
                    name=structured_output.__class__.__name__,
                    description="Model output structured as JSON schema",
                    schema_definition=structured_output.model_json_schema()
                ),

                type="json_schema"
            ) if structured_output else (ResponseFormat(type="json_object") if json_mode else None)
        )
        if structured_output:
            content=structured_output.model_validate_json(completion.choices[0].message.content)
            thinking=None
        else:
            thinking_parts = []
            content_parts = []
            ai_contents=completion.choices[0].message.content
            
            if isinstance(ai_contents,str):
                content_parts.append(ai_contents)
            elif isinstance(ai_contents,list):
                for ai_content in ai_contents:
                    if isinstance(ai_content,TextChunk):
                        content_parts.append(ai_content.text)
                    elif isinstance(ai_content,ThinkChunk):
                        # Handle thinking whether it's a string or a list of chunks
                        if isinstance(ai_content.thinking, str):
                            thinking_parts.append(ai_content.thinking)
                        elif isinstance(ai_content.thinking, list):
                            for chunk in ai_content.thinking:
                                if hasattr(chunk, 'text'):
                                    thinking_parts.append(chunk.text)
                    else:
                        raise ValueError(f"Unsupported message type: {type(ai_content)}")
            else:
                raise ValueError(f"Unsupported message type: {type(ai_contents)}")

            if completion.choices[0].message.tool_calls:
                 tool_call = completion.choices[0].message.tool_calls[0]
                 content = ToolMessage(
                     id=tool_call.id,
                     name=tool_call.function.name,
                     params=json.loads(tool_call.function.arguments),
                     content=None
                 )
            else:
                content = AIMessage(content="".join(content_parts))
            thinking = "".join(thinking_parts) if thinking_parts else None

        return ChatLLMResponse(
            thinking=thinking,
            content=content,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage.prompt_tokens,
                completion_tokens=completion.usage.completion_tokens,
                total_tokens=completion.usage.total_tokens
            )
        )

    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None=None, json_mode: bool = False) -> ChatLLMResponse:
        completion=await self.client.chat.complete_async(
            model=self.model,
            messages=self.serialize_messages(messages),
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=False,
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
            response_format=ResponseFormat(
                json_schema=JSONSchema(
                    name=structured_output.__class__.__name__,
                    description="Model output structured as JSON schema",
                    schema_definition=structured_output.model_json_schema()
                ),
                type="json_schema"
            ) if structured_output else (ResponseFormat(type="json_object") if json_mode else None)
        )
        if structured_output:
            content=structured_output.model_validate_json(completion.choices[0].message.content)
            thinking=None
        else:
            thinking_parts = []
            content_parts = []
            ai_contents=completion.choices[0].message.content
            
            if isinstance(ai_contents,str):
                content_parts.append(ai_contents)
            elif isinstance(ai_contents,list):
                for ai_content in ai_contents:
                    if isinstance(ai_content,TextChunk):
                        content_parts.append(ai_content.text)
                    elif isinstance(ai_content,ThinkChunk):
                        # Handle thinking whether it's a string or a list of chunks
                        if isinstance(ai_content.thinking, str):
                            thinking_parts.append(ai_content.thinking)
                        elif isinstance(ai_content.thinking, list):
                            for chunk in ai_content.thinking:
                                if hasattr(chunk, 'text'):
                                    thinking_parts.append(chunk.text)
                    else:
                        raise ValueError(f"Unsupported message type: {type(ai_content)}")
            else:
                raise ValueError(f"Unsupported message type: {type(ai_contents)}")

            if completion.choices[0].message.tool_calls:
                 tool_call = completion.choices[0].message.tool_calls[0]
                 content = ToolMessage(
                     id=tool_call.id,
                     name=tool_call.function.name,
                     params=json.loads(tool_call.function.arguments),
                     content=None
                 )
            else:
                content = AIMessage(content="".join(content_parts))
            thinking = "".join(thinking_parts) if thinking_parts else None

        return ChatLLMResponse(
            thinking=thinking,
            content=content,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage.prompt_tokens,
                completion_tokens=completion.usage.completion_tokens,
                total_tokens=completion.usage.total_tokens
            )
        )

    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None=None, json_mode: bool = False) -> Iterator[ChatLLMResponse]:
        stream = self.client.chat.stream(
            model=self.model,
            messages=self.serialize_messages(messages),
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
            response_format=ResponseFormat(
                json_schema=JSONSchema(
                    name=structured_output.__class__.__name__,
                    description="Model output structured as JSON schema",
                    schema_definition=structured_output.model_json_schema()
                ),
                type="json_schema"
            ) if structured_output else (ResponseFormat(type="json_object") if json_mode else None)
        )
        for chunk in stream:
            delta = chunk.data.choices[0].delta
            # Handle text content
            if delta.content:
                if isinstance(delta.content, str):
                    yield ChatLLMResponse(content=AIMessage(content=delta.content))
                elif isinstance(delta.content, list):
                     for part in delta.content:
                         if isinstance(part, TextChunk):
                             yield ChatLLMResponse(content=AIMessage(content=part.text))
                         elif isinstance(part, ThinkChunk):
                             if isinstance(part.thinking, str):
                                yield ChatLLMResponse(thinking=part.thinking)

    async def astream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None=None, json_mode: bool = False) -> AsyncIterator[ChatLLMResponse]:
        stream = await self.client.chat.stream_async(
            model=self.model,
            messages=self.serialize_messages(messages),
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
            response_format=ResponseFormat(
                json_schema=JSONSchema(
                    name=structured_output.__class__.__name__,
                    description="Model output structured as JSON schema",
                    schema_definition=structured_output.model_json_schema()
                ),
                type="json_schema"
            ) if structured_output else (ResponseFormat(type="json_object") if json_mode else None)
        )
        async for chunk in stream:
            delta = chunk.data.choices[0].delta
            # Handle text content
            if delta.content:
                if isinstance(delta.content, str):
                    yield ChatLLMResponse(content=AIMessage(content=delta.content))
                elif isinstance(delta.content, list):
                     for part in delta.content:
                         if isinstance(part, TextChunk):
                             yield ChatLLMResponse(content=AIMessage(content=part.text))
                         elif isinstance(part, ThinkChunk):
                             if isinstance(part.thinking, str):
                                 yield ChatLLMResponse(thinking=part.thinking)

    def get_model_specification(self):
        response = self.client.models.retrieve(model_id=self.model)
        return ModelMetadata(name=self.model,context_window=response.max_context_length,owned_by="mistral")
