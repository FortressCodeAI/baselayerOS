from typing import Any, Dict, List, Callable, Optional
from .state_transition import StateTransition
from .event_bus import EventBus

class StepExecutor:

    def __init__(
            self,
            transition: Optional[State_Transition] = None,
            event_bus: Optional[EventBus] = None,
    ) -> None:
        self._transition = transition or StateTransition()
        self._event_bus = event_bus or EventBus()

    def execute_step(
            self,
            ctx: Dict[str, Any],
            step_name: str,
            step_fn: Callable[[Dict[str, Any]]],
            payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        
        pre-state = self._tansition.snapshot()
        output = step_fn (payload)