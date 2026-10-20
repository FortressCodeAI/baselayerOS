"""
Kali v1.0.0 — Global State Container

This module holds the runtime state for:
- active envelope
- risk tier
- capability scope
- replay context
- council decisions
- HITL status

Kali's state MUST be:
- deterministic
- serializable
- replayable
- immutable once finalized
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class EnvelopeState:
    envelope_id: str
    request: Dict[str, Any]
    risk_tier: Optional[str] = None
    capability_scope: Optional[str] = None
    councils_ran: Dict[str, Any] = field(default_factory=dict)
    hitl_required: bool = False
    hitl_approved: bool = False
    replay_log: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KaliState:
    """
    Top-level state object for Kali's governance cycle.
    """

    active_envelope: Optional[EnvelopeState] = None

    def start_envelope(self, envelope_id: str, request: Dict[str, Any]) -> None:
        self.active_envelope = EnvelopeState(
            envelope_id=envelope_id,
            request=request,
        )

    def set_risk_tier(self, tier: str) -> None:
        if not self.active_envelope:
            raise RuntimeError("No active envelope to set risk tier.")
        self.active_envelope.risk_tier = tier

    def set_capability_scope(self, scope: str) -> None:
        if not self.active_envelope:
            raise RuntimeError("No active envelope to set capability scope.")
        self.active_envelope.capability_scope = scope

    def add_council_result(self, council: str, result: Any) -> None:
        if not self.active_envelope:
            raise RuntimeError("No active envelope to add council result.")
        self.active_envelope.councils_ran[council] = result

    def require_hitl(self) -> None:
        if not self.active_envelope:
            raise RuntimeError("No active envelope to mark HITL.")
        self.active_envelope.hitl_required = True

    def approve_hitl(self) -> None:
        if not self.active_envelope:
            raise RuntimeError("No active envelope to approve HITL.")
        self.active_envelope.hitl_approved = True

    def add_replay_event(self, event: str, data: Any) -> None:
        if not self.active_envelope:
            raise RuntimeError("No active envelope to add replay event.")
        self.active_envelope.replay_log[event] = data

    def finalize(self) -> EnvelopeState:
        """
        Freeze the envelope for deterministic replay.
        """
        if not self.active_envelope:
            raise RuntimeError("No active envelope to finalize.")
        return self.active_envelope
