import json

from pathlib import Path

from kali.runtime.registry import (
    resolve
)

from kali.core.hashing import (
    sha256_obj
)


AUDIT_FILE = (
    Path(__file__)
    .parents[1]
    / "audit"
    / "audit_chain.json"
)


class ReplayEngine:

    @staticmethod
    def load_chain():

        if not AUDIT_FILE.exists():
            return []

        with open(
            AUDIT_FILE,
            "r"
        ) as f:

            content = (
                f.read()
                .strip()
            )

            if not content:
                return []

            return json.loads(
                content
            )

    @classmethod
    def find_execution(
        cls,
        execution_id
    ):

        chain = (
            cls.load_chain()
        )

        for item in chain:

            event = (
                item.get(
                    "event",
                    {}
                )
            )

            if (
                event.get(
                    "execution_id"
                )
                == execution_id
            ):

                return event

        return None

    @classmethod
    def replay(
        cls,
        execution_id
    ):

        event = (
            cls.find_execution(
                execution_id
            )
        )

        if event is None:

            return {
                "status":
                    "execution_not_found",

                "execution_id":
                    execution_id
            }

        handler = resolve(
            event["action"]
        )

        replay_output = (
            handler(
                event["payload"]
            )
        )

        original_hash = (
            sha256_obj(
                event["output"]
            )
        )

        replay_hash = (
            sha256_obj(
                replay_output
            )
        )

        return {

            "status":
                "replayed",

            "execution_id":
                execution_id,

            "action":
                event["action"],

            "replay_verified":
                (
                    original_hash
                    ==
                    replay_hash
                ),

            "original_hash":
                original_hash,

            "replay_hash":
                replay_hash,

            "stored_output":
                event["output"],

            "replay_output":
                replay_output
        }
