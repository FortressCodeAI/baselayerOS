import json

from pathlib import Path


AUDIT_FILE = (
    Path(__file__)
    .parents[1]
    / "audit"
    / "audit_chain.json"
)


def main():

    if not AUDIT_FILE.exists():

        return []

    with open(
        AUDIT_FILE,
        "r"
    ) as f:

        chain = json.load(f)

    history = []

    for record in chain:

        event = (
            record.get(
                "event",
                {}
            )
        )

        history.append({

            "execution_id":
                event.get(
                    "execution_id"
                ),

            "action":
                event.get(
                    "action"
                )
        })

    return history