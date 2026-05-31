"""
BaseLayerOS Python SDK — Compliance Pack Interface

This file defines the public interface for building compliance packs.
Compliance packs enforce invariants, define checks, and specify actions
that must occur when violations happen.

This SDK does NOT enforce compliance — the runtime does.
"""

from typing import Any, Dict, List


class CompliancePack:
    """
    Base class for all compliance packs.

    Developers subclass this and implement:
      - invariants()
      - checks()
      - actions()

    The runtime handles:
      - enforcement
      - violation logging
      - deterministic refusal
      - replay
    """

    def invariants(self) -> List[Dict[str, Any]]:
        """
        Return a list of invariants enforced by this compliance pack.

        Each invariant must include:
            - id
            - description
            - severity

        Example:
            [
                {
                    "id": "fairness_threshold",
                    "description": "Model must not exceed fairness disparity threshold",
                    "severity": "critical"
                }
            ]
        """
        raise NotImplementedError(
            "Compliance packs must implement invariants()."
        )

    def checks(self) -> List[Dict[str, Any]]:
        """
        Return a list of compliance checks.

        Each check must include:
            - id
            - description
            - when (expression)
            - uses_invariants (list of invariant IDs)

        Example:
            [
                {
                    "id": "check_fairness",
                    "description": "Validate fairness score",
                    "when": "after:score_applicant",
                    "uses_invariants": ["fairness_threshold"]
                }
            ]
        """
        raise NotImplementedError(
            "Compliance packs must implement checks()."
        )

    def actions(self) -> List[Dict[str, Any]]:
        """
        Return a list of actions triggered on violation.

        Each action must include:
            - id
            - description
            - on_violation (list of invariant IDs)

        Example:
            [
                {
                    "id": "halt_execution",
                    "description": "Stop workflow execution",
                    "on_violation": ["fairness_threshold"]
                }
            ]
        """
        raise NotImplementedError(
            "Compliance packs must implement actions()."
        )
