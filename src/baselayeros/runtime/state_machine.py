# src/substrate/runtime/state_machine.py

from typing import Any, Dict


class StateMachine:
    """
    Deterministic state transition engine.

    Responsibilities:
    - hold current state
    - apply deterministic updates
    - never mutate input state directly
    """

    def __init__(self, initial_state: Dict[str, Any]):
        # Always deep copy to avoid external mutation
        self._state = dict(initial_state)

    def get_state(self) -> Dict[str, Any]:
        """Return a deterministic snapshot of current state."""
        return dict(self._state)

    def apply(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deterministically apply updates to state.
        - no deletion
        - no mutation of nested structures
        - shallow merge only
        """
        next_state = dict(self._state)

        for key, value in updates.items():
            next_state[key] = value

        self._state = next_state
        return next_state
