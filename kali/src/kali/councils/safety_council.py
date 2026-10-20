"""
Kali v1.0.0 — Safety Council

Ensures:
- no harmful actions
- no unsafe resource access
- no irreversible operations without HITL
- no external API calls unless risk tier allows it

This council is required for:
- medium
- high
- critical risk tiers
"""

from __future__ import annotations
from typing import Any, Dict

from kali.core.logging import KaliLogger


class SafetyCouncil:
    def __init__(self, logger: KaliLogger):
        self.logger = logger

    def evaluate(self, envelope_state) -> Dict[str, Any]:
        request = envelope_state.request
        action = request.get("action", "")
        resource_type = request.get("resource_type", "")
        external_api = bool(request.get("external_api", False))

        # Block irreversible actions unless HITL approved
        irreversible_actions = ["commit_change", "irreversible_write"]

        if action in irreversible_actions and not envelope_state.hitl_approved:
            reason = f"Irreversible action '{action}' requires HITL approval."
            self.logger.error("safety_rejected", envelope_id=envelope_state.envelope_id, reason=reason)
            return {"approved": False, "reason": reason}

        # Block unsafe resource types
        unsafe_resources = ["root", "system_kernel", "secrets"]

        if resource_type in unsafe_resources:
            reason = f"Access to unsafe resource '{resource_type}' is prohibited."
            self.logger.error("safety_rejected", envelope_id=envelope_state.envelope_id, reason=reason)
            return {"approved": False, "reason": reason}

        # External API calls require high or critical tier
        if external_api and envelope_state.risk_tier not in ("high", "critical"):
            reason = "External API calls require high or critical risk tier."
            self.logger.error("safety_rejected", envelope_id=envelope_state.envelope_id, reason=reason)
            return {"approved": False, "reason": reason}

        self.logger.info("safety_approved", envelope_id=envelope_state.envelope_id)
        return {"approved": True, "reason": "safe"}
