# src/substrate/actions/base_action.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ActionMetadata:
    """Metadata describing the action's deterministic contract."""
    name: str
    version: str
    giu_cost: int  # GIU credits required to execute
    description: Optional[str] = None


class BaseAction(ABC):
    """
    Deterministic action interface.

    Every action:
    - declares metadata (name, version, GIU cost)
    - validates input deterministically
    - executes deterministically
    - produces deterministic output
    """

    metadata: ActionMetadata

    @abstractmethod
    def validate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deterministically validate and normalize input parameters.
        Must not mutate external state.
        """
        raise NotImplementedError

    @abstractmethod
    def run(self, params: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deterministically execute the action.
        Must not perform I/O, randomness, or nondeterministic operations.
        """
        raise NotImplementedError

    def giu_cost(self) -> int:
        """Return the GIU cost for this action."""
        return self.metadata.giu_cost

    def name(self) -> str:
        """Return the action's canonical name."""
        return self.metadata.name

    def version(self) -> str:
        """Return the action's version."""
        return self.metadata.version
