from __future__ import annotations

from typing import Any, Dict

from ..context import ExecutionContext
from ..kernel import Kernel
from ..actions.registry import registry


class Executor:

    def __init__(self) -> None:
        self.kernel = Kernel()

    def execute(self, ctx: ExecutionContext, action: str, payload: Dict[str, Any]) -> Any:
        if not registry.frozen:
            # In production you might want to log or raise; for now we enforce determinism.
            raise RuntimeError("ActionRegistry must be frozen before executing actions.")
        result = self.kernel.execute(ctx=ctx, action=action, payload=payload)
        return result
