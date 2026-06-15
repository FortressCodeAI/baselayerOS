from __future__ import annotations
from typing import Dict
from .schemas import Status

State = Status


_TRANSITIONS: Dict[State, Dict[str, State]] = {
    "draft": {"file": "filed"},
    "filed": {"start_investigation": "investigating"},
    "investigating": {"resolve": "resolved"},
    "resolved": {"close": "closed"},
    "closed": {},
}


def next_state(current: State, event: str) -> State:
    return _TRANSITIONS.get(current, {}).get(event, current)
