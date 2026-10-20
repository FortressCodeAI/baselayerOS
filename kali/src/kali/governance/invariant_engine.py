class InvariantViolation(Exception):
    pass


class InvariantEngine:

    @staticmethod
    def evaluate(envelope):

        checks = []

        checks.append({
            "name":
                "deterministic_required",

            "passed":
                envelope.get(
                    "deterministic",
                    False
                )
        })

        checks.append({
            "name":
                "audit_chain_required",

            "passed":
                envelope.get(
                    "audit_chain_enabled",
                    False
                )
        })

        checks.append({
            "name":
                "replayable_required",

            "passed":
                envelope.get(
                    "replayable",
                    False
                )
        })

        failures = (
            item
            for item in checks
            if not item["passed"]
        )

        failures = list(failures)

        if failures:
            raise InvariantViolation(
                str(failures)
            )

        return checks
