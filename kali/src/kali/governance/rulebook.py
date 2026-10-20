import hashlib
import json

RULEBOOK_VERSION = "1.1.0"

RULEBOOK = {
    "GR-001": {
        "name": "Deterministic Execution"
    },
    "GR-002": {
        "name": "Replayability"
    },
    "GR-003": {
        "name": "Auditability"
    },
    "GR-004": {
        "name": "Traceability"
    }
}

RULEBOOK_HASH = hashlib.sha256(
    json.dumps(
        RULEBOOK,
        sort_keys=True
    ).encode()
).hexdigest()