from __future__ import annotations

from abc import ABC, abstractmethod

from operator_use.inference.model.types import Model
from operator_use.inference.types import GeneratedImage, ImageContext, ImageOptions


class BaseImageAPI(ABC):
    def __init__(self, options: ImageOptions) -> None:
        self.options = options

    @abstractmethod
    async def generate(self, model: Model, context: ImageContext) -> GeneratedImage:
        raise NotImplementedError


# Backward-compat alias
BaseAPI = BaseImageAPI
