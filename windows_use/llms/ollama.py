from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage
from windows_use.llms.base import BaseChatLLM
from ollama import Client,Image,Message
from dataclasses import dataclass
from pydantic import BaseModel

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
            elif isinstance(message, ImageMessage):
                message.scale_image(scale=0.7)
                data = message.image_to_bytes()
                serialized.append(Message(role="user", content=message.content,images=[Image(value=data)]))
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")
        return serialized
    
    def invoke(self, messages: list[BaseMessage],structured_output:BaseModel|None=None) -> str:
        completion=self.client.chat(
            model=self.model,
            stream=False,
            messages=self.serialize_messages(messages),
            format=structured_output.model_json_schema() if structured_output else "",
        )
        if structured_output:
            content=structured_output.model_validate_json(completion.message.content)
            thinking=None
        else:
            thinking=completion.message.thinking if self.think else None
            content=completion.message.content
        return ChatLLMResponse(
            thinking=thinking,
            content=content,
            usage=ChatLLMUsage(
                prompt_tokens=completion.get("prompt_eval_count"),
                completion_tokens=completion.get("eval_count"),
                total_tokens=completion.get("eval_count")+completion.get("prompt_eval_count"),
            )
        )


        
    
