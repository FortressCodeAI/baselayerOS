from __future__ import annotations
from typing import Any, Dict

def build_substrate_envelope(action: str, data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "action_slug": action,
        "payload": data,
        "deterministic": True,
        "replayable": True,
        "audit_chain_enabled": True,
        "routing": {
            "tier": "regulated",
            "trace": "kali",
        },
    }
