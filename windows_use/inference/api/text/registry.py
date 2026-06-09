from __future__ import annotations
import importlib
from typing import Type, Union
from operator_use.inference.api.text.base import BaseLLMAPI

_Entry = Union[Type[BaseLLMAPI], str]


class LLMAPIRegistry:
    def __init__(self) -> None:
        self._apis: dict[str, _Entry] = {}

    def register(self, name: str, api: _Entry) -> None:
        """Register an API class or a lazy 'module:ClassName' import path."""
        self._apis[name] = api

    def unregister(self, name: str) -> None:
        self._apis.pop(name, None)

    def list(self) -> list[Type[BaseLLMAPI]]:
        return [self._resolve(name) for name in list(self._apis)]

    def get(self, name: str) -> Type[BaseLLMAPI] | None:
        if name not in self._apis:
            return None
        return self._resolve(name)

    def reset(self) -> None:
        self._apis.clear()

    def _resolve(self, name: str) -> Type[BaseLLMAPI]:
        entry = self._apis[name]
        if isinstance(entry, str):
            mod_path, _, cls_name = entry.partition(":")
            cls = getattr(importlib.import_module(mod_path), cls_name)
            self._apis[name] = cls
            return cls
        return entry

    @classmethod
    def from_builtins(cls) -> LLMAPIRegistry:
        from operator_use.inference.api.text.builtins import LLM_APIS
        instance = cls()
        for name, api in LLM_APIS:
            instance.register(name, api)
        return instance


# Backward-compat alias
APIRegistry = LLMAPIRegistry
