"""
Kali v1.0.0 — Neural Sandbox Logger

Separate logger for:
- prompts sent to the model
- filtered prompts
- raw outputs
- filtered outputs
"""

from __future__ import annotations
import json
import os
import datetime
from typing import Any, Dict


SANDBOX_LOG_PATH = os.environ.get("KALI_SANDBOX_LOG_PATH", "logs/kali_sandbox.log")


class SandboxLogger:
    def __init__(self):
        os.makedirs(os.path.dirname(SANDBOX_LOG_PATH), exist_ok=True)

    def _ts(self) -> str:
        return datetime.datetime.utcnow().isoformat() + "Z"

    def _write(self, record: Dict[str, Any]) -> None:
        with open(SANDBOX_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def log(self, kind: str, **fields: Any) -> None:
        self._write({"ts": self._ts(), "kind": kind, "fields": fields})
