def evaluate(payload):
    reasons = []
    if not payload.get("deterministic", False):
        reasons.append("non_deterministic_lv1")
    return {"passed": len(reasons) == 0, "reasons": reasons}
