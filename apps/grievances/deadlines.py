from __future__ import annotations
from datetime import datetime, timedelta
from typing import TypedDict
import yaml

from .config.settings import settings


class DeadlineConfig(TypedDict):
    investigation_days: int
    meeting_days: int
    response_days: int


DEFAULTS: DeadlineConfig = {
    "investigation_days": 5,
    "meeting_days": 10,
    "response_days": 15,
}


def load_deadlines() -> DeadlineConfig:
    if not settings.deadlines_file.exists():
        return DEFAULTS
    with open(settings.deadlines_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return {
        "investigation_days": int(data.get("investigation_days", DEFAULTS["investigation_days"])),
        "meeting_days": int(data.get("meeting_days", DEFAULTS["meeting_days"])),
        "response_days": int(data.get("response_days", DEFAULTS["response_days"])),
    }


def compute_investigation_deadline(filed_date: str) -> str:
    cfg = load_deadlines()
    base = datetime.fromisoformat(filed_date)
    return (base + timedelta(days=cfg["investigation_days"])).date().isoformat()
