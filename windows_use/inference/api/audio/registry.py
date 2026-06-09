from __future__ import annotations

from typing import Type

from operator_use.inference.api.audio.base import BaseAudioAPI


class AudioAPIRegistry:
    def __init__(self) -> None:
        self._apis: dict[str, Type[BaseAudioAPI]] = {}

    def register(self, name: str, api: Type[BaseAudioAPI]) -> None:
        self._apis[name] = api

    def unregister(self, name: str) -> None:
        self._apis.pop(name, None)

    def list(self) -> list[Type[BaseAudioAPI]]:
        return list(self._apis.values())

    def get(self, name: str) -> Type[BaseAudioAPI] | None:
        return self._apis.get(name)

    def reset(self) -> None:
        self._apis.clear()

    @classmethod
    def from_builtins(cls) -> AudioAPIRegistry:
        from operator_use.inference.api.audio.builtins import AUDIO_APIS
        instance = cls()
        for name, api in AUDIO_APIS:
            instance.register(name, api)
        return instance
