# baselayeros/runtime/replay.py
from typing import Iterable
from .state import ExecutionState

class ReplayEngine:
    def replay(self, initial_state: ExecutionState, events: Iterable[dict]) -> ExecutionState:
        state = initial_state
        for event in events:
            state = state.advance(event["node_id"])
        return state
