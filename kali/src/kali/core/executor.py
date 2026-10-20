from kali.governance.rulebook import (
    RULEBOOK_HASH
)

from kali.governance.invariant_engine import (
    InvariantEngine
)

from kali.core.proofs.deterministic import (
    generate_deterministic_proof
)

from kali.core.proofs.replay import (
    generate_replay_proof
)

from kali.core.proofs.invariants import (
    generate_invariant_proof
)

from kali.core.proofs.governance import (
    generate_governance_proof
)

from kali.core.proofs.audit import (
    append_event
)


class GovernedExecutor:

    CODE_VERSION = "1.0.0"

    def execute(
        self,
        envelope,
        handler
    ):

        execution_id = envelope.get(
            "execution_id"
        )

        action_slug = (
            envelope["action_slug"]
        )

        payload = (
            envelope["payload"]
        )

        invariant_checks = (
            InvariantEngine
            .evaluate(
                envelope
            )
        )

        output = handler(
            payload
        )

        replay_output = handler(
            payload
        )

        deterministic = (
            generate_deterministic_proof(
                action_slug=action_slug,
                payload=payload,
                output=output,
                code_version=self.CODE_VERSION,
                rulebook_hash=RULEBOOK_HASH
            )
        )

        replay = (
            generate_replay_proof(
                output,
                replay_output
            )
        )

        invariants = (
            generate_invariant_proof(
                invariant_checks
            )
        )

        governance = (
            generate_governance_proof(
                envelope
            )
        )

        audit = (
            append_event({

                "execution_id":
                    execution_id,

                "action":
                    action_slug,

                "payload":
                    payload,

                "output":
                    output,

                "rulebook_hash":
                    RULEBOOK_HASH,

                "execution_hash":
                    deterministic[
                        "execution_hash"
                    ],

                "code_version":
                    self.CODE_VERSION
            })
        )

        proof_bundle = {

            "proof_version":
                "1.0",

            "execution_id":
                execution_id,

            "execution_hash":
                deterministic[
                    "execution_hash"
                ],

            "rulebook_hash":
                governance[
                    "rulebook_hash"
                ],

            "audit_hash":
                audit[
                    "entry_hash"
                ],

            "replay_verified":
                replay[
                    "equivalent"
                ],

            "invariants_passed":
                invariants[
                    "passed"
                ]
        }

        return {

            "execution_id":
                execution_id,

            "status":
                "executed",

            "proof_bundle":
                proof_bundle,

            "result":
                output,

            "proofs": {

                "deterministic_execution":
                    deterministic,

                "replay_equivalence":
                    replay,

                "invariant_enforcement":
                    invariants,

                "audit_chain":
                    audit,

                "governance_rulebook":
                    governance
            }
        }