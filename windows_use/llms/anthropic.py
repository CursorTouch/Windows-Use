from anthropic.types import Message,MessageParam,ImageBlockParam,Base64ImageSourceParam,TextBlockParam
from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage
from windows_use.llms.base import BaseChatLLM
from dataclasses import dataclass
from anthropic import Anthropic
from pydantic import BaseModel

@dataclass
class ChatAnthropic(BaseChatLLM):
    def __init__(self, model: str, api_key: str, temperature: float = 0.7):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature

    @property
    def client(self):
        return Anthropic(api_key=self.api_key)

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
                system_instruction = message.content
            elif isinstance(message, HumanMessage):
                content=[TextBlockParam(type="text",text=message.content)]
                serialized.append(MessageParam(role="user",content=content))
            elif isinstance(message, AIMessage):
                content=[TextBlockParam(type="text",text=message.content)]
                serialized.append(MessageParam(role="assistant",content=content))
            elif isinstance(message, ImageMessage):
                content=[
                    TextBlockParam(type="text",text=message.content),
                    ImageBlockParam(type="image",source=Base64ImageSourceParam(
                        type="base64",data=message.image_to_base64(),mimetype="image/png"
                    ))
                ]
                serialized.append(MessageParam(role="user",content=content))
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")
        return system_instruction,serialized
    
    def invoke(self, messages: list[BaseMessage], structured_output:BaseModel|None = None):
        system_instruction, messages = self.serialize_messages(messages)
        completion = self.client.messages.create(
            model=self.model,
            system=system_instruction,
            messages=messages,
            temperature=self.temperature,
        )

        if not isinstance(completion,Message):
            raise ValueError("Unexpected response type from Anthropic API")
        content = completion.content[0]
        return ChatLLMResponse(
            content=content,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage.input_tokens,
                completion_tokens=completion.usage.output_tokens,
                total_tokens=completion.usage.input_tokens+completion.usage.output_tokens
            )
        )     