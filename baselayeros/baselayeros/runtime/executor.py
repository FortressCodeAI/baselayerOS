# baselayeros/runtime/executor.py
from typing import Tuple
from .state import ExecutionState
from baselayeros.actions.registry import get_action
from baselayeros.invariants import authority, mutation, communication
from baselayeros.credits.meter import burn_giu

class StepExecutor:
    def __init__(self, graph_provider):
        self.graph_provider = graph_provider

    def step(self, state: ExecutionState, agent_id: str) -> Tuple[ExecutionState, dict]:
        node = self.graph_provider.get_node(state.workflow_id, state.node_id)
        action = get_action(node.action_id)

        authority.check(agent_id, node, state)
        mutation.check(agent_id, node, state)
        communication.check(agent_id, node, state)

        result, giu_cost = action.execute(state.context)
        burn_giu(agent_id, giu_cost)

        next_node_id = self.graph_provider.get_next_node(state.workflow_id, state.node_id, result)
        new_state = state.advance(next_node_id)
        new_state.giu_burned += giu_cost

        return new_state, {"result": result, "giu_cost": giu_cost}
