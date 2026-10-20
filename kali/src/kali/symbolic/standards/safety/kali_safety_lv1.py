from dataclasses import dataclass

@dataclass
class SafetyLv1Result:
    passed: bool
    reasons: list

def evaluate(payload):
    reasons = []

    if payload.get("unsafe_content", False):
        reasons.append("unsafe_content_detected")

    if payload.get("domain") in ["weapons", "violence", "self_harm"]:
        reasons.append("restricted_domain_lv1")

    return SafetyLv1Result(passed=len(reasons) == 0, reasons=reasons)
