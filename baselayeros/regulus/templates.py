# baselayeros/regulus/templates.py

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class DecisionTemplate:
    """
    A reusable decision template for Regulus.
    """

    name: str
    description: str

    def apply(self, operation: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deterministic template logic.
        Extend with real reasoning later.
        """
        return {
            "template": self.name,
            "operation": operation,
            "context": context,
            "approved": True,
        }


# -----------------------------
# Built-in templates
# -----------------------------

LOW_RISK_TEMPLATE = DecisionTemplate(
    name="low_risk",
    description="Default template for low-risk operations.",
)

SENSITIVE_OPERATION_TEMPLATE = DecisionTemplate(
    name="sensitive_operation",
    description="Template for operations involving sensitive data.",
)

FINANCIAL_OPERATION_TEMPLATE = DecisionTemplate(
    name="financial_operation",
    description="Template for operations involving money or assets.",
)
