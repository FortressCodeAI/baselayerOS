from __future__ import annotations

from typing import Dict, Type

from .base_action import BaseAction


class ActionRegistry:

    def __init__(self) -> None:
        self.actions: Dict[str, Type[BaseAction]] = {}
        self._frozen: bool = False

    def register(self, action_cls: Type[BaseAction]) -> None:
        if self._frozen:
            raise RuntimeError("ActionRegistry is frozen; no further registrations allowed.")

        name = action_cls.metadata.name

        if name in self.actions:
            raise RuntimeError(f"Action '{name}' is already registered.")

        self.actions[name] = action_cls

    def freeze(self) -> None:
        """Prevent any further action registrations."""
        self._frozen = True

    @property
    def frozen(self) -> bool:
        return self._frozen


# Global singleton registry used across the substrate
registry = ActionRegistry()
