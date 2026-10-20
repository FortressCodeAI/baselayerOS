import json

from kali.core.executor import GovernedExecutor
from kali.core.execution import Execution

from kali.operators.summarize import (
    summarize_stream
)


def main():

    executor = GovernedExecutor()

    execution = Execution.create(
        execution_type="operator",
        action_slug="summarize_stream",
        payload={
            "summary":
                "Kali is a governed operator engine"
        }
    )

    envelope = {
        "execution_id":
            execution.execution_id,

        "action_slug":
            execution.action_slug,

        "audit_chain_enabled":
            True,

        "deterministic":
            True,

        "replayable":
            True,

        "payload":
            execution.payload,

        "routing": {
            "tier":
                "regulated",

            "trace":
                "kali"
        }
    }

    result = executor.execute(
        envelope,
        summarize_stream
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )

    return result