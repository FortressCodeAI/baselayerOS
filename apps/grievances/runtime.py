from __future__ import annotations
from typing import Dict, Any

from sqlalchemy.orm import Session

from apps.grievances.engine.context import EngineContext
from apps.grievances.models import Grievance
from apps.grievances.repositories import update_grievance
from apps.grievances.state_machine import next_state, Status
from apps.grievances.policy import check_status_transition
from apps.grievances.audit.logging import audit


def apply_command(
    db: Session,
    ctx: EngineContext,
    grievance: Grievance,
    command: Dict[str, Any],
) -> Grievance:
    """
    Deterministic command handler for grievance lifecycle.
    """
    action = command.get("type")
    payload = command.get("payload", {})

    if action == "update_fields":
        for field in ("issue_summary", "requested_remedy", "notes"):
            if field in payload:
                setattr(grievance, field, payload[field])

    if action == "transition":
        event = payload.get("event")
        if event:
            current: Status = grievance.status  # type: ignore[assignment]
            target: Status = next_state(current, event)
            decision = check_status_transition(current, target)
            if decision["decision"] == "ALLOW":
                grievance.status = target # type: ignore[assignment]

    updated = update_grievance(db, grievance)
    audit(
        actor=ctx.actor,
        action=f"command:{action}",
        payload={"grievance_id": grievance.id, "command": command},
    )
    return updated
