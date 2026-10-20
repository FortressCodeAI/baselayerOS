from __future__ import annotations

from typing import Any, Dict

from kali.engine import execute_action


def main() -> Dict[str, Any]:
    payload = {
        "action": "ping",
        "data": {},
        "capability_envelope": [],
    }

    return execute_action(payload)
