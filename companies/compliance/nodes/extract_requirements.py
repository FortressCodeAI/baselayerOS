# baselayeros/companies/compliance/nodes/extract_requirements.py

from dataclasses import dataclass
from kali.refusal import refuse


@dataclass
class ExtractRequirements:
    """
    Deterministic requirement extraction node.
    Produces a stub list of compliance requirements.
    """

    def run(self) -> list[str]:
        # Deterministic stub output
        requirements = [
            "Submit annual compliance report",
            "Maintain updated policy documentation",
            "Provide quarterly financial statements",
        ]

        if not requirements:
            refuse("No requirements extracted", code="NO_REQUIREMENTS")

        return requirements
