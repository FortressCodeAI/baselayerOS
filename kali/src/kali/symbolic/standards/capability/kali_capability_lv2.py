def evaluate(payload):
    reasons = []
    envelope = payload.get("capability_envelope", [])
    if not envelope:
        reasons.append("missing_capability_envelope_lv2")
    if payload.get("requested_capability") not in envelope:
        reasons.append("capability_outside_envelope_lv2")
    return {"passed": len(reasons) == 0, "reasons": reasons}
