from __future__ import annotations

from typing import Any, Dict

from kali.engine import execute_action


def main() -> Dict[str, Any]:
    payload = {
        "action": "summarize_stream",
        "data": {
            "text": "Kali is a governed operator engine running on a deterministic substrate.",
        },
        "capability_envelope": ["summarize_stream"],
    }

    return execute_action(payload)
