import hashlib
import json

def hash_payload(payload) -> str:
    serialized = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()
