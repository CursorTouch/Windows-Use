from openai import OpenAI
from openai.types.chat import ChatCompletionAssistantMessageParam, ChatCompletionUserMessageParam, ChatCompletionContentPartTextParam, ChatCompletionContentPartImageParam, ChatCompletionSystemMessageParam
from openai.types.shared_params.response_format_json_schema import JSONSchema, ResponseFormatJSONSchema
from openai.types.chat.chat_completion_content_part_image_param import ImageURL
from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage
from windows_use.llms.base import BaseChatLLM
from dataclasses import dataclass
from pydantic import BaseModel
from httpx import Client

@dataclass
class ChatAzureOpenAI(BaseChatLLM):
    def __init__(
        self, 
        endpoint: str,
        deployment_name: str,
        api_key: str,
        model: str | None = None,
        api_version: str = "2024-10-21",
        temperature: float = 0.0, 
        profile: str | None = None,
        max_retries: int = 3,
        timeout: float | None = None,
        default_headers: dict[str, str] | None = None,
        default_query: dict[str, object] | None = None,
        http_client: Client | None = None,
    ):
        self.endpoint = endpoint.rstrip('/')
        self.deployment_name = deployment_name
        self.api_key = api_key
        self.model = model
        self.api_version = api_version
        self.temperature = temperature
        self.profile = profile
        self.max_retries = max_retries
        self.timeout = timeout
        self.default_headers = default_headers
        self.default_query = default_query
        self.http_client = http_client
        self._client = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            # Build the base URL with deployment
            base_url = f"{self.endpoint}/openai/deployments/{self.deployment_name}"
            
            # Azure requires 'api-key' header for authentication (not Authorization: Bearer)
            headers = {"api-key": self.api_key}
            if self.default_headers:
                headers.update(self.default_headers)
            
            # Add api-version as default query parameter
            query = {"api-version": self.api_version}
            if self.default_query:
                query.update(self.default_query)
            
            self._client = OpenAI(
                api_key=self.api_key,
                base_url=base_url,
                max_retries=self.max_retries,
                timeout=self.timeout,
                default_headers=headers,
                default_query=query,
                http_client=self.http_client,
            )
        return self._client
    
    @property
    def provider(self) -> str:
        return "azure_openai"
    
    @property
    def model_name(self) -> str:
        return self.model or self.deployment_name
    
    def serialize_messages(self, messages: list[BaseMessage]) -> list:
        serialized = []
        for message in messages:
            if isinstance(message, SystemMessage):
                content = [ChatCompletionContentPartTextParam(type="text", text=message.content)]
                serialized.append(ChatCompletionSystemMessageParam(role="system", content=content))
            elif isinstance(message, HumanMessage):
                content = [ChatCompletionContentPartTextParam(type="text", text=message.content)]
                serialized.append(ChatCompletionUserMessageParam(role="user", content=content))
            elif isinstance(message, AIMessage):
                content = [ChatCompletionContentPartTextParam(type="text", text=message.content)]
                serialized.append(ChatCompletionAssistantMessageParam(role="assistant", content=content))
            elif isinstance(message, ImageMessage):
                message.scale_image(scale=0.7)
                image = f"data:{message.mime_type};base64,{message.image_to_base64()}"
                content = [
                    ChatCompletionContentPartTextParam(type="text", text=message.content),
                    ChatCompletionContentPartImageParam(type="image_url", image_url=ImageURL(url=image, detail="auto"))
                ]
                serialized.append(ChatCompletionUserMessageParam(role="user", content=content))
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")
        return serialized
    
    def invoke(self, messages: list[BaseMessage], structured_output: BaseModel | None = None) -> ChatLLMResponse:
        completion = self.client.chat.completions.create(
            model=self.deployment_name,
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
        content = completion.choices[0].message.content
        
        if structured_output:
            content = structured_output.model_validate_json(content)
        
        return ChatLLMResponse(
            content=content,
            usage=ChatLLMUsage(
                prompt_tokens=completion.usage.prompt_tokens,
                completion_tokens=completion.usage.completion_tokens,
                total_tokens=completion.usage.total_tokens
            )
        )
