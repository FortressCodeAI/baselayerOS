# src/substrate/actions/builtin/echo.py

from substrate.actions.base_action import BaseAction, ActionMetadata


class EchoAction(BaseAction):
    """
    Deterministic builtin action.
    Simply returns the input params as output.
    """

    metadata = ActionMetadata(
        name="echo",
        version="1.0",
        giu_cost=1,
        description="Returns the input parameters unchanged."
    )

    def validate(self, params):
        # Deterministic: shallow copy only
        if not isinstance(params, dict):
            raise ValueError("EchoAction params must be an object.")
        return dict(params)

    def run(self, params, state):
        # Deterministic: return params as next-state updates
        return dict(params)
