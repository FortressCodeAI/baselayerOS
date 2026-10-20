def evaluate(payload):
    reasons = []
    if not payload.get("capability_envelope"):
        reasons.append("missing_capability_envelope_lv1")
    return {"passed": len(reasons) == 0, "reasons": reasons}
