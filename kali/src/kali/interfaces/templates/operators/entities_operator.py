from __future__ import annotations

from typing import Any, Dict

from kali.engine import execute_action


def main() -> Dict[str, Any]:
    payload = {
        "action": "extract_entities",
        "data": {
            "text": "James built Kali on BaseLayerOS in Kitchener, Ontario.",
        },
        "capability_envelope": ["extract_entities"],
    }

    return execute_action(payload)
