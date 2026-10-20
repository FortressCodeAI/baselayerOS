def evaluate(payload):
    reasons = []
    if payload.get("pii_present", False):
        reasons.append("pii_present_lv1")
    return {"passed": len(reasons) == 0, "reasons": reasons}
