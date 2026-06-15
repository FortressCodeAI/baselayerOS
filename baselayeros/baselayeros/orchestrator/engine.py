from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from schema.ues.v1_0_0.ues_types import UES
from baselayeros.ues.state_machine import UESStateMachine
from baselayeros.councils.router import CouncilRouter
from baselayeros.compiler.contract import CompilerContract
from baselayeros.executor.runtime import RuntimeExecutor
from baselayeros.audit.events import AuditEvent
from baselayeros.audit.store import AuditStore
from baselayeros.errors import BaseLayerError


class OrchestratorEngine:
    """
    The deterministic BaseLayerOS pipeline:

        1. Validate UES structure (Council 1)
        2. Validate risk/cost/time/safety/compliance (Council 2)
        3. Transition → OPTIMIZED
        4. Compile deterministically
        5. Transition → COMPILED
        6. Execute deterministically
        7. Transition → EXECUTED

    Every step emits an audit event.
    """

    def __init__(self):
        self.state_machine = UESStateMachine()
        self.councils = CouncilRouter()
        self.compiler = CompilerContract()
        self.executor = RuntimeExecutor()
        self.audit = AuditStore()

    # ---------------------------------------------------------
    # Main pipeline
    # ---------------------------------------------------------
    def run(self, ues: UES, actor: str, actor_org: str, actor_roles: list[str]) -> Dict[str, Any]:
        """
        Run the full deterministic pipeline on a UES proposal.
        """

        # 1. Council review
        ues = self._audit_step(
            ues,
            action="COUNCIL_REVIEW",
            actor=actor,
            actor_org=actor_org,
            actor_roles=actor_roles,
            fn=lambda u: self.councils.run_all(u),
        )

        # 2. Transition → OPTIMIZED
        ues = self._transition(ues, "OPTIMIZED", actor, actor_org, actor_roles)

        # 3. Compile
        compiled = self._audit_step(
            ues,
            action="COMPILE",
            actor=actor,
            actor_org=actor_org,
            actor_roles=actor_roles,
            fn=lambda u: self.compiler.compile(u),
        )

        # 4. Transition → COMPILED
        ues = self._transition(ues, "COMPILED", actor, actor_org, actor_roles)

        # 5. Execute
        result = self._audit_step(
            ues,
            action="EXECUTE",
            actor=actor,
            actor_org=actor_org,
            actor_roles=actor_roles,
            fn=lambda u: self.executor.run(u, compiled.__dict__),
        )

        # 6. Transition → EXECUTED
        ues = self._transition(ues, "EXECUTED", actor, actor_org, actor_roles)

        return {
            "proposal_id": ues.audit.proposal_id,
            "state": ues.state.status,
            "result": result.outputs,
            "success": result.success,
        }

    # ---------------------------------------------------------
    # Audit wrapper
    # ---------------------------------------------------------
    def _audit_step(
        self,
        ues: UES,
        action: str,
        actor: str,
        actor_org: str,
        actor_roles: list[str],
        fn,
    ):
        """
        Wrap a pipeline step with audit logging.
        """

        timestamp = datetime.utcnow().isoformat()
        prev_hash = self.audit.get_chain_head(ues.audit.proposal_id)

        event = AuditEvent(
            event_id=f"{ues.audit.proposal_id}:{action}:{timestamp}",
            proposal_id=ues.audit.proposal_id,
            timestamp=timestamp,
            actor_id=actor,
            actor_org=actor_org,
            actor_roles=actor_roles,
            action=action,
            details={},
            previous_hash=prev_hash,
        )

        # Execute step
        try:
            result = fn(ues)
        except BaseLayerError as e:
            event.details = {"error": str(e)}
            self.audit.append_event(event)
            raise

        # Success
        event.details = {"status": "OK"}
        self.audit.append_event(event)
        return result

    # ---------------------------------------------------------
    # State transitions
    # ---------------------------------------------------------
    def _transition(self, ues: UES, target: str, actor: str, actor_org: str, actor_roles: list[str]) -> UES:
        timestamp = datetime.utcnow().isoformat()
        prev_hash = self.audit.get_chain_head(ues.audit.proposal_id)

        event = AuditEvent(
            event_id=f"{ues.audit.proposal_id}:TRANSITION:{ues.state.status}->{target}:{timestamp}",
            proposal_id=ues.audit.proposal_id,
            timestamp=timestamp,
            actor_id=actor,
            actor_org=actor_org,
            actor_roles=actor_roles,
            action="STATE_TRANSITION",
            details={"from": ues.state.status, "to": target},
            previous_hash=prev_hash,
        )

        ues = self.state_machine.transition(
            ues,
            target=target,
            actor=actor,
            timestamp=timestamp,
        )

        self.audit.append_event(event)
        return ues
