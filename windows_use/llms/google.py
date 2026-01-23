from google.genai.types import Part, Content, GenerateContentConfigDict,Modality,ToolDict,FunctionDeclarationDict,FunctionCall
from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage, ToolMessage
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage, ModelMetadata
from google.genai.client import Client,DebugConfig
from google.auth.credentials import Credentials
from typing import Iterator, AsyncIterator
from windows_use.llms.base import BaseChatLLM
from dataclasses import dataclass
from windows_use.tool.service import Tool
from google.genai import types
from pydantic import BaseModel
import asyncio
import json
import os

def run_async(coro):
    """
    Run an async coroutine in both Jupyter notebooks and normal Python scripts.
    Returns the *actual result*, not a Task.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Running inside Jupyter — patch and run safely
        import nest_asyncio
        nest_asyncio.apply()
        return asyncio.get_event_loop().run_until_complete(coro)
    else:
        # Running in normal Python script
        return asyncio.run(coro)

@dataclass
class ChatGoogle(BaseChatLLM):
    def __init__(self, model: str, thinking_budget: int=-1, api_key: str|None=None, vertexai: bool|None=None, project: str|None=None, location: str|None=None, credentials: Credentials|None=None,http_options: types.HttpOptions | types.HttpOptionsDict | None = None, debug_config: DebugConfig | None = None, temperature: float = 0.7):
        self.model = model
        if not api_key and not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY is not set")
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.vertexai = vertexai
        self.temperature = temperature
        self.credentials = credentials
        self.project = project
        self.location = location
        self.http_options = http_options
        self.debug_config = debug_config
        self.thinking_budget = thinking_budget
        self._client = None
        self._async_client = None
        
    @property
    def provider(self) -> str:
        return "google"

    @property
    def model_name(self) -> str:
        return self.model
    
    @property
    def client(self) -> Client:
        if self._client is None:
            self._client = Client(**{
                "api_key": self.api_key,
                "vertexai": self.vertexai,
                "project": self.project,
                "location": self.location,
                "credentials": self.credentials,
                "http_options": self.http_options,
                "debug_config": self.debug_config
            })
        return self._client
    
    @property
    def async_client(self) -> Client:
        if self._async_client is None:
            self._async_client = Client(**{
                "api_key": self.api_key,
                "vertexai": self.vertexai,
                "project": self.project,
                "location": self.location,
                "credentials": self.credentials,
                "http_options": self.http_options,
                "debug_config": self.debug_config
            })
        return self._async_client
    
    def serialize_messages(self, messages: list[BaseMessage])-> tuple[str|None,list[dict]]:
        serialized = []
        system_instruction = None
        for message in messages:
            if isinstance(message, SystemMessage):
                system_instruction = message.content
            elif isinstance(message, HumanMessage):
                serialized.append(Content(role="user",parts=[Part.from_text(text=message.content)]))
            elif isinstance(message, AIMessage):
                serialized.append(Content(role="model",parts=[Part.from_text(text=message.content)]))
            elif isinstance(message, ToolMessage):
                serialized.append(Content(role="model",parts=[Part.from_function_call(name=message.name,args=message.params)]))
                if message.content:
                    serialized.append(Content(role="user",parts=[Part.from_function_response(name=message.name,response={"response":message.content})]))
            elif isinstance(message, ImageMessage):
                message.scale_images(scale=0.7)
                images=message.convert_images("bytes")
                serialized.append(
                    Content(role="user",parts=[
                        Part(text=message.content),
                        *[Part.from_bytes(data=image,mime_type=message.mime_type) for image in images]
                    ])
                )
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")
        return system_instruction, serialized
        
    def invoke(self, messages: list[BaseMessage]=[], tools:list[Tool]=[], structured_output: BaseModel | None = None) -> ChatLLMResponse:
        system_instruction, contents = self.serialize_messages(messages)
        config=GenerateContentConfigDict({
            "temperature": self.temperature,
            "system_instruction":system_instruction,    
            "response_mime_type": "application/json" if structured_output else "text/plain",
            "response_modalities": [Modality.TEXT],
            "response_json_schema":structured_output.model_json_schema(mode="serialization") if structured_output else None
        })
        if tools:
            config["tools"]= [ToolDict(function_declarations=[FunctionDeclarationDict(name=tool.name,description=tool.description,parameters_json_schema=tool.json_schema['parameters']) for tool in tools])]

        completion =run_async(self.client.aio.models.generate_content(
            model=self.model,
            config=config,
            contents=contents
            ))
        if structured_output:
            content=structured_output.model_validate(completion.parsed)
        elif getattr(completion, 'function_calls',None):
            function_call = completion.function_calls[0]
            content=ToolMessage(
                id="tool-call-id",
                name=function_call.name,
                params=function_call.args,
                content=None
            )
        else:
            # Manually extract text to avoid SDK warning about non-text parts (like thought_signature)
            text_parts = []
            if completion.candidates and completion.candidates[0].content and completion.candidates[0].content.parts:
                for part in completion.candidates[0].content.parts:
                    if part.text:
                        text_parts.append(part.text)
            
            content = AIMessage(content="".join(text_parts))
        return ChatLLMResponse(
            content=content,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage_metadata.prompt_token_count or 0,
                completion_tokens=completion.usage_metadata.candidates_token_count or 0,
                total_tokens=completion.usage_metadata.total_token_count or 0
            )
        )
    
    async def ainvoke(self, messages: list[BaseMessage]=[], tools:list[Tool]=[], structured_output: BaseModel | None = None) -> ChatLLMResponse:
        system_instruction, contents = self.serialize_messages(messages)
        config: GenerateContentConfigDict = {
            "temperature": self.temperature,
            "system_instruction":system_instruction,
            "response_mime_type": "application/json" if structured_output else "text/plain",
            "response_modalities": [Modality.TEXT],
            "response_json_schema":structured_output.model_json_schema() if structured_output else None
        }
        
        if tools:
             config["tools"]= [ToolDict(function_declarations=[FunctionDeclarationDict(name=tool.name,description=tool.description,parameters_json_schema=tool.json_schema['parameters']) for tool in tools])]
        
        try:
            completion = await self.async_client.aio.models.generate_content(
                model=self.model,
                config=config,
                contents=contents
            )
        except Exception as e:
            raise RuntimeError(f"Error calling Google GenAI API: {str(e)}") from e
        
        # Check if response has candidates
        if not completion.candidates or len(completion.candidates) == 0:
            error_msg = "Model returned empty response."
            if hasattr(completion, 'prompt_feedback'):
                error_msg += f" Prompt feedback: {completion.prompt_feedback}"
            raise ValueError(error_msg)
        
        # Check if the first candidate has content
        candidate = completion.candidates[0]
        if not candidate.content or not candidate.content.parts:
            error_msg = f"Model candidate has no content. Finish reason: {candidate.finish_reason}"
            if hasattr(candidate, 'safety_ratings'):
                error_msg += f", Safety ratings: {candidate.safety_ratings}"
            raise ValueError(error_msg)
        
        if structured_output:
            content=structured_output.model_validate(completion.parsed)
            thinking=None
        elif getattr(completion, 'function_calls',None):
            function_call = completion.function_calls[0]
            content=ToolMessage(
                id="tool-call-id",
                name=function_call.name,
                params=function_call.args,
                content=None
            )
            thinking=None
        else:
            # Manually extract text to avoid SDK warning about non-text parts (like thought_signature)
            text_parts = []
            thinking_parts = []
            if completion.candidates and completion.candidates[0].content and completion.candidates[0].content.parts:
                for part in completion.candidates[0].content.parts:
                    if part.text:
                        text_parts.append(part.text)
                    if getattr(part, 'thought', None):
                         thinking_parts.append(str(part.thought))
            
            content = AIMessage(content="".join(text_parts))
            thinking = "".join(thinking_parts) if thinking_parts else None
        return ChatLLMResponse(
            content=content,
            thinking=thinking,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage_metadata.prompt_token_count or 0,
                completion_tokens=completion.usage_metadata.candidates_token_count or 0,
                total_tokens=completion.usage_metadata.total_token_count or 0
            )
        )

    def stream(self, messages: list[BaseMessage]=[], tools:list[Tool]=[], structured_output: BaseModel | None = None) -> Iterator[ChatLLMResponse]:
        system_instruction, contents = self.serialize_messages(messages)
        config: GenerateContentConfigDict = {
            "temperature": self.temperature,
            "system_instruction":system_instruction,
            "response_mime_type": "application/json" if structured_output else "text/plain",
            "response_modalities": [Modality.TEXT],
            "response_json_schema":structured_output.model_json_schema(mode="serialization") if structured_output else None
        }
        
        if tools:
             config["tools"]= [ToolDict(function_declarations=[FunctionDeclarationDict(name=tool.name,description=tool.description,parameters_json_schema=tool.json_schema['parameters']) for tool in tools])]

        stream = self.client.models.generate_content_stream(
            model=self.model,
            config=config,
            contents=contents
        )
        for chunk in stream:
            if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                for part in chunk.candidates[0].content.parts:
                    if part.text:
                        yield ChatLLMResponse(content=AIMessage(content=part.text))
                    thought = getattr(part, 'thought', None)
                    if thought:
                        yield ChatLLMResponse(thinking=str(thought))

    async def astream(self, messages: list[BaseMessage]=[], tools:list[Tool]=[], structured_output: BaseModel | None = None) -> AsyncIterator[ChatLLMResponse]:
        system_instruction, contents = self.serialize_messages(messages)
        config: GenerateContentConfigDict = {
            "temperature": self.temperature,
            "system_instruction":system_instruction,
            "response_mime_type": "application/json" if structured_output else "text/plain",
            "response_modalities": [Modality.TEXT],
            "response_json_schema":structured_output.model_json_schema(mode="serialization") if structured_output else None
        }
        
        if tools:
             config["tools"]= [ToolDict(function_declarations=[FunctionDeclarationDict(name=tool.name,description=tool.description,parameters_json_schema=tool.json_schema['parameters']) for tool in tools])]

        stream = await self.async_client.aio.models.generate_content_stream(
            model=self.model,
            config=config,
            contents=contents
        )
        async for chunk in stream:
            if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                for part in chunk.candidates[0].content.parts:
                    if part.text:
                        yield ChatLLMResponse(content=AIMessage(content=part.text))
                    thought = getattr(part, 'thought', None)
                    if thought:
                        yield ChatLLMResponse(thinking=str(thought))
    
    def get_model_specification(self):
        response = run_async(self.client.aio.models.get(model=self.model))
        return ModelMetadata(name=self.model,context_window=response.input_token_limit,owned_by="google")
        

