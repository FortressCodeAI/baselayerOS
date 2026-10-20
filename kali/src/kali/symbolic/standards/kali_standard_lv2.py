# kali/symbolic/standards/kali_standard_lv2.py
"""
Kali Standard Level 2 — Strong Governance

Medium–high risk: external impact, customer-facing, but not fully regulated.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class KaliStandardLv2Result:
    passed: bool
    reasons: list


def evaluate_lv2(payload: Dict[str, Any]) -> KaliStandardLv2Result:
    """
    Level 2 checks:
    - All Level 1 checks
    - Risk score present and <= allowed threshold
    - Explicit capability envelope defined
    - Human-in-the-loop defined for high-impact actions
    """
    reasons = []

    # Reuse LV1 semantics
    from src.symbolic.standards.kali_standard_lv1 import evaluate_lv1
    lv1 = evaluate_lv1(payload)
    if not lv1.passed:
        reasons.append("lv1_failed")
        reasons.extend(lv1.reasons)

    risk_score = payload.get("risk_score")
    if risk_score is None:
        reasons.append("missing_risk_score")
    elif risk_score > payload.get("risk_threshold", 0.5):
        reasons.append("risk_score_above_threshold")

    capabilities = payload.get("capabilities")
    if not capabilities or not isinstance(capabilities, list):
        reasons.append("missing_capability_envelope")

    human_review_required = payload.get("human_review_required", False)
    high_impact = payload.get("high_impact", False)
    if high_impact and not human_review_required:
        reasons.append("missing_human_in_the_loop_for_high_impact")

    return KaliStandardLv2Result(
        passed=len(reasons) == 0,
        reasons=reasons,
    )
