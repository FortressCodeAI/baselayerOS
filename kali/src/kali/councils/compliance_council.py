"""
Kali v1.0.0 — Compliance Council

Ensures:
- the request complies with governance policies
- no restricted resource types are accessed
- no prohibited actions are performed
- no violations of Kali Standard Level 1–3

This council is required for:
- high
- critical risk tiers
"""

from __future__ import annotations
from typing import Dict, Any

from kali.core.logging import KaliLogger


class ComplianceCouncil:
    def __init__(self, logger: KaliLogger):
        self.logger = logger

        # Restricted resource types (v1.0.0)
        self.restricted_resources = {
            "internal_governance",
            "audit_logs",
            "substrate_kernel",
            "governance_policies",
        }

        # Prohibited actions (v1.0.0)
        self.prohibited_actions = {
            "delete_logs",
            "modify_governance",
            "override_council",
            "disable_hitl",
        }

    def evaluate(self, envelope_state) -> Dict[str, Any]:
        request = envelope_state.request
        action = request.get("action", "")
        resource_type = request.get("resource_type", "")

        # Block prohibited actions
        if action in self.prohibited_actions:
            reason = f"Action '{action}' is prohibited by compliance policy."
            self.logger.error("compliance_rejected", envelope_id=envelope_state.envelope_id, reason=reason)
            return {"approved": False, "reason": reason}

        # Block restricted resource access
        if resource_type in self.restricted_resources:
            reason = f"Access to restricted resource '{resource_type}' is prohibited."
            self.logger.error("compliance_rejected", envelope_id=envelope_state.envelope_id, reason=reason)
            return {"approved": False, "reason": reason}

        # Compliance passed
        self.logger.info("compliance_approved", envelope_id=envelope_state.envelope_id)
        return {"approved": True, "reason": "compliant"}
