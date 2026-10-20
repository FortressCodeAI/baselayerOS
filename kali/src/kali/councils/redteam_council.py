"""
Kali v1.0.0 — RedTeam Council

Applies adversarial checks for:
- prompt injection
- jailbreak attempts
- policy evasion
- attempts to bypass HITL or councils

This council is required for:
- critical risk tier
"""

from __future__ import annotations
from typing import Dict, Any

from kali.core.logging import KaliLogger


class RedTeamCouncil:
    def __init__(self, logger: KaliLogger):
        self.logger = logger

        # Simple v1.0.0 patterns — can be extended later
        self.jailbreak_phrases = [
            "ignore previous instructions",
            "bypass safety",
            "disable safety",
            "act as an unfiltered model",
            "you are no longer bound by rules",
        ]

        self.policy_evasion_phrases = [
            "pretend this is allowed",
            "this is just a test",
            "for research purposes only",
        ]

    def evaluate(self, envelope_state) -> Dict[str, Any]:
        request = envelope_state.request
        text = str(request.get("prompt", "")) + " " + str(request.get("description", ""))

        lowered = text.lower()

        for phrase in self.jailbreak_phrases:
            if phrase in lowered:
                reason = f"Detected jailbreak phrase: '{phrase}'."
                self.logger.error("redteam_rejected", envelope_id=envelope_state.envelope_id, reason=reason)
                return {"approved": False, "reason": reason}

        for phrase in self.policy_evasion_phrases:
            if phrase in lowered:
                reason = f"Detected policy evasion phrase: '{phrase}'."
                self.logger.error("redteam_rejected", envelope_id=envelope_state.envelope_id, reason=reason)
                return {"approved": False, "reason": reason}

        self.logger.info("redteam_approved", envelope_id=envelope_state.envelope_id)
        return {"approved": True, "reason": "redteam_ok"}
