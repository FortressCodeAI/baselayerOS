from __future__ import annotations

from typing import Dict, Type

from .base_action import BaseAction


class ActionRegistry:
    """
    Deterministic global registry for all governed actions.

    - Actions register themselves (or are registered by the server bootstrap)
    - Once frozen, no further registrations are allowed
    - Kernel and Executor read from this registry only
    """

    def __init__(self) -> None:
        # Maps action_name -> ActionClass
        self.actions: Dict[str, Type[BaseAction]] = {}
        self._frozen: bool = False

    def register(self, action_cls: Type[BaseAction]) -> None:
        """Register a new action class before the registry is frozen."""
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
