from groq.types.chat import ChatCompletionSystemMessageParam,ChatCompletionUserMessageParam,ChatCompletionAssistantMessageParam,ChatCompletionContentPartTextParam,ChatCompletionContentPartImageParam
from groq.types.chat.completion_create_params import ResponseFormatResponseFormatJsonSchemaJsonSchema,ResponseFormatResponseFormatJsonSchema
from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage
from groq.types.chat.chat_completion_content_part_image_param import ImageURL
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage
from windows_use.llms.base import BaseChatLLM
from dataclasses import dataclass
from pydantic import BaseModel
from groq import Groq

@dataclass
class ChatGroq(BaseChatLLM):
    def __init__(self, model: str, base_url: str|None=None, api_key: str|None=None, temperature: float = 0.7,max_retries: int = 3,timeout: int|None=None):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.max_retries = max_retries
        self.base_url = base_url
        self.timeout = timeout

    @property
    def client(self) -> Groq:
        return Groq(base_url=self.base_url,api_key=self.api_key,max_retries=self.max_retries,timeout=self.timeout)

    @property
    def provider(self) -> str:
        return "groq"
    
    @property
    def model_name(self) -> str:
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
                content=[
                    ChatCompletionContentPartTextParam(type="text",text=message.content),
                    ChatCompletionContentPartImageParam(type="image_url",url=ImageURL(url=message.image_to_base64(),detail="auto"))
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
            response_format=ResponseFormatResponseFormatJsonSchema(
                json_schema=ResponseFormatResponseFormatJsonSchemaJsonSchema(
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


    
