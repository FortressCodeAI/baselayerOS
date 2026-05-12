# src/substrate/utils/hashing.py

import hashlib
import json
from typing import Any, Dict


def deterministic_hash(data: Dict[str, Any]) -> str:
    """
    Deterministic SHA-256 hash of a JSON-serializable dict.

    - stable key ordering
    - stable separators
    - no whitespace variance
    """
    encoded = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return hashlib.sha256(encoded).hexdigest()
