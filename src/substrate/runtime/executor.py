# src/substrate/runtime/executor.py

from typing import Any, Dict

from substrate.actions.registry import registry
from substrate.invariants.verifier import verifier
from substrate.credits.burn import burner
from .state_machine import StateMachine


class Executor:
    """
    Deterministic executor for actions.

    Responsibilities:
    - load action from registry
    - validate params
    - run deterministic logic
    - burn GIU credits
    - verify invariants
    - apply state transition
    """

    def __init__(self, initial_state: Dict[str, Any]):
        self.state_machine = StateMachine(initial_state)

    def execute(
        self,
        action_name: str,
        version: str,
        params: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute a deterministic action.

        Returns:
            {
                "action": "name:version",
                "validated_params": ...,
                "result": ...,
                "next_state": ...,
                "giu_burn_receipt": ...,
                "invariant_violations": [],
            }
        """

        # 1. Load action class
        action_cls = registry.get(action_name, version)
        action = action_cls()

        # 2. Validate params deterministically
        validated = action.validate(params)

        # 3. Run deterministic action logic
        prev_state = self.state_machine.get_state()
        result = action.run(validated, prev_state)

        # 4. Burn GIU credits
        giu_receipt = burner.burn(action_name, version, action.giu_cost())

        # 5. Compute next state
        next_state = self.state_machine.apply(result)

        # 6. Verify invariants
        violations = verifier.verify(prev_state, next_state, context)

        return {
            "action": f"{action_name}:{version}",
            "validated_params": validated,
            "result": result,
            "next_state": next_state,
            "giu_burn_receipt": giu_receipt,
            "invariant_violations": violations,
        }
