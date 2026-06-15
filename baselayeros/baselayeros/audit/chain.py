from __future__ import annotations

import hashlib
from typing import List

from .events import AuditEvent
from baselayeros.errors import AuditError


class AuditChain:
    """
    A tamper-evident SHA-256 audit chain.

    Each event includes:
        - its own canonical JSON
        - the hash of the previous event

    The chain head is stored in the UES object and updated after every event.
    """

    def __init__(self):
        self._events: List[AuditEvent] = []

    @staticmethod
    def _hash_event(event: AuditEvent) -> str:
        """Compute SHA-256 hash of the event's canonical JSON."""
        encoded = event.to_json().encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def append(self, event: AuditEvent) -> str:
        """
        Append an event to the chain and return the new chain head hash.
        Validates that the event's previous_hash matches the current chain head.
        """

        if self._events:
            current_head = self._hash_event(self._events[-1])
            if event.previous_hash != current_head:
                raise AuditError(
                    f"Invalid previous_hash: expected {current_head}, got {event.previous_hash}"
                )
        else:
            # First event must declare previous_hash = "GENESIS"
            if event.previous_hash != "GENESIS":
                raise AuditError("First event must have previous_hash='GENESIS'")

        self._events.append(event)
        return self._hash_event(event)

    def verify(self) -> bool:
        """
        Verify the integrity of the entire chain.
        Returns True if valid, raises AuditError if tampering is detected.
        """

        for i, event in enumerate(self._events):
            expected_prev = "GENESIS" if i == 0 else self._hash_event(self._events[i - 1])
            if event.previous_hash != expected_prev:
                raise AuditError(
                    f"Audit chain tampering detected at event {event.event_id}: "
                    f"expected previous_hash={expected_prev}, got {event.previous_hash}"
                )

        return True

    def head(self) -> str:
        """Return the current chain head hash."""
        if not self._events:
            return "GENESIS"
        return self._hash_event(self._events[-1])

    def events(self) -> List[AuditEvent]:
        """Return a copy of the event list."""
        return list(self._events)
