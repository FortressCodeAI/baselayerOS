# baselayeros/runtime/state.py
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class ExecutionState:
    workflow_id: str
    node_id: str
    context: Dict[str, Any]
    giu_burned: int = 0
    history: list[str] = None

    def advance(self, next_node_id: str) -> "ExecutionState":
        return ExecutionState(
            workflow_id=self.workflow_id,
            node_id=next_node_id,
            context=self.context.copy(),
            giu_burned=self.giu_burned,
            history=(self.history or []) + [self.node_id],
        )
