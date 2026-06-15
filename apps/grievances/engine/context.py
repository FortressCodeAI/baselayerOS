from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class EngineContext:
    actor: str
    run_id: str
    extra: Dict[str, Any] = field(default_factory=dict)
