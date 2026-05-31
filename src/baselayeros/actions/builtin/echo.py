from __future__ import annotations

from ..base_action import ActionMetadata
from ...context import ExecutionContext


class EchoAction:

    metadata = ActionMetadata(
        name="echo",
        version="1.0.0",
        description="Return the payload unchanged.",
        giu_cost=1,
        )

    def run(self, ctx: ExecutionContext, payload: dict):
        return {
            "echo": payload,
            "request_id": ctx.request_id,
            "subject": ctx.identity.subject_id,
            "timestamp": ctx.timestamp.isoformat(),
        }
