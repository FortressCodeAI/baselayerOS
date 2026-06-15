# baselayeros/runtime/event_bus.py

from __future__ import annotations
from typing import Any, Dict, Callable, List, Optional
import hashlib
import json
from copy import deepcopy


class EventBus:
    """
    Deterministic runtime event bus.

    Responsibilities:
    - Publish events in strict registration order
    - Maintain a hash-chained event log for auditability
    - Ensure events are immutable to callers
    - Support deterministic replay
    """

    def __init__(self) -> None:
        self._handlers: List[Callable[[Dict[str, Any]], None]] = []
        self._log: List[Dict[str, Any]] = []
        self._last_hash: str = "0" * 64  # genesis hash

    # -----------------------------
    # Public API
    # -----------------------------

    def register_handler(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Register a deterministic event handler."""
        self._handlers.append(handler)

    def publish(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Publish an event deterministically.

        - Event is deep-copied
        - Hash-chained for audit
        - Handlers invoked in registration order
        """

        event_copy = deepcopy(event)

        # Compute event hash
        event_hash = self._compute_hash(event_copy, self._last_hash)
        event_copy["_event_hash"] = event_hash
        event_copy["_prev_hash"] = self._last_hash

        # Append to log
        self._log.append(event_copy)
        self._last_hash = event_hash

        # Invoke handlers
        for handler in self._handlers:
            handler(deepcopy(event_copy))

        return event_copy

    def get_log(self) -> List[Dict[str, Any]]:
        """Return a deep copy of the full event log."""
        return deepcopy(self._log)

    def replay(
        self,
        handler: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> None:
        """
        Replay all events deterministically.

        - If handler is provided, replay through that handler only
        - Otherwise replay through all registered handlers
        """
        if handler:
            for event in self._log:
                handler(deepcopy(event))
        else:
            for event in self._log:
                for h in self._handlers:
                    h(deepcopy(event))

    # -----------------------------
    # Internal helpers
    # -----------------------------

    def _compute_hash(self, event: Dict[str, Any], prev_hash: str) -> str:
        """
        Compute a deterministic hash for the event.

        - Includes previous hash (hash chaining)
        - JSON-serialized with sorted keys
        """
        payload = {
            "event": event,
            "prev_hash": prev_hash,
        }
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
