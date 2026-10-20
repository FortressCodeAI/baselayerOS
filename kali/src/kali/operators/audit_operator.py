"""
Kali v1.0.0 — Audit Operator

Responsible for:
- exporting replay logs
- generating audit bundles
- summarizing governance decisions

This is how Kali exposes her audit-first nature.
"""

from __future__ import annotations
from typing import Dict, Any

from kali.core.logging import KaliLogger


class AuditOperator:
    def __init__(self, logger: KaliLogger):
        self.logger = logger

    def export_replay(self, replay: Dict[str, Any]) -> Dict[str, Any]:
        """
        Return replay log as-is for now.
        """
        self.logger.info("audit_replay_exported", envelope_id=replay.get("envelope_id"))
        return replay

    def summarize_governance(self, replay: Dict[str, Any]) -> Dict[str, Any]:
        """
        Produce a simple summary of governance decisions.
        """
        summary = {
            "envelope_id": replay.get("envelope_id"),
            "risk_tier": replay.get("risk_tier"),
            "capability_scope": replay.get("capability_scope"),
            "hitl_required": replay.get("hitl_required"),
            "hitl_approved": replay.get("hitl_approved"),
            "councils_ran": list(replay.get("councils_ran", {}).keys()),
        }

        self.logger.info("audit_summary_generated", envelope_id=summary["envelope_id"])
        return summary
