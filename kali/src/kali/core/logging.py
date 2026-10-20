"""
Kali v1.0.0 — Deterministic Logging System

Kali's logging MUST be:
- deterministic
- structured
- replayable
- auditable
- JSON-safe

This logger is used across:
- symbolic governance core
- neural sandbox
- operators
- councils
- substrate adapter
"""

import json
import datetime
import os
from typing import Any, Dict


LOG_PATH = os.environ.get("KALI_LOG_PATH", "logs/kali.log")


class KaliLogger:
    def __init__(self, name: str):
        self.name = name
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    def _timestamp(self) -> str:
        return datetime.datetime.utcnow().isoformat() + "Z"

    def _write(self, record: Dict[str, Any]) -> None:
        """
        Deterministic JSON log record.
        """
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def info(self, message: str, **fields: Any) -> None:
        self._write({
            "ts": self._timestamp(),
            "level": "INFO",
            "component": self.name,
            "message": message,
            "fields": fields,
        })

    def warn(self, message: str, **fields: Any) -> None:
        self._write({
            "ts": self._timestamp(),
            "level": "WARN",
            "component": self.name,
            "message": message,
            "fields": fields,
        })

    def error(self, message: str, **fields: Any) -> None:
        self._write({
            "ts": self._timestamp(),
            "level": "ERROR",
            "component": self.name,
            "message": message,
            "fields": fields,
        })


def get_logger(name: str) -> KaliLogger:
    return KaliLogger(name)
