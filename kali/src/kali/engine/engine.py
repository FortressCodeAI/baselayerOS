from __future__ import annotations

from typing import Any, Dict, List

from ..governance.governance import validate_capability
from ..governance.envelopes import apply_envelopes
from ..governance.audit import record_audit
from ..governance.errors import GovernanceError
from kali.substrate.adapter import execute as substrate_execute


def execute_action(payload: Dict[str, Any]) -> Dict[str, Any]:
    # Extract action safely
    raw_action = payload.get("action")
    if not isinstance(raw_action, str):
        raise GovernanceError("Payload missing required string field: 'action'")

    action: str = raw_action

    # Extract data safely
    raw_data = payload.get("data", {})
    if not isinstance(raw_data, dict):
        raise GovernanceError("Payload field 'data' must be a dict")

    data: Dict[str, Any] = raw_data

    # Extract envelopes safely
    raw_env = payload.get("capability_envelope", [])
    if not isinstance(raw_env, list):
        raise GovernanceError("Payload field 'capability_envelope' must be a list")

    envelopes: List[str] = [str(e) for e in raw_env]

    # Governance validation
    if not validate_capability(action, envelopes):
        raise GovernanceError(
            f"Action '{action}' not permitted under envelopes {envelopes}"
        )

    # Apply envelopes (priority collapse, summarization, etc.)
    governed_data = apply_envelopes(action, data, envelopes)

    # Execute deterministically on substrate
    result = substrate_execute(
        {
            "action": action,
            "data": governed_data,
            "deterministic": True,
            "replayable": True,
            "audit_chain_enabled": True,
        }
    )

    # Audit chain
    record_audit(action, governed_data, result)

    return {
        "status": "ok",
        "action": action,
        "input": governed_data,
        "result": result,
    }


def execute_workflow(
    steps: List[Dict[str, Any]], meta: Dict[str, Any] | None = None
) -> Dict[str, Any]:
    outputs: List[Dict[str, Any]] = []

    for step in steps:
        outputs.append(execute_action(step))

    return {
        "status": "workflow_complete",
        "steps": outputs,
        "meta": meta or {},
    }
