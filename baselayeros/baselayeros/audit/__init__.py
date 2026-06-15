"""
Audit subsystem for BaseLayerOS.

Provides:
- AuditEvent: canonical event representation
- AuditChain: tamper-evident SHA-256 chain
- AuditStore: persistence interface for events and chain heads
"""

from .events import AuditEvent
from .chain import AuditChain
from .store import AuditStore

__all__ = [
    "AuditEvent",
    "AuditChain",
    "AuditStore",
]
