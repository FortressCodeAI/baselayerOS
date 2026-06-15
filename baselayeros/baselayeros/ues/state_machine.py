from __future__ import annotations

from typing import Dict, Set

from schemas.ues.v1_0_0.ues_types import UES
from baselayeros.errors import StateTransitionError


class UESStateMachine:
    """
    Enforces the deterministic lifecycle of a UES proposal.

    Allowed transitions:
        DRAFTED → OPTIMIZED
        OPTIMIZED → RISK_REVIEWED
        RISK_REVIEWED → APPROVED
        APPROVED → COMPILED
        COMPILED → EXECUTED

    Any state may transition to REJECTED.
    """

    _transitions: Dict[str, Set[str]] = {
        "DRAFTED": {"OPTIMIZED", "REJECTED"},
        "OPTIMIZED": {"RISK_REVIEWED", "REJECTED"},
        "RISK_REVIEWED": {"APPROVED", "REJECTED"},
        "APPROVED": {"COMPILED", "REJECTED"},
        "COMPILED": {"EXECUTED", "REJECTED"},
        "EXECUTED": set(),  # terminal
        "REJECTED": set(),  # terminal
    }

    def can_transition(self, current: str, target: str) -> bool:
        return target in self._transitions.get(current, set())

    def transition(self, ues: UES, target: str, actor: str, timestamp: str) -> UES:
        current = ues.state.status

        if not self.can_transition(current, target):
            raise StateTransitionError(
                f"Invalid transition: {current} → {target}"
            )

        # mutate the UES state
        ues.state.status = target
        ues.state.last_transition_by = actor
        ues.state.last_transition_at = timestamp

        return ues
