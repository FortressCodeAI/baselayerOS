def evaluate(payload):
    reasons = []
    if payload.get("pii_present", False):
        reasons.append("pii_present_lv3")
    if payload.get("regulatory_domain") in ["hipaa", "soc2", "pci"]:
        if not payload.get("compliance_pack_enabled", False):
            reasons.append("missing_compliance_pack_lv3")
    if not payload.get("audit_chain_enabled", False):
        reasons.append("audit_chain_required_lv3")
    return {"passed": len(reasons) == 0, "reasons": reasons}
