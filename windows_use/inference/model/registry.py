from __future__ import annotations
from operator_use.inference.model.types import Model


class ModelRegistry:
    """Lookup table for Model descriptors, supporting multiple providers per model ID."""

    def __init__(self) -> None:
        # A single model id may be served by several providers; store all variants
        self._models: dict[str, list[Model]] = {}

    def register(self, model: Model) -> None:
        """Append a model variant; multiple providers for the same id are allowed."""
        self._models.setdefault(model.id, []).append(model)

    def unregister(self, model_id: str, provider: str | None = None) -> None:
        """Remove a model by id; if provider is given, only remove that provider's variant."""
        if provider is None:
            self._models.pop(model_id, None)
        else:
            remaining = [m for m in self._models.get(model_id, []) if m.provider != provider]
            if remaining:
                self._models[model_id] = remaining
            else:
                self._models.pop(model_id, None)

    def list(self) -> list[Model]:
        """Return all registered model variants across all providers."""
        return [m for models in self._models.values() for m in models]

    def get(self, model_id: str, provider: str | None = None) -> Model | None:
        """Return a model by id, optionally filtered to a specific provider; first match wins."""
        models = self._models.get(model_id, [])
        if not models:
            return None
        if provider is None:
            return models[0]
        return next((m for m in models if m.provider == provider), None)

    def reset(self) -> None:
        """Remove all registered models."""
        self._models.clear()

    @classmethod
    def from_llm_builtins(cls) -> ModelRegistry:
        """Construct a registry pre-populated with all builtin text/LLM models."""
        from operator_use.builtins.models.text import models
        instance = cls()
        for model in models:
            instance.register(model)
        return instance

    @classmethod
    def from_image_builtins(cls) -> ModelRegistry:
        """Construct a registry pre-populated with all builtin image models."""
        from operator_use.builtins.models.image import models
        instance = cls()
        for model in models:
            instance.register(model)
        return instance

    @classmethod
    def from_audio_builtins(cls) -> ModelRegistry:
        """Construct a registry pre-populated with all builtin audio models."""
        from operator_use.builtins.models.audio import models
        instance = cls()
        for model in models:
            instance.register(model)
        return instance

    @classmethod
    def from_video_builtins(cls) -> ModelRegistry:
        """Construct a registry pre-populated with all builtin video models."""
        from operator_use.builtins.models.video import models
        instance = cls()
        for model in models:
            instance.register(model)
        return instance

    @classmethod
    def from_all_builtins(cls) -> ModelRegistry:
        """Construct a registry pre-populated with all builtin models across all modalities."""
        from operator_use.builtins.models.text import models as llm
        from operator_use.builtins.models.image import models as image
        from operator_use.builtins.models.audio import models as audio
        from operator_use.builtins.models.video import models as video
        instance = cls()
        for model in llm + image + audio + video:
            instance.register(model)
        return instance

    # Backward-compat aliases
    @classmethod
    def from_builtin(cls) -> ModelRegistry:
        """Backward-compat alias for from_llm_builtins."""
        return cls.from_llm_builtins()

    @classmethod
    def from_builtins(cls) -> ModelRegistry:
        """Backward-compat alias for from_image_builtins."""
        return cls.from_image_builtins()
