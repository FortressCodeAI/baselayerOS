# src/substrate/runtime/replay.py

from typing import Any, Dict, List

from ..utils.hashing import deterministic_hash
from ..invariants.verifier import verifier
from ..actions.registry import registry


class ReplayEngine:
    """
    Deterministic replay engine for substrate-level transitions.

    Responsibilities:
    - re-run actions deterministically
    - verify state transitions
    - verify invariants
    - produce a replay trace

    This is NOT the governance replay engine.
    """

    def replay(
        self,
        initial_state: Dict[str, Any],
        events: List[Dict[str, Any]],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Replay a sequence of deterministic action events.

        Each event must contain:
            {
                "action": "name:version",
                "params": {...}
            }

        Returns:
            {
                "final_state": {...},
                "trace": [...],
                "invariant_violations": [...],
                "state_hash": "..."
            }
        """

        state = dict(initial_state)
        trace = []
        all_violations = []

        for event in events:
            name, version = event["action"].split(":")
            params = event["params"]

            # Load action class
            action_cls = registry.get(name, version)
            action = action_cls()

            # Validate params
            validated = action.validate(params)

            # Run deterministic logic
            prev_state = dict(state)
            result = action.run(validated, prev_state)

            # Compute next state
            next_state = dict(prev_state)
            for k, v in result.items():
                next_state[k] = v

            # Verify invariants
            violations = verifier.verify(prev_state, next_state, context)
            all_violations.extend(violations)

            # Update state
            state = next_state

            # Append trace entry
            trace.append(
                {
                    "action": event["action"],
                    "validated_params": validated,
                    "result": result,
                    "next_state": next_state,
                    "invariant_violations": violations,
                }
            )

        # Final deterministic state hash
        state_hash = deterministic_hash(state)

        return {
            "final_state": state,
            "trace": trace,
            "invariant_violations": all_violations,
            "state_hash": state_hash,
        }


# Global instance
replay_engine = ReplayEngine()
