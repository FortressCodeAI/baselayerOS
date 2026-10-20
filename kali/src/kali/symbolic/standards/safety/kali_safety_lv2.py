from dataclasses import dataclass
from src.symbolic.standards.safety.kali_safety_lv1 import evaluate as lv1

@dataclass
class SafetyLv2Result:
    passed: bool
    reasons: list

def evaluate(payload):
    base = lv1(payload)
    reasons = base.reasons.copy()

    if payload.get("risk_score", 0) > 0.4:
        reasons.append("risk_score_too_high_lv2")

    if payload.get("requires_human_review", False) and not payload.get("human_reviewed", False):
        reasons.append("missing_human_review_lv2")

    return SafetyLv2Result(passed=len(reasons) == 0, reasons=reasons)
