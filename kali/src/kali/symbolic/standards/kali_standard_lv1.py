# kali/symbolic/standards/kali_standard_lv1.py
"""
Kali Standard Level 1 — Baseline Governance

Lightweight governance for low-risk, advisory, and internal use.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class KaliStandardLv1Result:
    passed: bool
    reasons: list


def evaluate_lv1(payload: Dict[str, Any]) -> KaliStandardLv1Result:
    """
    Level 1 checks:
    - Identity present (actor / system)
    - Basic logging enabled
    - No critical domains (finance, healthcare, safety)
    """
    reasons = []

    actor = payload.get("actor")
    if not actor:
        reasons.append("missing_actor")

    logging_enabled = payload.get("logging_enabled", False)
    if not logging_enabled:
        reasons.append("logging_disabled")

    domain = payload.get("domain", "internal")
    if domain in ["finance", "healthcare", "safety", "regulated"]:
        reasons.append("domain_too_sensitive_for_lv1")

    return KaliStandardLv1Result(
        passed=len(reasons) == 0,
        reasons=reasons,
    )
