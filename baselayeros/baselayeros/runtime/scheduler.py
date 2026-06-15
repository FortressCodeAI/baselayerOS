# baselayeros/runtime/scheduler.py
from typing import Dict
from .state import ExecutionState
from .executor import StepExecutor

class DeterministicScheduler:
  def __init__(self, graph_provider):
      self.executor = StepExecutor(graph_provider)
      self.agent_states: Dict[str, ExecutionState] = {}

  def register_agent(self, agent_id: str, initial_state: ExecutionState):
      self.agent_states[agent_id] = initial_state

  def step_agent(self, agent_id: str):
      state = self.agent_states[agent_id]
      new_state, meta = self.executor.step(state, agent_id)
      self.agent_states[agent_id] = new_state
      return new_state, meta
