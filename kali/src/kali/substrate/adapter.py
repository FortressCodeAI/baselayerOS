import subprocess
import json
import hashlib
from typing import Any, Dict

from .envelopes import build_substrate_envelope


def _hash(data: Dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def call_substrate(payload: Dict[str, Any]) -> Dict[str, Any]:
    result = subprocess.run(
        ["baselayeros", "execute", json.dumps(payload)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return {
            "status": "substrate_error",
            "stderr": result.stderr,
        }

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "status": "substrate_invalid_output",
            "raw": result.stdout,
        }


def execute(payload: Dict[str, Any]) -> Dict[str, Any]:
    envelope = build_substrate_envelope(payload["action"], payload.get("data", {}))

    input_hash = _hash(envelope)
    result = call_substrate(envelope)
    output_hash = _hash(result)

    return {
        "status": "executed",
        "input_hash": input_hash,
        "output_hash": output_hash,
        "result": result,
    }
