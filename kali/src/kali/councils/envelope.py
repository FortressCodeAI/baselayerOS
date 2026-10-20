# kali/councils/envelope.py

import hashlib
import json
from kali.src.kali.councils.council import evaluate

def governance_envelope(payload: dict):
    """
    Wrap governance evaluation in a deterministic envelope.
    """

    # Deterministic input hash
    input_hash = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()

    result = evaluate(payload)

    # Deterministic output hash
    output_hash = hashlib.sha256(
        json.dumps(result, sort_keys=True).encode()
    ).hexdigest()

    return {
        "input_hash": input_hash,
        "output_hash": output_hash,
        "governance": result,
    }
