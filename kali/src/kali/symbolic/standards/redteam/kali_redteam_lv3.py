def evaluate(payload):
    reasons = []
    if payload.get("jailbreak_attempt", False):
        reasons.append("jailbreak_detected_lv3")
    if payload.get("adversarial_prompt", False):
        reasons.append("adversarial_prompt_lv3")
    if payload.get("tool_escalation_attempt", False):
        reasons.append("tool_escalation_lv3")
    return {"passed": len(reasons) == 0, "reasons": reasons}
