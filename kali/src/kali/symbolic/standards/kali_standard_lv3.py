# kali/symbolic/standards/kali_standard_lv3.py
"""
Kali Standard Level 3 — Maximum Enforcement

Regulated / critical: finance, healthcare, safety, employment, credit, etc.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class KaliStandardLv3Result:
    passed: bool
    reasons: list


def evaluate_lv3(payload: Dict[str, Any]) -> KaliStandardLv3Result:
    """
    Level 3 checks:
    - All Level 2 checks
    - Deterministic execution required
    - Invariant set defined and all invariants satisfied
    - Full audit chain enabled
    - Governance council approval recorded
    """
    reasons = []

    from src.symbolic.standards.kali_standard_lv2 import evaluate_lv2
    lv2 = evaluate_lv2(payload)
    if not lv2.passed:
        reasons.append("lv2_failed")
        reasons.extend(lv2.reasons)

    deterministic = payload.get("deterministic", False)
    if not deterministic:
        reasons.append("non_deterministic_execution")

    invariants = payload.get("invariants", [])
    violated = [inv for inv in invariants if not inv.get("satisfied", False)]
    if not invariants:
        reasons.append("missing_invariants")
    if violated:
        reasons.append("invariants_violated")

    audit_chain_enabled = payload.get("audit_chain_enabled", False)
    if not audit_chain_enabled:
        reasons.append("audit_chain_disabled")

    council_approved = payload.get("council_approved", False)
    if not council_approved:
        reasons.append("missing_governance_council_approval")

    return KaliStandardLv3Result(
        passed=len(reasons) == 0,
        reasons=reasons,
    )
