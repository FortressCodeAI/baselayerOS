from kali.governance.rulebook import (
    RULEBOOK_HASH
)


def generate_governance_proof(
        envelope
):

    rules = {

        "GR-001":
            envelope.get(
                "deterministic",
                False
            ),

        "GR-002":
            envelope.get(
                "replayable",
                False
            ),

        "GR-003":
            envelope.get(
                "audit_chain_enabled",
                False
            ),

        "GR-004":
            bool(
                envelope
                .get("routing", {})
                .get("trace")
            )
    }

    return {

        "proof_type":
            "governance_rulebook",

        "rulebook_hash":
            RULEBOOK_HASH,

        "evaluated_rules":
            rules
    }
