from __future__ import annotations

from typing import Type

from operator_use.inference.api.video.base import BaseVideoAPI


class VideoAPIRegistry:
    def __init__(self) -> None:
        self._apis: dict[str, Type[BaseVideoAPI]] = {}

    def register(self, name: str, api: Type[BaseVideoAPI]) -> None:
        self._apis[name] = api

    def unregister(self, name: str) -> None:
        self._apis.pop(name, None)

    def list(self) -> list[Type[BaseVideoAPI]]:
        return list(self._apis.values())

    def get(self, name: str) -> Type[BaseVideoAPI] | None:
        return self._apis.get(name)

    def reset(self) -> None:
        self._apis.clear()

    @classmethod
    def from_builtins(cls) -> VideoAPIRegistry:
        from operator_use.inference.api.video.builtins import VIDEO_APIS
        instance = cls()
        for name, api in VIDEO_APIS:
            instance.register(name, api)
        return instance
