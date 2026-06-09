from dataclasses import dataclass, field
from enum import Enum
from operator_use.message.types import Usage, UsageCost


class Modality(str, Enum):
    """Content modality supported by a model's input or output."""

    Text  = "text"
    Image = "image"
    Audio = "audio"
    Video = "video"


@dataclass
class Cost:
    """Per-million-token pricing for a model (USD)."""

    input: float = 0.0
    output: float = 0.0
    cache_read: float = 0.0
    cache_write: float = 0.0


@dataclass
class Model:
    """Full descriptor for a single LLM/image/audio/video model variant."""

    id: str
    name: str
    provider: str
    cost: Cost = field(default_factory=Cost)
    thinking: bool = False
    context_window: int = 0
    max_tokens: int = 16384
    input: list[Modality] = field(default_factory=list)
    output: list[Modality] = field(default_factory=list)
    api: str | None = None
    base_url: str | None = None
    voices: list[str] = field(default_factory=list)
    tts_format: str | None = None  # override response_format for TTS (e.g. "wav" for Groq)

    def get_name(self) -> str:
        """Return the human-readable model name."""
        return self.name

    def get_model_id(self) -> str:
        """Return the provider-facing model identifier string."""
        return self.id

    def get_cost(self) -> Cost:
        """Return the per-million-token cost schedule for this model."""
        return self.cost

    def calculate_cost(self, usage: Usage) -> UsageCost:
        """Populate usage.cost from token counts and return it."""
        # Rates are stored per-million; divide before multiplying by actual token count
        usage.cost.input = (self.cost.input / 1_000_000) * usage.input_tokens
        usage.cost.output = (self.cost.output / 1_000_000) * usage.output_tokens
        usage.cost.cache_read = (self.cost.cache_read / 1_000_000) * usage.cache_read_tokens
        usage.cost.cache_write = (self.cost.cache_write / 1_000_000) * usage.cache_write_tokens
        usage.cost.total = usage.cost.input + usage.cost.output + usage.cost.cache_read + usage.cost.cache_write
        return usage.cost


# Type aliases
TextModel  = Model
ImageModel = Model
AudioModel = Model
VideoModel = Model
