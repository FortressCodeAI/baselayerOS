"""
Kali v1.0.0 — Capability Council

Ensures:
- the capability scope assigned to the envelope is valid
- the requested action is allowed under that scope
- no escalation beyond declared capability boundaries

This council is required for ALL risk tiers.
"""

from __future__ import annotations
from typing import Dict, Any

from kali.core.logging import KaliLogger


class CapabilityCouncil:
    def __init__(self, logger: KaliLogger):
        self.logger = logger

    def evaluate(self, envelope_state) -> Dict[str, Any]:
        scope = envelope_state.capability_scope
        request = envelope_state.request
        action = request.get("action", "read")

        # Capability scope must exist
        if scope is None:
            reason = "Capability scope not assigned."
            self.logger.error("capability_rejected", envelope_id=envelope_state.envelope_id, reason=reason)
            return {"approved": False, "reason": reason}

        # Allowed actions per scope
        allowed = {
            "read_only": ["read"],
            "workflow": ["read", "start_workflow", "inspect_workflow", "replay"],
            "write_limited": ["read", "write_limited"],
        }.get(scope, ["read"])

        if action not in allowed:
            reason = f"Action '{action}' not allowed under capability scope '{scope}'."
            self.logger.error("capability_rejected", envelope_id=envelope_state.envelope_id, reason=reason)
            return {"approved": False, "reason": reason}

        self.logger.info("capability_approved", envelope_id=envelope_state.envelope_id)
        return {"approved": True, "reason": "capability_ok"}
