# baselayeros/runtime/state_transition.py

from __future__ import annotations
from typing import Any, Dict, Optional
from copy import deepcopy
import hashlib
import json


class StateTransition:

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None) -> None:
        self._state: Dict[str, Any] = deepcopy(initial_state or {})
        self._state_hash = self._compute_hash(self._state)


    def snapshot(self) -> Dict[str, Any]:
        return deepcopy(self._state)

    def state_hash(self) -> str:
        return self._state_hash

    def apply(
        self,
        ctx: Dict[str, Any],
        action: str,
        updates: Dict[str, Any],
    ) -> Dict[str, Any]:
        next_state = deepcopy(self._state)

        for key, value in updates.items():
            next_state[key] = deepcopy(value)

        next_state["_last_action"] = action
        next_state["_last_actor"] = ctx.get("actor")
        next_state["_last_ctx"] = {k: v for k, v in ctx.items() if k != "state"}


        self._state = next_state
        self._state_hash = self._compute_hash(self._state)

        return deepcopy(self._state)

    def _compute_hash(self, state: Dict[str, Any]) -> str:
        serialized = json.dumps(state, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
