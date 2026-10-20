import json

# Safety Council
from kali.src.kali.symbolic.standards.safety.kali_safety_lv1 import evaluate as safety_lv1
from kali.src.kali.symbolic.standards.safety.kali_safety_lv2 import evaluate as safety_lv2
from kali.src.kali.symbolic.standards.safety.kali_safety_lv3 import evaluate as safety_lv3

# Red Team Council
from kali.src.kali.symbolic.standards.redteam.kali_redteam_lv1 import evaluate as red_lv1
from kali.src.kali.symbolic.standards.redteam.kali_redteam_lv2 import evaluate as red_lv2
from kali.src.kali.symbolic.standards.redteam.kali_redteam_lv3 import evaluate as red_lv3

# Determinism Council
from kali.src.kali.symbolic.standards.determinism.kali_determinism_lv1 import evaluate as det_lv1
from kali.src.kali.symbolic.standards.determinism.kali_determinism_lv2 import evaluate as det_lv2
from kali.src.kali.symbolic.standards.determinism.kali_determinism_lv3 import evaluate as det_lv3

# Compliance Council
from kali.src.kali.symbolic.standards.compliance.kali_compliance_lv1 import evaluate as comp_lv1
from kali.src.kali.symbolic.standards.compliance.kali_compliance_lv2 import evaluate as comp_lv2
from kali.src.kali.symbolic.standards.compliance.kali_compliance_lv3 import evaluate as comp_lv3

# Capability Council
from kali.src.kali.symbolic.standards.capability.kali_capability_lv1 import evaluate as cap_lv1
from kali.src.kali.symbolic.standards.capability.kali_capability_lv2 import evaluate as cap_lv2
from kali.src.kali.symbolic.standards.capability.kali_capability_lv3 import evaluate as cap_lv3


COUNCIL_MAP = {
    "safety":   {1: safety_lv1, 2: safety_lv2, 3: safety_lv3},
    "redteam":  {1: red_lv1,    2: red_lv2,    3: red_lv3},
    "determinism": {1: det_lv1, 2: det_lv2,    3: det_lv3},
    "compliance":  {1: comp_lv1, 2: comp_lv2,  3: comp_lv3},
    "capability":  {1: cap_lv1, 2: cap_lv2,    3: cap_lv3},
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


def evaluate_all(level: int, payload: dict):
    """
    Evaluate all five councils at a given governance level.
    Returns a deterministic governance decision.
    """

    results = {}

    for council_name, levels in COUNCIL_MAP.items():
        evaluator = levels[level]
        result = evaluator(payload)
        results[council_name] = result

    # Merge pass/fail
    all_passed = all(r["passed"] for r in results.values())

    return {
        "passed": all_passed,
        "council_results": results,
        "governance_level": level,
    }
