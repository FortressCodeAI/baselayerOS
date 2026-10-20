import hashlib
import json


def canonical_json(data):
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":")
    )


def sha256_obj(data):

    payload = canonical_json(data).encode()

    return hashlib.sha256(payload).hexdigest()
