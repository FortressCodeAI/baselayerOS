def evaluate(payload):
    reasons = []
    if not payload.get("deterministic", False):
        reasons.append("non_deterministic_lv3")
    if not payload.get("replayable", False):
        reasons.append("missing_replayability_lv3")
    if not payload.get("invariants_satisfied", False):
        reasons.append("invariant_violation_lv3")
    return {"passed": len(reasons) == 0, "reasons": reasons}
