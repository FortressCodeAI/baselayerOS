"""
baselayeros.credits.ledger

Deterministic append-only GIU ledger.
Compatible with meter.py burn_giu().
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from decimal import Decimal
from uuid import uuid4
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Protocol



# ---------- Ledger Event Model ----------

@dataclass(frozen=True)
class LedgerEvent:
    event_id: str
    account_id: str
    giu_delta: Decimal
    reason: str
    category: str
    created_at: str
    context: Dict[str, Any]


# Ledger Implementation
class Ledger:

    def __init__(self) -> None:
        self._events: List[LedgerEvent] = []
        self._balances: Dict[str, Decimal] = {}

    # Internal helpers

    @staticmethod
    def _now_iso8601() -> str:
        return datetime.now(timezone.utc).isoformat()

    def _append_event(self, event: LedgerEvent) -> None:
        self._events.append(event)

        # Update balance deterministically
        prev = self._balances.get(event.account_id, Decimal("0"))
        new = prev + event.giu_delta

        if new < 0:
            raise ValueError(
                f"Ledger underflow for account '{event.account_id}'. "
                f"Attempted delta={event.giu_delta}, balance={prev}"
            )

        self._balances[event.account_id] = new

    # Public API

    def credit(self, account_id: str, amount: Decimal, *, reason: str, category: str = "system", context=None) -> LedgerEvent:
        if amount <= 0:
            raise ValueError("Credit amount must be positive")

        event = LedgerEvent(
            event_id=str(uuid4()),
            account_id=account_id,
            giu_delta=amount,
            reason=reason,
            category=category,
            created_at=self._now_iso8601(),
            context=context or {},
        )

        self._append_event(event)
        return event

    def burn(self, account_id: str, amount: Decimal, *, reason: str, category: str, context=None) -> LedgerEvent:
        
        if amount <= 0:
            raise ValueError("Burn amount must be positive")

        event = LedgerEvent(
            event_id=str(uuid4()),
            account_id=account_id,
            giu_delta=-amount,
            reason=reason,
            category=category,
            created_at=self._now_iso8601(),
            context=context or {},
        )
        self._append_event(event)
        return event

    def get_balance(self, account_id: str) -> Decimal:
        return self._balances.get(account_id, Decimal("0"))

    def events(self) -> List[LedgerEvent]:
        return list(self._events)

    def export(self) -> List[Dict[str, any]]:
        return [asdict(e) for e in self._events]
