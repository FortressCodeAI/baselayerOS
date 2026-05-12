# src/substrate/credits/events.py

from dataclasses import dataclass
from typing import Any, Dict, Optional

from substrate.utils.hashing import deterministic_hash


@dataclass(frozen=True)
class CreditEventRecord:
    """
    A deterministic, serializable credit event record.
    This is the raw structure used before hashing.
    """
    action: str
    amount: int
    prev_hash: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "amount": self.amount,
            "prev_hash": self.prev_hash,
        }


@dataclass(frozen=True)
class CreditEventSerialized:
    """
    A fully serialized credit event with its deterministic hash.
    """
    action: str
    amount: int
    prev_hash: Optional[str]
    hash: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "amount": self.amount,
            "prev_hash": self.prev_hash,
            "hash": self.hash,
        }


class CreditEventFactory:
    """
    Deterministic factory for constructing credit events.
    """

    @staticmethod
    def create(action: str, amount: int, prev_hash: Optional[str]) -> CreditEventSerialized:
        record = CreditEventRecord(
            action=action,
            amount=amount,
            prev_hash=prev_hash,
        )

        event_hash = deterministic_hash(record.to_dict())

        return CreditEventSerialized(
            action=record.action,
            amount=record.amount,
            prev_hash=record.prev_hash,
            hash=event_hash,
        )


# Global factory instance
factory = CreditEventFactory()