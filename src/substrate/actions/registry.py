# src/substrate/actions/registry.py

from typing import Dict, Type
from .base_action import BaseAction


class ActionRegistry:
    """
    Deterministic registry for all available actions.

    - No dynamic imports
    - No nondeterministic ordering
    - Can be frozen to prevent further mutation
    """

    def __init__(self):
        self._actions: Dict[str, Type[BaseAction]] = {}
        self._frozen: bool = False

    def register(self, action_cls: Type[BaseAction]):
        """Register an action class deterministically."""
        if self._frozen:
            raise RuntimeError("ActionRegistry is frozen; no further registrations allowed.")

        name = action_cls.metadata.name
        version = action_cls.metadata.version
        key = f"{name}:{version}"

        if key in self._actions:
            raise ValueError(f"Action '{key}' already registered.")

        self._actions[key] = action_cls

    def get(self, name: str, version: str) -> Type[BaseAction]:
        """Retrieve an action class deterministically."""
        key = f"{name}:{version}"
        if key not in self._actions:
            raise KeyError(f"Action '{key}' not found in registry.")
        return self._actions[key]

    def list_actions(self):
        """Return a deterministic list of registered actions."""
        return sorted(self._actions.keys())

    def freeze(self):
        """Prevent further mutation — ensures deterministic action surface."""
        self._frozen = True

    @property
    def frozen(self) -> bool:
        return self._frozen


# Global registry instance used by the substrate
registry = ActionRegistry()
