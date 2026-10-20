"""
Kali v1.0.0 — Human-In-The-Loop (HITL) Engine

Determines:
- whether HITL is required (based on risk tier)
- whether HITL has been satisfied
- enforces HITL gates before execution

This engine is:
- deterministic
- rule-based
- replayable
"""

from __future__ import annotations
from typing import Dict, Any

from kali.core.config import KaliConfig
from kali.core.logging import KaliLogger
from kali.core.errors import HITLError


class HITLEngine:
    def __init__(self, config: KaliConfig, logger: KaliLogger):
        self.config = config
        self.logger = logger

    def evaluate(self, risk_tier_level: int) -> bool:
        """
        Determine if HITL is required based on risk tier level.
        """
        required = risk_tier_level >= self.config.hitl_threshold_level

        self.logger.info(
            "hitl_evaluated",
            risk_tier_level=risk_tier_level,
            hitl_required=required,
        )

        return required

    def enforce(self, envelope_state) -> None:
        """
        Enforce HITL requirement before execution.
        """
        if envelope_state.hitl_required and not envelope_state.hitl_approved:
            self.logger.error(
                "hitl_blocked",
                envelope_id=envelope_state.envelope_id,
            )
            raise HITLError(
                f"Envelope {envelope_state.envelope_id} requires HITL approval."
            )

        self.logger.info(
            "hitl_passed",
            envelope_id=envelope_state.envelope_id,
            hitl_required=envelope_state.hitl_required,
            hitl_approved=envelope_state.hitl_approved,
        )
