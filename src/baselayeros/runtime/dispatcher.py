# src/substrate/runtime/dispatcher.py

from typing import Any, Dict

from .executor import Executor
from .hooks import hooks


class Dispatcher:
    """
    Deterministic dispatcher.

    Responsibilities:
    - receive high-level execution requests
    - run pre-execution hooks
    - delegate to Executor
    - run post-execution hooks
    - return a deterministic envelope
    """

    def __init__(self, initial_state: Dict[str, Any]):
        self._executor = Executor(initial_state)

    def dispatch(
        self,
        action_name: str,
        version: str,
        params: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Dispatch a single deterministic action.

        Returns a deterministic envelope:
            {
                "action": "name:version",
                "request": {...},
                "response": {...},
                "final_context": {...},
            }
        """

        # 1. Run pre-execution hooks
        pre_context = hooks.run_pre(action_name, version, params, context)

        # 2. Execute action
        exec_result = self._executor.execute(
            action_name=action_name,
            version=version,
            params=params,
            context=pre_context,
        )

        # 3. Run post-execution hooks
        post_context = hooks.run_post(
            action_name,
            version,
            exec_result,
            pre_context,
        )

        # 4. Deterministic envelope
        return {
            "action": exec_result["action"],
            "request": {
                "params": exec_result["validated_params"],
                "initial_context": context,
                "pre_context": pre_context,
            },
            "response": {
                "result": exec_result["result"],
                "next_state": exec_result["next_state"],
                "giu_burn_receipt": exec_result["giu_burn_receipt"],
                "invariant_violations": exec_result["invariant_violations"],
            },
            "final_context": post_context,
        }
