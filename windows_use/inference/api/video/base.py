from __future__ import annotations

from abc import ABC, abstractmethod

from operator_use.inference.model.types import Model
from operator_use.inference.types import GeneratedVideo, VideoContext, VideoOptions


class BaseVideoAPI(ABC):
    """
    Base class for all video generation providers.

    Video generation is inherently async at the provider level — jobs are
    submitted and polled until completion. Implementations handle the full
    submit → poll → return cycle inside generate(), keeping the caller
    interface simple and uniform.
    """

    def __init__(self, options: VideoOptions) -> None:
        self.options = options

    @abstractmethod
    async def generate(self, model: Model, context: VideoContext) -> GeneratedVideo:
        raise NotImplementedError


# Backward-compat alias
BaseAPI = BaseVideoAPI
