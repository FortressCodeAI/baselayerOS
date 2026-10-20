from __future__ import annotations

from typing import List

from kali.governance.spine import SPINE, CouncilDecision
from .errors import GovernanceError


def validate_capability(action: str, envelopes: List[str]) -> bool:
    decision: CouncilDecision = SPINE.evaluate(action, {})

    if not decision.approved:
        raise GovernanceError(decision.reason)

    # envelopes must be subset of council-approved envelopes
    if envelopes and not set(envelopes).issubset(set(decision.envelopes)):
        raise GovernanceError(
            f"Envelopes {envelopes} not permitted for action '{action}'"
        )

    return True
