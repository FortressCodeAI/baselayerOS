# baselayeros/regulus/policy_linter.py

import json
from typing import List


class PolicyLinter:
    """
    Lints operator_contract.json for structural and logical issues.
    """

    VALID_ACTIONS = {"allow", "deny", "escalate"}
    VALID_ACTORS = {"regulus", "human", "any"}

    def lint(self, path: str) -> List[str]:
        issues = []

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            return [f"Failed to load JSON: {e}"]

        contract = data.get("operator_contract")
        if not contract:
            return ["Missing operator_contract root"]

        rules = contract.get("rules", [])
        if not isinstance(rules, list):
            issues.append("rules must be a list")

        for rule in rules:
            if rule.get("actor") not in self.VALID_ACTORS:
                issues.append(f"Invalid actor: {rule.get('actor')}")

            if rule.get("action") not in self.VALID_ACTIONS:
                issues.append(f"Invalid action: {rule.get('action')}")

            if "condition" not in rule:
                issues.append(f"Rule missing condition: {rule.get('id')}")

        forbidden = contract.get("forbidden_operations", [])
        if not isinstance(forbidden, list):
            issues.append("forbidden_operations must be a list")

        return issues
