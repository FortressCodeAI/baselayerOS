def evaluate(payload):
    reasons = []
    if not payload.get("deterministic", False):
        reasons.append("non_deterministic_lv2")
    if not payload.get("replayable", False):
        reasons.append("missing_replayability_lv2")
    return {"passed": len(reasons) == 0, "reasons": reasons}
