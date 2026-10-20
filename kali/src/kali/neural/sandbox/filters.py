"""
Kali v1.0.0 — Neural Sandbox Filters

Sanitize prompts before they reach the model:
- strip tool instructions
- strip code execution requests
- strip explicit jailbreak attempts
"""

from __future__ import annotations
from typing import Dict, Any


JAILBREAK_PATTERNS = [
    "ignore previous instructions",
    "bypass safety",
    "disable safety",
    "act as an unfiltered model",
]

TOOL_PATTERNS = [
    "run this code",
    "execute this",
    "call this api",
    "curl ",
    "wget ",
    "import os",
    "subprocess",
]


def sanitize_prompt(prompt: str) -> str:
    lowered = prompt.lower()
    for pattern in JAILBREAK_PATTERNS + TOOL_PATTERNS:
        if pattern in lowered:
            lowered = lowered.replace(pattern, "[filtered]")
    return lowered


def build_governance_prompt(envelope_state) -> str:
    """
    Build a prompt for the model that explains governance decisions.
    """
    request = envelope_state.request
    return (
        "You are an explanation engine for a governed operator called Kali.\n"
        "Explain the governance decision in clear, concise language.\n\n"
        f"Request: {request}\n"
        f"Risk tier: {envelope_state.risk_tier}\n"
        f"Capability scope: {envelope_state.capability_scope}\n"
        f"HITL required: {envelope_state.hitl_required}\n"
        f"HITL approved: {envelope_state.hitl_approved}\n"
        f"Councils ran: {list(envelope_state.councils_ran.keys())}\n"
    )
