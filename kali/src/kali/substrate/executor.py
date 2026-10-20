import json
import hashlib
import subprocess


def _hash(data) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


def call_substrate(payload: dict) -> dict:
    """
    Adapter to BaseLayerOS substrate.

    For now, this uses a CLI call. Replace with FFI when ready.
    """
    result = subprocess.run(
        ["baselayeros", "execute", json.dumps(payload)],
        capture_output=True,
        text=True,
        check=False,
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


def execute(payload: dict) -> dict:
    """
    Governance‑gated, deterministic execution wrapper.
    """
    # Input hash for audit
    input_hash = _hash(payload)

    # Call substrate
    result = call_substrate(payload)

    # Output hash for audit
    output_hash = _hash(result)

    return {
        "status": "executed",
        "input_hash": input_hash,
        "output_hash": output_hash,
        "result": result,
    }
