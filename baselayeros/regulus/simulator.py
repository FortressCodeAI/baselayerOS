from dataclasses import dataclass
from typing import Any, Dict

from baselayeros.regulus.config import RegulusConfig
from baselayeros.regulus.policy import PolicyEngine
from baselayeros.regulus.risk import RiskAssessor


@dataclass
class RegulusSimulator:
    """
    Runs a Regulus-style simulation:
    - assess risk
    - enforce policy
    - return a decision object
    """

    config: RegulusConfig
    policy: PolicyEngine
    risk: RiskAssessor

    @classmethod
    def bootstrap(cls) -> "RegulusSimulator":
        config = RegulusConfig()
        policy = PolicyEngine(config=config)
        risk = RiskAssessor()
        return cls(config=config, policy=policy, risk=risk)

    def simulate(self, operation: str, context: Dict[str, Any]) -> Dict[str, Any]:
        tier = self.risk.assess(operation, context)
        self.policy.enforce_risk_tier(operation, tier)

        decision = self.policy.decide(operation, context)
        decision["risk_tier"] = tier
        return decision
