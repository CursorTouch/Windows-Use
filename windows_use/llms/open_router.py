from openai.types.chat import ChatCompletionAssistantMessageParam,ChatCompletionUserMessageParam,ChatCompletionContentPartTextParam,ChatCompletionContentPartImageParam,ChatCompletionSystemMessageParam
from openai.types.shared_params.response_format_json_schema import JSONSchema, ResponseFormatJSONSchema
from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage
from openai.types.chat.chat_completion_content_part_image_param import ImageURL
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage
from windows_use.llms.base import BaseChatLLM
from dataclasses import dataclass
from pydantic import BaseModel
from openai import OpenAI
from httpx import Client

@dataclass
class ChatOpenRouter(BaseChatLLM):
    def __init__(self, model: str, api_key: str, base_url: str|None=None, temperature: float = 0.7,max_retries: int = 3,timeout: int|None=None, default_headers: dict[str, str] | None = None, default_query: dict[str, object] | None = None, http_client: Client | None = None, strict_response_validation: bool = False):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.max_retries = max_retries
        self.base_url = base_url
        self.timeout = timeout
        self.default_headers = default_headers
        self.default_query = default_query
        self.http_client = http_client
        self.strict_response_validation = strict_response_validation
    
    @property
    def client(self):
        return OpenAI(**{
            "api_key": self.api_key,
            "base_url": self.base_url or 'https://openrouter.ai/api/v1',
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "default_headers": self.default_headers,
            "default_query": self.default_query,
            "http_client": self.http_client,
            "_strict_response_validation": self.strict_response_validation
        })
    
    @property
    def provider(self):
        return "openrouter"
    
    @property
    def model_name(self):
        return self.model
    
    def serialize_messages(self, messages: list[BaseMessage]):
        serialized = []
        for message in messages:
            if isinstance(message, SystemMessage):
                content=[ChatCompletionContentPartTextParam(type="text",text=message.content)]
                serialized.append(ChatCompletionSystemMessageParam(role="system",content=content))
            elif isinstance(message, HumanMessage):
                content=[ChatCompletionContentPartTextParam(type="text",text=message.content)]
                serialized.append(ChatCompletionUserMessageParam(role="user",content=content))
            elif isinstance(message, AIMessage):
                content=[ChatCompletionContentPartTextParam(type="text",text=message.content)]
                serialized.append(ChatCompletionAssistantMessageParam(role="assistant",content=content))
            elif isinstance(message, ImageMessage):
                message.scale_image(scale=0.7)
                image=f"data:{message.mime_type};base64,{message.image_to_base64()}"
                content=[
                    ChatCompletionContentPartTextParam(type="text",text=message.content),
                    ChatCompletionContentPartImageParam(type="image_url",url=ImageURL(url=image,detail="auto"))
                ]
                serialized.append(ChatCompletionUserMessageParam(role="user",content=content))
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")
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