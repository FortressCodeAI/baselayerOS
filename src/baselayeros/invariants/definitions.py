# src/substrate/invariants/definitions.py

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional


InvariantFn = Callable[[Dict[str, Any], Dict[str, Any], Dict[str, Any]], bool]
# args: (prev_state, next_state, context) → bool


@dataclass(frozen=True)
class Invariant:
    """
    A deterministic invariant over state transitions.

    - name: stable identifier
    - description: human-readable explanation
    - check: pure function, no side effects, no I/O
    """
    name: str
    description: str
    check: InvariantFn


@dataclass(frozen=True)
class InvariantViolation:
    """Represents a failed invariant check."""
    name: str
    description: str
    details: Optional[Dict[str, Any]] = None


class InvariantSet:
    """
    A deterministic collection of invariants.

    - registration is explicit
    - evaluation order is deterministic (insertion order)
    - can be frozen to prevent further mutation
    """

    def __init__(self):
        self._invariants: List[Invariant] = []
        self._frozen: bool = False

    def register(self, invariant: Invariant):
        if self._frozen:
            raise RuntimeError("InvariantSet is frozen; no further registrations allowed.")
        self._invariants.append(invariant)

    def all(self) -> List[Invariant]:
        return list(self._invariants)

    def freeze(self):
        self._frozen = True

    @property
    def frozen(self) -> bool:
        return self._frozen


# Global invariant set for the substrate
invariants = InvariantSet()


# Example baseline invariants (safe to ship publicly)


def _non_negative_counters(prev_state: Dict[str, Any],
                           next_state: Dict[str, Any],
                           context: Dict[str, Any]) -> bool:
    """
    Example invariant:
    - any key ending with '_count' must be non-negative integer.
    """
    for key, value in next_state.items():
        if key.endswith("_count"):
            if not isinstance(value, int):
                return False
            if value < 0:
                return False
    return True


def _no_missing_required_keys(prev_state: Dict[str, Any],
                              next_state: Dict[str, Any],
                              context: Dict[str, Any]) -> bool:
    """
    Example invariant:
    - required keys listed in context['required_keys'] must exist in next_state.
    """
    required = context.get("required_keys", [])
    for key in required:
        if key not in next_state:
            return False
    return True


# Register baseline invariants
invariants.register(
    Invariant(
        name="non_negative_counters",
        description="All '*_count' fields must be non-negative integers.",
        check=_non_negative_counters,
    )
)

invariants.register(
    Invariant(
        name="no_missing_required_keys",
        description="All required keys must be present in the next state.",
        check=_no_missing_required_keys,
    )
)
