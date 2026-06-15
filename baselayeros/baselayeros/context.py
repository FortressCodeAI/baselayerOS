from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class ExecutionIdentity:
    subject_id: str
    roles: list[str]
    raw_header: str
    signature: str 

    def to_dict(self) -> Dict[str, Any]:
        return {
            "subject_id": self.subject_id,
            "roles": self.roles or [],
        }


@dataclass
class ExecutionState:
    """Opaque state wrapper; you can swap this for a real store later."""
    data: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.data)


@dataclass
class ExecutionContext:
    identity: ExecutionIdentity
    state: ExecutionState
    request_id: str
    timestamp: datetime

    @classmethod
    def from_request(cls, request: Dict[str, Any]) -> "ExecutionContext":
        ident = ExecutionIdentity(
            subject_id=request.get("subject_id", "anonymous"),
            roles=request.get("roles", []),
            raw_header=request.get("raw_header", []),
            signature=request.get("signature", []),
        )
        state = ExecutionState(data=request.get("state", {}))
        return cls(
            identity=ident,
            state=state,
            request_id=request.get("request_id", "unknown"),
            timestamp=datetime.utcnow(),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identity": self.identity.to_dict(),
            "state": self.state.to_dict(),
            "request_id": self.request_id,
            "timestamp": self.timestamp.isoformat(),
        }
