from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass(frozen=True)
class AuditEvent:
    """
    A single audit event in the BaseLayerOS substrate.

    Every state transition, council decision, compilation, and execution step
    must emit an AuditEvent. These events are chained together using SHA-256
    to provide tamper-evident replayability.
    """

    event_id: str
    proposal_id: str
    timestamp: str
    actor_id: str
    actor_org: str
    actor_roles: list[str]
    action: str
    details: Dict[str, Any]
    previous_hash: str

    def to_json(self) -> str:
        """Return canonical JSON representation for hashing and storage."""
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))
