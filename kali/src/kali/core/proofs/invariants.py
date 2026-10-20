def generate_invariant_proof(
        checks
):

    passed = all(
        c["passed"]
        for c in checks
    )

    return {
        "proof_type":
            "invariant_enforcement",

        "passed":
            passed,

        "checks":
            checks
    }
