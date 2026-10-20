# kali/substrate/governance_gate.py

from src.councils.envelope import governance_envelope

def enforce_governance(payload: dict):
    """
    Enforce governance before substrate execution.
    """

    envelope = governance_envelope(payload)
    gov = envelope["governance"]

    if not gov["passed"]:
        return {
            "allowed": False,
            "reason": "governance_failed",
            "details": gov,
        }

    return {
        "allowed": True,
        "details": gov,
    }
