from __future__ import annotations

from typing import Dict, List

from .events import AuditEvent
from .chain import AuditChain
from baselayeros.errors import AuditError


class AuditStore:
    """
    In-memory audit store for BaseLayerOS.

    Responsibilities:
    - persist audit events per proposal_id
    - maintain an AuditChain per proposal_id
    - expose chain head and verification
    """

    def __init__(self):
        self._chains: Dict[str, AuditChain] = {}
        self._events: Dict[str, List[AuditEvent]] = {}

    def _get_or_create_chain(self, proposal_id: str) -> AuditChain:
        if proposal_id not in self._chains:
            self._chains[proposal_id] = AuditChain()
            self._events[proposal_id] = []
        return self._chains[proposal_id]

    def append_event(self, event: AuditEvent) -> str:
        """
        Append an event to the proposal's audit chain and return the new chain head hash.
        """

        chain = self._get_or_create_chain(event.proposal_id)

        # Append to chain (validates previous_hash)
        new_head = chain.append(event)

        # Persist event
        self._events[event.proposal_id].append(event)

        return new_head

    def get_events(self, proposal_id: str) -> List[AuditEvent]:
        """
        Return all events for a proposal_id.
        """
        if proposal_id not in self._events:
            return []
        return list(self._events[proposal_id])

    def get_chain_head(self, proposal_id: str) -> str:
        """
        Return the current chain head hash for a proposal_id.
        """
        chain = self._get_or_create_chain(proposal_id)
        return chain.head()

    def verify_chain(self, proposal_id: str) -> bool:
        """
        Verify the integrity of the audit chain for a proposal_id.
        """
        if proposal_id not in self._chains:
            raise AuditError(f"No audit chain found for proposal_id={proposal_id}")

        chain = self._chains[proposal_id]
        return chain.verify()
