# src/substrate/invariants/verifier.py

from typing import Any, Dict, List

from .definitions import InvariantViolation, invariants


class InvariantVerifier:
    """
    Deterministic invariant verifier.

    - evaluates all registered invariants
    - no side effects
    - no I/O
    - returns a list of violations (empty list = all good)
    """

    def verify(
        self,
        prev_state: Dict[str, Any],
        next_state: Dict[str, Any],
        context: Dict[str, Any],
    ) -> List[InvariantViolation]:
        violations: List[InvariantViolation] = []

        for invariant in invariants.all():
            ok = invariant.check(prev_state, next_state, context)
            if not ok:
                violations.append(
                    InvariantViolation(
                        name=invariant.name,
                        description=invariant.description,
                        details={
                            "prev_state_snapshot": self._snapshot(prev_state),
                            "next_state_snapshot": self._snapshot(next_state),
                        },
                    )
                )

        return violations

    @staticmethod
    def _snapshot(state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deterministic shallow snapshot of state for logging/audit.

        - no mutation
        - no sorting assumptions beyond dict copy
        """
        return dict(state)


# Global verifier instance
verifier = InvariantVerifier()
