def evaluate(payload):
    reasons = []
    if payload.get("pii_present", False):
        reasons.append("pii_present_lv2")
    if payload.get("regulatory_domain") in ["hipaa", "soc2", "pci"]:
        reasons.append("regulated_domain_lv2")
    return {"passed": len(reasons) == 0, "reasons": reasons}
