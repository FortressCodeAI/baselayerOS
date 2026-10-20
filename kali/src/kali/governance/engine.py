class GovernanceEngine:

    def evaluate(
        self,
        execution
    ):

        violations = []

        if not execution.action_slug:
            violations.append(
                "action_slug required"
            )

        decision = len(
            violations
        ) == 0

        return {
            "allowed": decision,
            "violations": violations
        }
