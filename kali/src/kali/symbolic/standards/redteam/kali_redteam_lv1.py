def evaluate(payload):
    reasons = []
    if payload.get("jailbreak_attempt", False):
        reasons.append("jailbreak_detected_lv1")
    return {"passed": len(reasons) == 0, "reasons": reasons}
