from collections.abc import Callable
from typing import Any


class PluginRegistry:
    """Simple plugin registry for extension algorithms."""

    def __init__(self) -> None:
        self._plugins: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, plugin: Callable[..., Any]) -> None:
        if name in self._plugins:
            raise ValueError(f"Plugin '{name}' already registered")
        self._plugins[name] = plugin

    def get(self, name: str) -> Callable[..., Any]:
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not found")
        return self._plugins[name]

    def list_plugins(self) -> list[str]:
        return sorted(self._plugins.keys())
