"""
Kali v1.0.0 — Capability Engine

Ensures that requested actions stay within:
- declared capability scope
- Kali Standard guarantees

This engine is:
- deterministic
- rule-based
- enforcement-first
"""

from __future__ import annotations
from typing import Dict, Any

from kali.core.config import KaliConfig
from kali.core.logging import KaliLogger
from kali.core.constants import (
    CAP_SCOPE_READ_ONLY,
    CAP_SCOPE_WORKFLOW,
    CAP_SCOPE_WRITE_LIMITED,
)
from kali.core.errors import CapabilityViolationError


class CapabilityEngine:
    def __init__(self, config: KaliConfig, logger: KaliLogger):
        self.config = config
        self.logger = logger

    def enforce(self, scope_name: str, request: Dict[str, Any]) -> None:
        """
        Enforce capability scope against a request.

        scope_name: one of CAP_SCOPE_READ_ONLY, CAP_SCOPE_WORKFLOW, CAP_SCOPE_WRITE_LIMITED
        request: {
            "action": "read" | "start_workflow" | "write_limited" | ...
        }
        """
        action = request.get("action", "read")

        if scope_name == CAP_SCOPE_READ_ONLY:
            allowed = ["read"]
        elif scope_name == CAP_SCOPE_WORKFLOW:
            allowed = ["read", "start_workflow", "inspect_workflow", "replay"]
        elif scope_name == CAP_SCOPE_WRITE_LIMITED:
            allowed = ["read", "write_limited"]
        else:
            # Unknown scope: treat as read-only
            allowed = ["read"]

        if action not in allowed:
            self.logger.error(
                "capability_violation",
                scope=scope_name,
                action=action,
                allowed=allowed,
            )
            raise CapabilityViolationError(
                f"Action '{action}' is not allowed under capability scope '{scope_name}'."
            )

        self.logger.info(
            "capability_enforced",
            scope=scope_name,
            action=action,
            allowed=allowed,
        )
