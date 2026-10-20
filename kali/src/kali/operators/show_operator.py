import json

from pathlib import Path


TARGET_EXECUTION_ID = ""


AUDIT_FILE = (
    Path(__file__)
    .parents[1]
    / "audit"
    / "audit_chain.json"
)


def main():

    with open(
        AUDIT_FILE,
        "r"
    ) as f:

        chain = json.load(f)

    for item in chain:

        event = item.get(
            "event",
            {}
        )

        if (
            event.get(
                "execution_id"
            )
            ==
            TARGET_EXECUTION_ID
        ):

            return event

    return {

        "status":
            "not_found"
    }