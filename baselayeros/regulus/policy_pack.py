from dataclasses import dataclass
from typing import Dict, Any

from baselayeros.regulus.templates import (
    LOW_RISK_TEMPLATE,
    SENSITIVE_OPERATION_TEMPLATE,
    FINANCIAL_OPERATION_TEMPLATE,
)


@dataclass
class PolicyPack:
    """
    A reusable collection of Regulus decision templates.
    """

    def select_template(self, operation: str, context: Dict[str, Any]):
        # Sensitive operations
        if context.get("sensitive", False):
            return SENSITIVE_OPERATION_TEMPLATE

        # Financial operations
        if "payment" in operation or "financial" in operation:
            return FINANCIAL_OPERATION_TEMPLATE

        # Default
        return LOW_RISK_TEMPLATE

    def apply(self, operation: str, context: Dict[str, Any]) -> Dict[str, Any]:
        template = self.select_template(operation, context)
        return template.apply(operation, context)
