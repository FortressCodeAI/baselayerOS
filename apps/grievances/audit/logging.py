from __future__ import annotations
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import Any, Dict
from pathlib import Path

from ..config.settings import settings


LOG_FILE: Path = settings.log_dir / "grievance_audit.log"

logger = logging.getLogger("baselayeros.audit")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=5)
formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def audit(actor: str, action: str, payload: Dict[str, Any]) -> None:
    record = {
        "actor": actor,
        "action": action,
        "payload": payload,
        "ts": datetime.utcnow().isoformat(),
    }
    logger.info(json.dumps(record, separators=(",", ":")))
