from __future__ import annotations
from typing import Type
from operator_use.inference.api.image.base import BaseImageAPI


class ImageAPIRegistry:
    def __init__(self) -> None:
        self._apis: dict[str, Type[BaseImageAPI]] = {}

    def register(self, name: str, api: Type[BaseImageAPI]) -> None:
        self._apis[name] = api

    def unregister(self, name: str) -> None:
        self._apis.pop(name, None)

    def list(self) -> list[Type[BaseImageAPI]]:
        return list(self._apis.values())

    def get(self, name: str) -> Type[BaseImageAPI] | None:
        return self._apis.get(name)

    def reset(self) -> None:
        self._apis.clear()

    @classmethod
    def from_builtins(cls) -> ImageAPIRegistry:
        from operator_use.inference.api.image.builtins import IMAGE_APIS
        instance = cls()
        for name, api in IMAGE_APIS:
            instance.register(name, api)
        return instance
