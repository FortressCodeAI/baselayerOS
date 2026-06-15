from __future__ import annotations
from pathlib import Path
from typing import BinaryIO

from ..config.settings import settings


def grievance_dir(grievance_id: int) -> Path:
    d = settings.attachment_dir / str(grievance_id)
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_attachment(grievance_id: int, filename: str, stream: BinaryIO) -> Path:
    target = grievance_dir(grievance_id) / filename
    with open(target, "wb") as f:
        f.write(stream.read())
    return target
