"""
Kali v1.0.0 — Determinism Council

Ensures:
- envelope structure is deterministic
- request fields are valid
- no nondeterministic actions are requested
- replay log can be generated

This council MUST approve before any other council runs.
"""

from __future__ import annotations
from typing import Any, Dict

from kali.core.logging import KaliLogger


class DeterminismCouncil:
    def __init__(self, logger: KaliLogger):
        self.logger = logger

    def evaluate(self, envelope_state) -> Dict[str, Any]:
        """
        Deterministic validation of envelope structure.
        """

        # Envelope must have required fields
        required_fields = [
            "envelope_id",
            "request",
            "risk_tier",
            "capability_scope",
            "timestamp",
            "kali_standard",
        ]

        missing = [f for f in required_fields if getattr(envelope_state, f, None) is None]

        if missing:
            reason = f"Missing required envelope fields: {missing}"
            self.logger.error("determinism_rejected", envelope_id=envelope_state.envelope_id, reason=reason)
            return {"approved": False, "reason": reason}

        # Request must be deterministic (no random, no time-based actions)
        request = envelope_state.request
        action = request.get("action", "")

        nondeterministic_actions = ["random", "generate_nonce", "system_time"]

        if action in nondeterministic_actions:
            reason = f"Action '{action}' is nondeterministic."
            self.logger.error("determinism_rejected", envelope_id=envelope_state.envelope_id, reason=reason)
            return {"approved": False, "reason": reason}

        self.logger.info("determinism_approved", envelope_id=envelope_state.envelope_id)
        return {"approved": True, "reason": "deterministic"}
