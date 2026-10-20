import hashlib
import json


class ProofEngine:

    @staticmethod
    def execution_hash(
        execution,
        result
    ):

        material = {

            "action":
                execution.action_slug,

            "payload":
                execution.payload,

            "result":
                result
        }

        return hashlib.sha256(
            json.dumps(
                material,
                sort_keys=True
            ).encode()
        ).hexdigest()
