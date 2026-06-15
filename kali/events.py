# baselayeros/kali/events.py

from datetime import datetime
from baselayeros.core.io.hashing import hash_payload
from kali.config import (
    REFUSAL_GIU_COST,
    COMMIT_GIU_COST,
    AUTHORITY_GATE_GIU_COST
)


def _timestamp():
    return datetime.utcnow().isoformat()


def build_refusal_event(node, input_payload, input_hash):
    """
    Canonical refusal event builder.
    Deterministic, reproducible, audit‑ready.
    """
    return {
        "event_type": "refusal",
        "timestamp": _timestamp(),
        "node_id": node.name,
        "operator_contract_clause": node.contract_clause,
        "violated_constraint": node.refusal_reason,
        "input_hash": input_hash,
        "refusal_reason": node.refusal_reason,
        "giu_burn": REFUSAL_GIU_COST
    }


def build_commit_event(node, input_hash, output_payload):
    """
    Canonical commit event builder.
    """
    output_hash = hash_payload(output_payload)

    return {
        "event_type": "commit",
        "timestamp": _timestamp(),
        "node_id": node.name,
        "operator_contract_clause": node.contract_clause,
        "input_hash": input_hash,
        "output_hash": output_hash,
        "giu_burn": COMMIT_GIU_COST
    }


def build_authority_gate_event(node, action, decision, reason):
    """
    Canonical human‑in‑the‑loop event builder.
    """
    return {
        "event_type": "authority_gate",
        "timestamp": _timestamp(),
        "node_id": node.name,
        "action_requested": action,
        "human_decision": decision,
        "decision_reason": reason,
        "operator_contract_clause": node.contract_clause,
        "giu_burn": AUTHORITY_GATE_GIU_COST
    }
