from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage
from google.genai.types import Part, Content, GenerateContentConfigDict,Modality
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage
from google.auth.credentials import Credentials
from windows_use.llms.base import BaseChatLLM
from dataclasses import dataclass
from google.genai import types
from pydantic import BaseModel
from google import genai
import asyncio

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
    def __init__(self, model: str, api_key: str, vertexai: bool|None=None, project: str|None=None, location: str|None=None, credentials: Credentials|None=None,http_options: types.HttpOptions | types.HttpOptionsDict | None = None, temperature: float = 0.7):
        self.model = model
        self.api_key = api_key
        self.vertexai = vertexai
        self.temperature = temperature
        self.credentials = credentials
        self.project = project
        self.location = location
        self.http_options = http_options
        
    @property
    def provider(self) -> str:
        return "google"

    @property
    def model_name(self) -> str:
        return self.model
    
    @property
    def client(self) -> genai.Client:
        return genai.Client(vertexai=self.vertexai,api_key=self.api_key,credentials=self.credentials,project=self.project,location=self.location,http_options=self.http_options)
    
    def serialize_messages(self, messages: list[BaseMessage])-> tuple[str|None,list[dict]]:
        serialized = []
        system_instruction = None
        for message in messages:
            if isinstance(message, SystemMessage):
                system_instruction = message.content
            elif isinstance(message, HumanMessage):
                serialized.append(Content(role="user",parts=[Part(text=message.content)]))
            elif isinstance(message, AIMessage):
                serialized.append(Content(role="model",parts=[Part(text=message.content)]))
            elif isinstance(message, ImageMessage):
                data=message.image_to_bytes()
                serialized.append(
                    Content(role="user",parts=[
                        Part(text=message.content),
                        Part.from_bytes(data=data,mime_type="image/png")
                    ])
                )
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")
        return system_instruction, serialized
        
    def invoke(self, messages: list[BaseMessage], structured_output: BaseModel | None = None) -> ChatLLMResponse:
        system_instruction, contents = self.serialize_messages(messages)
        config: GenerateContentConfigDict = {
            "temperature": self.temperature,
            "system_instruction":system_instruction,
            "response_mime_type": "application/json" if structured_output else "text/plain",
            "response_modalities": [Modality.TEXT],
            "response_json_schema":structured_output.model_json_schema() if structured_output else None
        }
        completion =run_async(self.client.aio.models.generate_content(
            model=self.model,
            config=config,
            contents=contents
            ))
        if structured_output:
            content=structured_output.model_validate(completion.parsed)
        else:
            content=completion.text
        return ChatLLMResponse(
            content=content,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage_metadata.prompt_token_count or 0,
                completion_tokens=completion.usage_metadata.candidates_token_count or 0,
                total_tokens=completion.usage_metadata.total_token_count or 0
            )
        )
        

