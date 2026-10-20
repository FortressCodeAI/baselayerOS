
import json

# Safety Council
from src.symbolic.standards.safety.kali_safety_lv1 import evaluate as safety_lv1
from src.symbolic.standards.safety.kali_safety_lv2 import evaluate as safety_lv2
from src.symbolic.standards.safety.kali_safety_lv3 import evaluate as safety_lv3

# Red Team Council
from src.symbolic.standards.redteam.kali_redteam_lv1 import evaluate as red_lv1
from src.symbolic.standards.redteam.kali_redteam_lv2 import evaluate as red_lv2
from src.symbolic.standards.redteam.kali_redteam_lv3 import evaluate as red_lv3

# Determinism Council
from src.symbolic.standards.determinism.kali_determinism_lv1 import evaluate as det_lv1
from src.symbolic.standards.determinism.kali_determinism_lv2 import evaluate as det_lv2
from src.symbolic.standards.determinism.kali_determinism_lv3 import evaluate as det_lv3

# Compliance Council
from src.symbolic.standards.compliance.kali_compliance_lv1 import evaluate as comp_lv1
from src.symbolic.standards.compliance.kali_compliance_lv2 import evaluate as comp_lv2
from src.symbolic.standards.compliance.kali_compliance_lv3 import evaluate as comp_lv3

# Capability Council
from src.symbolic.standards.capability.kali_capability_lv1 import evaluate as cap_lv1
from src.symbolic.standards.capability.kali_capability_lv2 import evaluate as cap_lv2
from src.symbolic.standards.capability.kali_capability_lv3 import evaluate as cap_lv3

from dataclasses import dataclass

COUNCIL_MAP = {
    "safety":   {1: safety_lv1, 2: safety_lv2, 3: safety_lv3},
    "redteam":  {1: red_lv1,    2: red_lv2,    3: red_lv3},
    "determinism": {1: det_lv1, 2: det_lv2,    3: det_lv3},
    "compliance":  {1: comp_lv1, 2: comp_lv2,  3: comp_lv3},
    "capability":  {1: cap_lv1, 2: cap_lv2,    3: cap_lv3},
}
"""
Council router — runs all governance checks over a payload.
"""




@dataclass
class CouncilResult:
    name: str
    passed: bool
    reasons: list


def safety_council(payload: dict) -> CouncilResult:
    reasons = []
    if payload.get("unsafe_content", False):
        reasons.append("unsafe_content")
    return CouncilResult(name="safety", passed=len(reasons) == 0, reasons=reasons)


def capability_council(payload: dict) -> CouncilResult:
    reasons = []
    envelope = payload.get("capability_envelope", [])
    requested = payload.get("requested_capability")

    if not envelope:
        reasons.append("missing_envelope")
    elif requested not in envelope:
        reasons.append("capability_outside_envelope")

    return CouncilResult(name="capability", passed=len(reasons) == 0, reasons=reasons)


def determinism_council(payload: dict) -> CouncilResult:
    # For now, assume deterministic if flag is set.
    reasons = []
    if not payload.get("deterministic", False):
        reasons.append("non_deterministic_flag")
    return CouncilResult(name="determinism", passed=len(reasons) == 0, reasons=reasons)


def compliance_council(payload: dict) -> CouncilResult:
    # Placeholder for compliance tier checks.
    reasons = []
    tier = payload.get("governance_tier", "pro")
    if tier not in ("pro", "enterprise", "regulated"):
        reasons.append(f"invalid_governance_tier:{tier}")
    return CouncilResult(name="compliance", passed=len(reasons) == 0, reasons=reasons)


def evaluate_all(payload: dict) -> dict:
    councils = [
        safety_council,
        capability_council,
        determinism_council,
        compliance_council,
    ]

    results = []
    for council in councils:
        res = council(payload)
        results.append(
            {
                "name": res.name,
                "passed": res.passed,
                "reasons": res.reasons,
            }
        )

    passed = all(r["passed"] for r in results)
    return {
        "passed": passed,
        "councils": results,
    }


def evaluate_council(council: str, level: int, payload: dict):
    """
    Evaluate a single council at a given governance level.
    """
    if council not in COUNCIL_MAP:
        return {"passed": False, "reasons": [f"unknown_council:{council}"]}

    if level not in COUNCIL_MAP[council]:
        return {"passed": False, "reasons": [f"invalid_level:{level}"]}

    evaluator = COUNCIL_MAP[council][level]
    return evaluator(payload)

