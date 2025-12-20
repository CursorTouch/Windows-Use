from cerebras.cloud.sdk.types.chat.completion_create_params import MessageSystemMessageRequestTyped,MessageUserMessageRequestTyped,MessageAssistantMessageRequestTyped,MessageSystemMessageRequestContentUnionMember1Typed,MessageAssistantMessageRequestContentUnionMember1Typed,MessageUserMessageRequestContentUnionMember1Typed,MessageAssistantMessageRequestContentUnionMember1Typed
from cerebras.cloud.sdk.types.chat.completion_create_params import ResponseFormatResponseFormatJsonSchemaJsonSchemaTyped,ResponseFormatResponseFormatJsonSchemaTyped
from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage
from windows_use.llms.base import BaseChatLLM
from cerebras.cloud.sdk import Cerebras
from dataclasses import dataclass
from pydantic import BaseModel
from httpx import Client

@dataclass
class ChatCerebras(BaseChatLLM):
    def __init__(self, model: str, api_key: str, temperature: float = 0.7,  base_url: str | None = None, timeout: float | None = None, max_retries: int = 3, default_headers: dict[str, str] | None = None, default_query: dict[str, object] | None = None, http_client: Client | None = None, strict_response_validation: bool = False, warm_tcp_connection: bool = True):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.default_headers = default_headers
        self.default_query = default_query
        self.http_client = http_client
        self.strict_response_validation = strict_response_validation
        self.warm_tcp_connection = warm_tcp_connection

    @property
    def client(self) -> Cerebras:
        return Cerebras(**{
            "api_key": self.api_key,
            "base_url": self.base_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "default_headers": self.default_headers,
            "default_query": self.default_query,
            "http_client": self.http_client,
            "_strict_response_validation": self.strict_response_validation,
            "warm_tcp_connection": self.warm_tcp_connection
        })

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
                raise ValueError("Image messages are not supported by Cerebras yet.")
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
            thinking=None
            content=structured_output.model_validate_json(completion.choices[0].message.content)
        else:
            thinking=completion.choices[0].message.reasoning
            content=completion.choices[0].message.content
        return ChatLLMResponse(
            thinking=thinking,
            content=content,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage.prompt_tokens,
                completion_tokens=completion.usage.completion_tokens,
                total_tokens=completion.usage.total_tokens
            )
        )


    
