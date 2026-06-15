from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .context import ExecutionContext
from .actions.registry import registry


@dataclass
class KernelResult:
    output: Any
    action_name: str
    action_version: str
    context_snapshot: Dict[str, Any]


class Kernel:

    def __init__(self) -> None:
        pass

    def execute(self, ctx: ExecutionContext, action: str, payload: Dict[str, Any]) -> KernelResult:
        if action not in registry.actions:
            raise ValueError(f"Unknown action '{action}'. Registered actions: {list(registry.actions.keys())}")

        action_cls = registry.actions[action]
        action_instance = action_cls()
        output = action_instance.run(ctx=ctx, payload=payload)

        return KernelResult(
            output=output,
            action_name=action_cls.metadata.name,
            action_version=action_cls.metadata.version,
            context_snapshot=ctx.to_dict(),
        )
