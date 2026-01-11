from openai import OpenAI
from openai.types.responses import (
    ResponseInputMessageItem,
)
from windows_use.messages import BaseMessage, SystemMessage, AIMessage, HumanMessage, ImageMessage
from windows_use.llms.views import ChatLLMResponse, ChatLLMUsage
from windows_use.llms.base import BaseChatLLM
from dataclasses import dataclass, field
from pydantic import BaseModel
from httpx import Client
from typing import Literal

@dataclass
class ChatOpenAI(BaseChatLLM):
    model: str = "gpt-5.2"
    api_key: str = ""
    organization: str | None = None
    project: str | None = None
    base_url: str | None = None
    websocket_base_url: str | None = None
    temperature: float = 0.7
    max_retries: int = 3
    timeout: int | None = None
    default_headers: dict[str, str] | None = None
    default_query: dict[str, object] | None = None
    http_client: Client | None = None
    strict_response_validation: bool = False

    # === Responses API specific ===
    # Stores ID of last response for chaining
    _last_response_id: str | None = field(default=None, repr=False)
    _client: OpenAI | None = field(default=None, repr=False)

    def __post_init__(self):
        self._client = None
        self._last_response_id = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            self._client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                max_retries=self.max_retries,
                websocket_base_url=self.websocket_base_url,
                timeout=self.timeout,
                organization=self.organization,
                project=self.project,
                default_headers=self.default_headers,
                default_query=self.default_query,
                http_client=self.http_client,
                _strict_response_validation=self.strict_response_validation,
            )
        return self._client

    @property
    def provider(self) -> str:
        return "openai"

    @property
    def model_name(self) -> str:
        return self.model

    @property
    def last_response_id(self) -> str | None:
        """ID of last response for continuing chain"""
        return self._last_response_id

    def reset_conversation(self) -> None:
        """Reset conversation chain (start new)"""
        self._last_response_id = None

    def serialize_messages(
        self,
        messages: list[BaseMessage]
    ) -> list[ResponseInputMessageItem]:
        """
        Serialization of messages in Responses API format.

        Format:
        {
            "role": "user" | "assistant" | "system",
            "content": str | list[ContentPart]
        }
        """
        serialized: list[ResponseInputMessageItem] = []

        for message in messages:
            if isinstance(message, SystemMessage):
                # System message — just text or list
                serialized.append({
                    "role": "system",
                    "content": message.content
                })

            elif isinstance(message, HumanMessage):
                serialized.append({
                    "role": "user",
                    "content": message.content
                })

            elif isinstance(message, AIMessage):
                serialized.append({
                    "role": "assistant",
                    "content": message.content
                })

            elif isinstance(message, ImageMessage):
                # Image + text
                message.scale_image(scale=0.7)
                image_url = f"data:{message.mime_type};base64,{message.image_to_base64()}"

                content_parts: list[ResponseInputContentParam] = []

                # Text (if exists)
                if message.content:
                    content_parts.append({
                        "type": "input_text",
                        "text": message.content
                    })

                # Image
                content_parts.append({
                    "type": "input_image",
                    "image_url": image_url,
                    "detail": "auto"  # or "low" / "high"
                })

                serialized.append({
                    "role": "user",
                    "content": content_parts
                })
            else:
                raise ValueError(f"Unsupported message type: {type(message)}")

        return serialized

    def invoke(
        self,
        messages: list[BaseMessage],
        structured_output: type[BaseModel] | None = None,
        use_conversation_chain: bool = True,
        reasoning_effort: Literal["low", "medium", "high", "none"] | None = "none",
    ) -> ChatLLMResponse:
        """
        Invoke model through Responses API.

        Args:
            messages: List of messages
            structured_output: Pydantic model for structured output
            use_conversation_chain: Use previous_response_id for chaining
            reasoning_effort: Reasoning level (for o1/o3 models)
        """
        # Preparing request parameters
        request_params: dict = {
            "model": self.model,
            #"temperature": self.temperature,
            "reasoning": {"effort": reasoning_effort},
            "text": {"verbosity": "low"},
        }

        # === Conversation chain ===
        # If there is previous_response_id — pass only NEW messages
        if use_conversation_chain and self._last_response_id:
            request_params["previous_response_id"] = self._last_response_id
            # Pass only latest messages (those after previous response)
            # Usually this is 1 user message
            request_params["input"] = self.serialize_messages(messages[-1:])
        else:
            # First request — pass all messages
            request_params["input"] = self.serialize_messages(messages)

        # === Structured Output ===
        if structured_output is not None:
            request_params["text"] = {
                "format": {
                    "type": "json_schema",
                    "name": structured_output.__name__,
                    "schema": structured_output.model_json_schema(),
                    "strict": True
                }
            }

        # === Reasoning (for o1/o3 models) ===
        if reasoning_effort:
            request_params["reasoning"] = {"effort": reasoning_effort}

        # === API call ===
        response = self.client.responses.create(**request_params)

        # Save ID for chain
        self._last_response_id = response.id

        # === Response parsing ===
        content_value = self._extract_content(response)
        usage = self._extract_usage(response)

        return ChatLLMResponse(
            content=content_value,
            usage=usage,
        )

    def _extract_content(self, response) -> str | None:
        """Extract text content from response"""
        if not response.output:
            return None

        # Looking for message with text
        for output_item in response.output:
            # output_item can be ResponseOutputMessage or other type
            if hasattr(output_item, "content") and output_item.content:
                for content_part in output_item.content:
                    if hasattr(content_part, "text"):
                        return content_part.text
            # Or text directly
            if hasattr(output_item, "text"):
                return output_item.text

        return None

    def _extract_usage(self, response) -> ChatLLMUsage | None:
        """Extract token usage information"""
        if not hasattr(response, "usage") or response.usage is None:
            return None

        usage = response.usage

        return ChatLLMUsage(
            prompt_tokens=getattr(usage, "input_tokens", 0),
            completion_tokens=getattr(usage, "output_tokens", 0),
            total_tokens=getattr(usage, "total_tokens", 0),
        )

    # === Additional methods for agentic scenarios ===

    def invoke_with_tools(
        self,
        messages: list[BaseMessage],
        tools: list[dict],
        tool_choice: str | dict = "auto",
    ) -> ChatLLMResponse:
        """
        Invoke with tools (function calling).
        """
        request_params = {
            "model": self.model,
            "input": self.serialize_messages(messages),
            "text": {"verbosity": "low"},
            "reasoning": {"effort": "none"},
            #"temperature": self.temperature,
            "tools": tools,
            "tool_choice": tool_choice,
        }

        if self._last_response_id:
            request_params["previous_response_id"] = self._last_response_id
            request_params["input"] = self.serialize_messages(messages[-1:])

        response = self.client.responses.create(**request_params)
        self._last_response_id = response.id

        # Parsing tool calls
        tool_calls = []
        content_value = None

        for output_item in response.output:
            if output_item.type == "function_call":
                tool_calls.append({
                    "id": output_item.call_id,
                    "name": output_item.name,
                    "arguments": output_item.arguments,
                })
            elif hasattr(output_item, "content"):
                content_value = self._extract_content_from_item(output_item)

        return ChatLLMResponse(
            content=content_value,
            usage=self._extract_usage(response),
            tool_calls=tool_calls if tool_calls else None,
            response_id=response.id,  # Useful for debugging
        )

    def add_tool_result(
        self,
        tool_call_id: str,
        result: str,
    ) -> None:
        """
        Add result of tool execution to context.

        In Responses API this is done through input with type="function_call_output"
        """
        # This needs to be called in the next invoke
        # Result is added as a special message
        pass

# === Extended version of ChatLLMResponse for tool calls ===
@dataclass
class ChatLLMResponse:
    content: str | None
    usage: ChatLLMUsage | None
    tool_calls: list[dict] | None = None
    response_id: str | None = None  # ID for chain
