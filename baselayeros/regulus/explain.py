# baselayeros/regulus/explain.py

from dataclasses import dataclass
from typing import Dict, Any

from baselayeros.regulus.config import RegulusConfig


@dataclass
class RegulusExplainer:
    """
    Produces human-readable explanations of Regulus decisions.
    """

    config: RegulusConfig

    def explain_decision(self, decision: Dict[str, Any]) -> str:
        op = decision.get("operation", "unknown")
        risk_tier = decision.get("risk_tier", "unknown")
        template = decision.get("template", "unknown")
        approved = decision.get("approved", False)

        lines: list[str] = []
        lines.append(f"Decision for operation: {op}")
        lines.append(f"- Risk tier: {risk_tier}")
        lines.append(f"- Template: {template}")
        lines.append(f"- Approved: {approved}")
        lines.append(
            f"- Max autonomous risk tier: {self.config.max_autonomous_risk_tier}"
        )

        if isinstance(risk_tier, int) and risk_tier > self.config.max_autonomous_risk_tier:
            lines.append(
                "- Explanation: Risk tier exceeds autonomous threshold; "
                "Regulus should escalate to a human."
            )
        else:
            lines.append(
                "- Explanation: Risk tier within autonomous threshold; "
                "Regulus may proceed under policy."
            )

        return "\n".join(lines)

    def explain_engine_result(self, engine_result: Dict[str, Any]) -> str:
        success = engine_result.get("success", False)
        error = engine_result.get("error")
        committed = engine_result.get("committed", False)

        lines: list[str] = []
        lines.append("Engine Result:")
        lines.append(f"- Success: {success}")
        lines.append(f"- Committed: {committed}")
        if error:
            lines.append(f"- Error: {error}")
        else:
            lines.append("- Error: None")

        return "\n".join(lines)

    def explain_full(self, regulus_bundle: Dict[str, Any]) -> str:
        decision = regulus_bundle.get("regulus_decision", {})
        engine_result = regulus_bundle.get("engine_result", {})

        return "\n\n".join(
            [
                self.explain_decision(decision),
                self.explain_engine_result(engine_result),
            ]
        )
