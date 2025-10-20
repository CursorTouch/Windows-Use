from openai.types.shared_params.response_format_json_schema import JSONSchema, ResponseFormatJSONSchema
from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage
from windows_use.llm.views import ChatLLMResponse, ChatLLMUsage
from windows_use.llm.base import BaseChatLLM
from dataclasses import dataclass
from pydantic import BaseModel
from openai import OpenAI

@dataclass
class ChatOpenAI(BaseChatLLM):
    def __init__(self, model: str, api_key: str, temperature: float = 0.7):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
    
    @property
    def client(self):
        return OpenAI(api_key=self.api_key)
    
    @property
    def provider(self):
        return "openai"
    
    @property
    def model_name(self):
        return self.model
    
    def serialize_messages(self, messages: list[BaseMessage]):
        serialized = []
        for message in messages:
            if isinstance(message, SystemMessage|HumanMessage|AIMessage):
                match message.role:
                    case "system":
                        role="system"
                    case "human":
                        role="user"
                    case "ai":
                        role="assistant"
                content=[
                    {
                        "type": "text",
                        "text": message.content
                    }
                ]
            elif isinstance(message, ImageMessage):
                role="user"
                content=[
                    {
                        "type": "text",
                        "text": message.content
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": message.image
                        }
                    }
                ]
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")
            serialized.append({"role": role, "content": content})
        return serialized
    
    def invoke(self, messages: list[BaseMessage],structured_output:BaseModel|None=None) -> str:
        completion=self.client.chat.completions.create(
            model=self.model,
            messages=self.serialize_messages(messages),
            temperature=self.temperature,
            response_format=ResponseFormatJSONSchema(
                type="json_schema",
                json_schema=JSONSchema(
                    name=structured_output.__class__.__name__,
                    description="Model output structured as JSON schema",
                    schema=structured_output.model_json_schema()
                )
            ) if structured_output else None
        )
        content=completion.choices[0].message.content
        return ChatLLMResponse(
            content=content,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage.prompt_tokens,
                completion_tokens=completion.usage.completion_tokens,
                total_tokens=completion.usage.total_tokens
            )
        )