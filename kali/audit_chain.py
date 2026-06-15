# baselayeros/kali/audit_chain.py

"""
Minimal deterministic audit chain for BaseLayerOS.
"""

from dataclasses import dataclass
from typing import Any, List


@dataclass
class AuditEvent:
    actor: str
    operation: str
    event_type: str
    detail: str


class AuditChain:
    """
    Minimal audit chain that stores events in memory.
    """

    def __init__(self) -> None:
        self.events: List[AuditEvent] = []

    def record_refusal(self, actor: str, operation: str, reason: str) -> None:
        self.events.append(
            AuditEvent(actor, operation, "refusal", reason)
        )

    def record_error(self, actor: str, operation: str, error: str) -> None:
        self.events.append(
            AuditEvent(actor, operation, "error", error)
        )

    def record_commit(self, actor: str, operation: str, state: Any) -> None:
        self.events.append(
            AuditEvent(actor, operation, "commit", repr(state))
        )
