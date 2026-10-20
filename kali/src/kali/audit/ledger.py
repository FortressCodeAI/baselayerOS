import json
import os
import hashlib


class AuditLedger:

    FILE = "audit_ledger.json"

    def record(
        self,
        entry
    ):

        previous = "GENESIS"

        ledger = []

        if os.path.exists(self.FILE):

            with open(self.FILE) as f:
                ledger = json.load(f)

            if ledger:
                previous = ledger[-1][
                    "entry_hash"
                ]

        packed = {
            "previous_hash":
                previous,
            "entry":
                entry
        }

        entry_hash = hashlib.sha256(
            json.dumps(
                packed,
                sort_keys=True
            ).encode()
        ).hexdigest()

        packed[
            "entry_hash"
        ] = entry_hash

        ledger.append(packed)

        with open(
            self.FILE,
            "w"
        ) as f:
            json.dump(
                ledger,
                f,
                indent=2
            )

        return entry_hash
