from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
import uuid


@dataclass(frozen=True)
class LedgerEntry:
    id: str
    account_id: str
    direction: str  # "credit" | "debit"
    amount: int
    source: str     # "purchase" | "burn" | "adjustment" | "payout"
    audit_id: str | None
    builder_share: int
    created_at: str


class Billing:
    def __init__(self, path: Path | None = None) -> None:
        self._ledger_path = path or Path(".baselayeros/giu_ledger.jsonl")
        self._ledger_path.parent.mkdir(parents=True, exist_ok=True)

    def _append(self, entry: LedgerEntry) -> None:
        with self._ledger_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry), separators=(",", ":")))
            f.write("\n")

    def credit_purchase(self, account_id: str, amount: int) -> None:
        entry = LedgerEntry(
            id=str(uuid.uuid4()),
            account_id=account_id,
            direction="credit",
            amount=amount,
            source="purchase",
            audit_id=None,
            builder_share=0,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._append(entry)

    def burn(
        self,
        customer_id: str,
        builder_id: str | None,
        amount: int,
        audit_id: str,
    ) -> None:
        """Burn GIUs for a customer and credit builder revenue share."""
        if amount <= 0:
            return

        # Customer debit
        debit = LedgerEntry(
            id=str(uuid.uuid4()),
            account_id=customer_id,
            direction="debit",
            amount=amount,
            source="burn",
            audit_id=audit_id,
            builder_share=0,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._append(debit)

        # Builder revenue share (25%)
        if builder_id:
            share = int(amount * 0.25)
            credit = LedgerEntry(
                id=str(uuid.uuid4()),
                account_id=builder_id,
                direction="credit",
                amount=share,
                source="burn",
                audit_id=audit_id,
                builder_share=share,
                created_at=datetime.now(timezone.utc).isoformat(),
            )
            self._append(credit)

    def balance(self, account_id: str) -> int:
        if not self._ledger_path.exists():
            return 0

        bal = 0
        with self._ledger_path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                rec = json.loads(line)
                if rec["account_id"] != account_id:
                    continue
                if rec["direction"] == "credit":
                    bal += rec["amount"]
                else:
                    bal -= rec["amount"]
        return bal
