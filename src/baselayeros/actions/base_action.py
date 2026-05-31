from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Protocol

from ..context import ExecutionContext


@dataclass
class ActionMetadata:
    name: str
    version: str = "1.0.0"
    description: str | None = None
    giu_cost: int = 0   # ⭐ Your credit system lives here


class BaseAction(Protocol):
    metadata: ActionMetadata

    def run(self, ctx: ExecutionContext, payload: Dict[str, Any]) -> Any:
        ...
