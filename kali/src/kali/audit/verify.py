import json

from pathlib import Path

from kali.core.hashing import (
    sha256_obj
)


AUDIT_FILE = (
    Path(__file__).parent
    / "audit_chain.json"
)


def verify_chain():

    with open(
        AUDIT_FILE,
        "r"
    ) as f:

        chain = json.load(f)

    previous = "GENESIS"

    for entry in chain:

        candidate = {

            "previous_hash":
                previous,

            "event":
                entry["event"]
        }

        expected = (
            sha256_obj(
                candidate
            )
        )

        if (
            expected
            !=
            entry["entry_hash"]
        ):

            return {
                "chain_valid":
                    False
            }

        previous = (
            entry[
                "entry_hash"
            ]
        )

    return {

        "chain_valid":
            True,

        "entries":
            len(chain)
    }