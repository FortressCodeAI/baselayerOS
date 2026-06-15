# baselayeros/kali/authority_gate.py

from dataclasses import dataclass
from kali.refusal import refuse

@dataclass
class AuthorityGate:

    def allow(self, actor: str, operation: str, risk_tier: int = 0) -> bool:
        # Tier 4+ requires human approval
        if risk_tier >= 4:
            refuse(
                f"Operation '{operation}' requires human approval (risk tier {risk_tier})",
                code="RISK_TIER_TOO_HIGH"
            )

        return True
