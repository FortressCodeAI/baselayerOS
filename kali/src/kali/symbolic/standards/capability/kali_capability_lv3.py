def evaluate(payload):
    reasons = []
    envelope = payload.get("capability_envelope", [])
    if not envelope:
        reasons.append("missing_capability_envelope_lv3")
    if payload.get("requested_capability") not in envelope:
        reasons.append("capability_outside_envelope_lv3")
    if payload.get("capability_escalation_attempt", False):
        reasons.append("capability_escalation_lv3")
    return {"passed": len(reasons) == 0, "reasons": reasons}
