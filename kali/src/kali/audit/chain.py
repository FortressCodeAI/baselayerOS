# audit/chain.py

import hashlib
import json

def hash_event(event):

    serialized = json.dumps(
        event,
        sort_keys=True
    )

    return hashlib.sha256(
        serialized.encode()
    ).hexdigest()


class AuditChain:

    def __init__(self):
        self.previous_hash = "GENESIS"

    def record(self, event):

        entry = {
            "previous_hash":
                self.previous_hash,
            "event":
                event
        }

        entry_hash = hash_event(entry)

        entry["entry_hash"] = entry_hash

        self.previous_hash = entry_hash

        return entry
