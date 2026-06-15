from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UESState:
    """
    Represents the lifecycle state of a UES proposal.

    Allowed states:
        - DRAFT
        - REVIEWED
        - OPTIMIZED
        - COMPILED
        - EXECUTED
    """

    status: str

    @staticmethod
    def initial() -> "UESState":
        return UESState(status="DRAFT")
