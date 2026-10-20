def evaluate(payload):
    reasons = []
    if payload.get("jailbreak_attempt", False):
        reasons.append("jailbreak_detected_lv2")
    if payload.get("adversarial_prompt", False):
        reasons.append("adversarial_prompt_lv2")
    return {"passed": len(reasons) == 0, "reasons": reasons}
