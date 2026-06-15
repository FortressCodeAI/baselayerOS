from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class RiskAssessor:
    """
    Computes a simple risk tier from context.
    Deterministic stub logic for now.
    """

    def assess(self, operation: str, context: Dict[str, Any]) -> int:
        # Deterministic stub:
        # - if context has "sensitive": True → tier 4
        # - else tier 2
        if context.get("sensitive", False):
            return 4
        return 2
