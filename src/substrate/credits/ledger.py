# src/substrate/credits/ledger.py

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _hash_record(record: Dict[str, Any]) -> str:
    """
    Deterministic hash of a ledger record.
    - stable JSON encoding
    - SHA-256 digest
    """
    encoded = json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True)
class CreditEvent:
    """
    A single GIU credit event.
    - action: name:version
    - amount: GIU burned
    - prev_hash: hash of previous event
    - hash: hash of this event
    """
    action: str
    amount: int
    prev_hash: Optional[str]
    hash: str


class CreditLedger:
    """
    Deterministic append-only GIU ledger.
    - no mutation
    - no deletion
    - no reordering
    """

    def __init__(self):
        self._events: List[CreditEvent] = []

    def append(self, action: str, amount: int):
        prev_hash = self._events[-1].hash if self._events else None

        record = {
            "action": action,
            "amount": amount,
            "prev_hash": prev_hash,
        }

        event_hash = _hash_record(record)

        event = CreditEvent(
            action=action,
            amount=amount,
            prev_hash=prev_hash,
            hash=event_hash,
        )

        self._events.append(event)

    def events(self) -> List[CreditEvent]:
        """Return a deterministic copy of all events."""
        return list(self._events)

    def total_burned(self) -> int:
        """Return total GIU burned."""
        return sum(e.amount for e in self._events)
