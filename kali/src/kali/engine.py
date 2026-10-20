from kali.governance.engine import GovernanceEngine
from kali.runtime.engine import RuntimeEngine
from kali.core.proofs.engine import ProofEngine
from kali.audit.ledger import AuditLedger


class KaliEngine:

    def __init__(self):

        self.governance = (
            GovernanceEngine()
        )

        self.runtime = (
            RuntimeEngine()
        )

        self.audit = (
            AuditLedger()
        )

    def execute(
        self,
        execution
    ):

        decision = (
            self.governance
            .evaluate(execution)
        )

        if not decision["allowed"]:

            return {
                "status":
                    "denied",
                "decision":
                    decision
            }

        result = (
            self.runtime
            .execute(execution)
        )

        execution_hash = (
            ProofEngine
            .execution_hash(
                execution,
                result
            )
        )

        audit_hash = (
            self.audit
            .record(
                {
                    "execution_id":
                        execution.execution_id,

                    "action":
                        execution.action_slug,

                    "hash":
                        execution_hash
                }
            )
        )

        return {

            "status":
                "executed",

            "execution_id":
                execution.execution_id,

            "result":
                result,

            "proofs": {

                "execution_hash":
                    execution_hash,

                "audit_hash":
                    audit_hash
            }
        }
