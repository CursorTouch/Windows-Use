from typing import Protocol, runtime_checkable, overload, Iterator, AsyncIterator
from windows_use.providers.events import LLMEvent, LLMStreamEvent
from windows_use.providers.views import Metadata
from windows_use.messages import BaseMessage
from collections.abc import Iterable
from windows_use.tools import Tool
from pydantic import BaseModel


@runtime_checkable
class BaseChatLLM(Protocol):

    def sanitize_schema(self, tool_schema: dict) -> dict:
        """Convert full JSON schema into a minimal function schema.

        Keeps only: name, description, and simplified parameters (type, enum, description).
        """
        params = tool_schema.get("parameters", {})
        properties = params.get("properties", {})
        required = params.get("required", [])

        clean_props = {}

        for name, prop in properties.items():
            if isinstance(prop, dict):
                t = prop.get("type", "string")
                enum_vals = prop.get("enum")
                description = prop.get("description")
            else:
                t = "string"
                enum_vals = None
                description = None

            # Normalize to valid JSON schema types
            if t not in {"string", "integer", "number", "boolean", "array", "object"}:
                t = "string"

            entry: dict = {"type": t}
            if enum_vals is not None:
                entry["enum"] = enum_vals
            if description is not None:
                entry["description"] = description
            clean_props[name] = entry

        return {
            "name": tool_schema.get("name"),
            "description": tool_schema.get("description"),
            "parameters": {
                "type": "object",
                "properties": clean_props,
                "required": required,
            },
        }

    @property
    def model_name(self) -> str:
        ...

    @property
    def provider(self) -> str:
        ...

    @overload
    def invoke(self, messages: list[BaseMessage]|Iterable[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ...

    @overload
    async def ainvoke(self, messages: list[BaseMessage]|Iterable[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        ...

    @overload
    def stream(self, messages: list[BaseMessage]|Iterable[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> Iterator[LLMStreamEvent]:
        ...

    @overload
    async def astream(self, messages: list[BaseMessage]|Iterable[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> AsyncIterator[LLMStreamEvent]:
        ...

    @overload
    def get_metadata(self) -> Metadata:
        ...


@runtime_checkable
class BaseSTT(Protocol):
    """Protocol for Speech-to-Text providers.

    Any STT provider must implement `transcribe` and `atranscribe` methods
    that accept an audio file path and return transcribed text.

    Example:
        ```python
        class MySTTProvider(BaseSTT):
            @property
            def model(self) -> str:
                return "my-model"

            def transcribe(self, file_path: str) -> str:
                return "transcribed text"

            async def atranscribe(self, file_path: str) -> str:
                return "transcribed text"
        ```
    """

    @property
    def model(self) -> str:
        """The name of the STT model being used."""
        ...

    def transcribe(self, file_path: str) -> str:
        """Transcribe an audio file to text.

        Args:
            file_path: Path to the audio file (WAV, MP3, M4A, etc.).

        Returns:
            Transcribed text from the audio.
        """
        ...

    async def atranscribe(self, file_path: str) -> str:
        """Asynchronously transcribe an audio file to text.

        Args:
            file_path: Path to the audio file (WAV, MP3, M4A, etc.).

        Returns:
            Transcribed text from the audio.
        """
        ...


@runtime_checkable
class BaseTTS(Protocol):
    """Protocol for Text-to-Speech providers.

    Any TTS provider must implement `synthesize` and `asynthesize` methods
    that accept text and an output file path, generating an audio file.

    Example:
        ```python
        class MyTTSProvider(BaseTTS):
            @property
            def model(self) -> str:
                return "my-model"

            def synthesize(self, text: str, output_path: str) -> None:
                ...

            async def asynthesize(self, text: str, output_path: str) -> None:
                ...
        ```
    """

    @property
    def model(self) -> str:
        """The name of the TTS model being used."""
        ...

    def synthesize(self, text: str, output_path: str) -> None:
        """Synthesize text into an audio file.

        Args:
            text: The text to convert to speech.
            output_path: Path where the generated audio file will be saved.
        """
        ...

    async def asynthesize(self, text: str, output_path: str) -> None:
        """Asynchronously synthesize text into an audio file.

        Args:
            text: The text to convert to speech.
            output_path: Path where the generated audio file will be saved.
        """
        ...
