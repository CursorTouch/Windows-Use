from cerebras.cloud.sdk.types.chat.completion_create_params import MessageSystemMessageRequestTyped,MessageUserMessageRequestTyped,MessageAssistantMessageRequestTyped,MessageSystemMessageRequestContentUnionMember1Typed,MessageAssistantMessageRequestContentUnionMember1Typed,MessageUserMessageRequestContentUnionMember1Typed,MessageAssistantMessageRequestContentUnionMember1Typed
from cerebras.cloud.sdk.types.chat.completion_create_params import ResponseFormatResponseFormatJsonSchemaJsonSchemaTyped,ResponseFormatResponseFormatJsonSchemaTyped
from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage
from windows_use.llms.base import BaseChatLLM
from cerebras.cloud.sdk import Cerebras
from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class ChatCerebras(BaseChatLLM):
    def __init__(self, model: str, base_url: str|None = None, api_key: str|None=None, temperature: float = 0.7,timeout: int|None = None):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.base_url = base_url
        self.timeout = timeout

    @property
    def client(self) -> Cerebras:
        return Cerebras(base_url=self.base_url,api_key=self.api_key,timeout=self.timeout)

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
                content = [MessageSystemMessageRequestContentUnionMember1Typed(type="text",text=message.content)]
                serialized.append(MessageSystemMessageRequestTyped(role="system",content=content))
            elif isinstance(message, HumanMessage):
                content = [MessageUserMessageRequestContentUnionMember1Typed(type="text",text=message.content)]
                serialized.append(MessageUserMessageRequestTyped(role="user",content=content))
            elif isinstance(message, AIMessage):
                content = [MessageAssistantMessageRequestContentUnionMember1Typed(type="text",text=message.content)]
                serialized.append(MessageAssistantMessageRequestTyped(role="assistant",content=content))
            elif isinstance(message, ImageMessage):
                pass
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")
        return serialized
    
    def invoke(self, messages: list[BaseMessage],structured_output:BaseModel|None=None) -> str:
        completion=self.client.chat.completions.create(
            model=self.model,
            messages=self.serialize_messages(messages),
            temperature=self.temperature,
            response_format=ResponseFormatResponseFormatJsonSchemaTyped(
                json_schema=ResponseFormatResponseFormatJsonSchemaJsonSchemaTyped(
                    name=structured_output.__class__.__name__,
                    description="Model output structured as JSON schema",
                    schema=structured_output.model_json_schema()
                ),
                type="json_schema"
            ) if structured_output else None
        )
        if structured_output:
            content=structured_output.model_validate_json(completion.choices[0].message.content)
        else:
            content=completion.choices[0].message.content
        return ChatLLMResponse(
            content=content,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage.prompt_tokens,
                completion_tokens=completion.usage.completion_tokens,
                total_tokens=completion.usage.total_tokens
            )
        )


    
