from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class CouncilDecision:
    approved: bool
    reason: str
    tier: str
    envelopes: List[str]


class GovernanceSpine:
    def __init__(self) -> None:
        self.tier = "regulated"
        self.default_envelopes: List[str] = [
            "summarize_stream",
            "priority_collapse",
        ]

    def evaluate(self, action: str, data: Dict[str, Any] | None = None) -> CouncilDecision:
        # health check
        if action == "ping":
            return CouncilDecision(
                approved=True,
                reason="Health check",
                tier=self.tier,
                envelopes=[],
            )

        # standard governed capabilities
        if action in {"summarize_stream", "priority_collapse", "extract_entities"}:
            return CouncilDecision(
                approved=True,
                reason="Standard governed capability",
                tier=self.tier,
                envelopes=self.default_envelopes,
            )

        # everything else is denied by default
        return CouncilDecision(
            approved=False,
            reason=f"Action '{action}' not allowed at tier '{self.tier}'",
            tier=self.tier,
            envelopes=[],
        )


SPINE = GovernanceSpine()
