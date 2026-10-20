from dataclasses import dataclass
from src.symbolic.standards.safety.kali_safety_lv2 import evaluate as lv2

@dataclass
class SafetyLv3Result:
    passed: bool
    reasons: list

def evaluate(payload):
    base = lv2(payload)
    reasons = base.reasons.copy()

    if payload.get("risk_score", 0) > 0.2:
        reasons.append("risk_score_too_high_lv3")

    if not payload.get("audit_chain_enabled", False):
        reasons.append("audit_chain_required_lv3")

    if payload.get("domain") in ["medical", "finance", "legal"]:
        if not payload.get("expert_validation", False):
            reasons.append("missing_expert_validation_lv3")

    return SafetyLv3Result(passed=len(reasons) == 0, reasons=reasons)
