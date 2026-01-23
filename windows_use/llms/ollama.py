from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage, ToolMessage
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage, ModelMetadata
from ollama import Client, AsyncClient,Image,Message
from typing import Iterator, AsyncIterator
from windows_use.llms.base import BaseChatLLM
from windows_use.tool.service import Tool
from dataclasses import dataclass
from pydantic import BaseModel
import json
import os

@dataclass
class ChatOllama(BaseChatLLM):
    def __init__(self,host: str|None=None, model: str|None=None, think:bool=False, temperature: float = 0.7,timeout: int|None=None):
        self.host = host
        self.model = model
        self.think=think
        self.temperature = temperature
        self.timeout = timeout
    
    @property
    def provider(self) -> str:
        return "ollama"
    
    @property
    def client(self) -> Client:
        return Client(host=self.host,timeout=self.timeout)

    @property
    def async_client(self) -> AsyncClient:
        return AsyncClient(host=self.host,timeout=self.timeout)
    
    @property
    def model_name(self) -> str:
        return self.model
    
    def serialize_messages(self, messages: list[BaseMessage]) -> list[dict]:
        serialized = []
        for message in messages:
            if isinstance(message, SystemMessage):
                serialized.append(Message(role="system", content=message.content))
            elif isinstance(message, HumanMessage):
                serialized.append(Message(role="user", content=message.content))
            elif isinstance(message, AIMessage):
                serialized.append(Message(role="assistant", content=message.content))
            elif isinstance(message, ToolMessage):
                # Assistant Tool Call
                serialized.append(Message(
                    role="assistant",
                    tool_calls=[{
                        "function": {
                            "name": message.name,
                            "arguments": message.params
                        }
                    }]
                ))
                # Tool Result (if content exists)
                if message.content:
                     serialized.append(Message(
                        role="tool",
                        content=str(message.content)
                    ))
            elif isinstance(message, ImageMessage):
                message.scale_images(scale=0.7)
                images=message.convert_images("bytes")
                serialized.append(Message(role="user", content=message.content,images=[Image(value=image) for image in images]))
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")
        return serialized
    
    def invoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None=None) -> ChatLLMResponse:
        completion=self.client.chat(
            model=self.model,
            stream=False,
            messages=self.serialize_messages(messages),
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
            format=structured_output.model_json_schema() if structured_output else "",
        )
        if structured_output:
            content=structured_output.model_validate_json(completion.message.content)
            thinking=None
        elif completion.message.tool_calls:
            tool_call = completion.message.tool_calls[0]
            content = ToolMessage(
                id="tool-call-id",
                name=tool_call.function.name,
                params=tool_call.function.arguments,
                content=None
            )
            thinking=getattr(completion.message, 'reasoning_content', None)
        else:
            content=AIMessage(content=completion.message.content)
            thinking=getattr(completion.message, 'reasoning_content', None)
        return ChatLLMResponse(
            content=content,
            thinking=thinking,
            usage=ChatLLMUsage(
                prompt_tokens=completion.get("prompt_eval_count"),
                completion_tokens=completion.get("eval_count"),
                total_tokens=completion.get("eval_count")+completion.get("prompt_eval_count"),
            )
        )
    async def ainvoke(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None=None) -> ChatLLMResponse:
        completion=await self.async_client.chat(
            model=self.model,
            stream=False,
            messages=self.serialize_messages(messages),
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
            format=structured_output.model_json_schema() if structured_output else "",
        )
        if structured_output:
            content=structured_output.model_validate_json(completion.message.content)
            thinking=None
        elif completion.message.tool_calls:
            tool_call = completion.message.tool_calls[0]
            content = ToolMessage(
                id="tool-call-id",
                name=tool_call.function.name,
                params=tool_call.function.arguments,
                content=None
            )
            thinking=getattr(completion.message, 'reasoning_content', None)
        else:
            content=AIMessage(content=completion.message.content)
            thinking=getattr(completion.message, 'reasoning_content', None)
        return ChatLLMResponse(
            thinking=thinking,
            content=content,
            usage=ChatLLMUsage(
                prompt_tokens=completion.get("prompt_eval_count"),
                completion_tokens=completion.get("eval_count"),
                total_tokens=completion.get("eval_count")+completion.get("prompt_eval_count"),
            )
        )

    def stream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None=None) -> Iterator[ChatLLMResponse]:
        stream = self.client.chat(
            model=self.model,
            stream=True,
            messages=self.serialize_messages(messages),
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
            format=structured_output.model_json_schema() if structured_output else "",
        )
        for chunk in stream:
            if 'message' in chunk:
                 if 'content' in chunk['message']:
                     yield ChatLLMResponse(content=AIMessage(content=chunk['message']['content']))
                 if 'reasoning_content' in chunk['message']:
                     yield ChatLLMResponse(thinking=chunk['message']['reasoning_content'])

    async def astream(self, messages: list[BaseMessage], tools: list[Tool] = [], structured_output:BaseModel|None=None) -> AsyncIterator[ChatLLMResponse]:
        stream = await self.async_client.chat(
            model=self.model,
            stream=True,
            messages=self.serialize_messages(messages),
            tools=[{'type': 'function', 'function': tool.json_schema} for tool in tools] if tools else None,
            format=structured_output.model_json_schema() if structured_output else "",
        )
        async for chunk in stream:
             if 'message' in chunk:
                 if 'content' in chunk['message']:
                     yield ChatLLMResponse(content=AIMessage(content=chunk['message']['content']))
                 if 'reasoning_content' in chunk['message']:
                     yield ChatLLMResponse(thinking=chunk['message']['reasoning_content'])
        
    def get_model_specification(self):
        response = self.client.show(model=self.model)
        context_window=response.modelinfo.get([key for key in response.modelinfo.keys() if key.endswith("context_length")][0])
        return ModelMetadata(name=self.model,context_window=context_window,owned_by="ollama")

        
    
