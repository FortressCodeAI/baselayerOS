from pathlib import Path
import json

from kali.core.hashing import sha256_obj


AUDIT_FILE = (
    Path(__file__).parents[2]
    / "audit"
    / "audit_chain.json"
)


def load_chain():

    if not AUDIT_FILE.exists():
        return []

    with open(AUDIT_FILE, "r") as f:
        return json.load(f)


def save_chain(chain):

    AUDIT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(AUDIT_FILE, "w") as f:
        json.dump(
            chain,
            f,
            indent=2
        )


def append_event(event):

    chain = load_chain()

    previous_hash = (
        chain[-1]["entry_hash"]
        if chain
        else "GENESIS"
    )

    record = {
        "previous_hash": previous_hash,
        "event": event
    }

    entry_hash = sha256_obj(record)

    record["entry_hash"] = entry_hash

    chain.append(record)

    save_chain(chain)

    return {
        "proof_type": "audit_chain",
        "entry_hash": entry_hash,
        "previous_hash": previous_hash,
        "chain_length": len(chain)
    }