from __future__ import annotations
from typing import Any, Dict, Callable, List, Optional
from dataclasses import dataclass, field

from .state_transition import StateTransition
from .event_bus import EventBus


@dataclass
class EngineContext:
    """Deterministic execution context."""
    actor: str
    run_id: str
    policy_set: str = "default"
    seed: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)


class RuntimeEngine:
    """
    Minimal deterministic runtime engine for BaseLayerOS.

    This version is intentionally self-contained:

    - No dependency on ScheduledTask
    - No dependency on DeterministicScheduler
    - No dependency on graph_provider

    It wires:
    - StateTransition (canonical state)
    - EventBus (deterministic events)
    """

    def __init__(
        self,
        engine_id: str,
        initial_state: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.engine_id = engine_id
        self._state = StateTransition(initial_state or {})
        self._events = EventBus()
        self._exec_log: List[Dict[str, Any]] = []

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def register_event_handler(
        self,
        handler: Callable[[Dict[str, Any]], None],
    ) -> None:
        """Register a deterministic event handler."""
        self._events.register_handler(handler)

    def get_state(self) -> Dict[str, Any]:
        """Return a snapshot of the current state."""
        return self._state.snapshot()

    def execute(
        self,
        ctx: EngineContext,
        command: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Deterministic execution entrypoint.

        - Applies a state transition
        - Emits a deterministic event
        - Records an execution entry
        """

        # Snapshot before
        prev_state = self._state.snapshot()

        # Derive deterministic updates
        updates = self._derive_updates(command)

        # Apply state transition
        new_state = self._state.apply(
            ctx={
                "actor": ctx.actor,
                "run_id": ctx.run_id,
                "policy_set": ctx.policy_set,
                "extra": ctx.extra,
            },
            action=command.get("type", "unknown"),
            updates=updates,
        )

        # Emit event
        event = {
            "type": "engine.command_applied",
            "run_id": ctx.run_id,
            "actor": ctx.actor,
            "policy_set": ctx.policy_set,
            "command": command,
            "state_hash": self._state.state_hash(),
        }
        emitted_event = self._events.publish(event)

        # Record execution
        record = {
            "engine_id": self.engine_id,
            "run_id": ctx.run_id,
            "command": command,
            "state_before": prev_state,
            "state_after": new_state,
            "event": emitted_event,
        }
        self._exec_log.append(record)

        # Deterministic summary
        return {
            "run_id": ctx.run_id,
            "state": new_state,
            "event": emitted_event,
        }

    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Return the execution log."""
        return list(self._exec_log)

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------

    def _derive_updates(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """
        Minimal deterministic reducer.

        Extend/replace this with domain-specific logic.
        """
        updates: Dict[str, Any] = {"_last_command": command}

        if "data" in command:
            updates["data"] = command["data"]

        return updates
