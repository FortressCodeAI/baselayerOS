"""
Kali v1.0.0 — Councils Package

Provides helper to wire all councils into CouncilRouter.
"""

from kali.core.logging import get_logger
from kali.councils.determinism_council import DeterminismCouncil
from kali.councils.safety_council import SafetyCouncil
from kali.councils.capability_council import CapabilityCouncil
from kali.councils.compliance_council import ComplianceCouncil
from kali.councils.redteam_council import RedTeamCouncil


def register_all_councils(router) -> None:
    """
    Register all default councils with the given CouncilRouter.
    """
    logger = get_logger("councils")

    router.register("determinism", DeterminismCouncil(logger=logger))
    router.register("safety", SafetyCouncil(logger=logger))
    router.register("capability", CapabilityCouncil(logger=logger))
    router.register("compliance", ComplianceCouncil(logger=logger))
    router.register("redteam", RedTeamCouncil(logger=logger))
