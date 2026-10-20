"""
Kali v1.0.0 — Risk Engine

Classifies requests into risk tiers based on:
- action type
- capability scope
- resource sensitivity
- environment

This engine is:
- deterministic
- rule-based
- replayable
"""

from __future__ import annotations
from typing import Dict, Any

from kali.core.config import KaliConfig
from kali.core.logging import KaliLogger
from kali.core.constants import (
    RISK_TIER_LOW,
    RISK_TIER_MEDIUM,
    RISK_TIER_HIGH,
    RISK_TIER_CRITICAL,
)


class RiskEngine:
    def __init__(self, config: KaliConfig, logger: KaliLogger):
        self.config = config
        self.logger = logger

    def classify(self, request: Dict[str, Any]) -> str:
        """
        Determine risk tier for a given request.

        Expected request shape (simplified v1.0.0):
        {
            "action": "start_workflow" | "read" | "write_limited" | ...,
            "resource_type": "config" | "data" | "financial" | "medical" | ...,
            "external_api": bool,
        }
        """
        action = request.get("action", "read")
        resource_type = request.get("resource_type", "data")
        external_api = bool(request.get("external_api", False))

        # Low risk: read-only, non-sensitive, no external API
        if action == "read" and resource_type not in ("financial", "medical") and not external_api:
            tier = RISK_TIER_LOW

        # Medium risk: workflow operations, limited write, internal only
        elif action in ("start_workflow", "inspect_workflow", "replay") and not external_api:
            tier = RISK_TIER_MEDIUM

        # High risk: write operations, external API, moderate sensitivity
        elif action in ("write_limited", "start_workflow") and (
            external_api or resource_type in ("config", "user_profile")
        ):
            tier = RISK_TIER_HIGH

        # Critical risk: financial, medical, irreversible actions
        elif resource_type in ("financial", "medical") or action in ("commit_change", "irreversible_write"):
            tier = RISK_TIER_CRITICAL

        else:
            # Default to medium if unknown
            tier = RISK_TIER_MEDIUM

        self.logger.info(
            "risk_tier_classified",
            action=action,
            resource_type=resource_type,
            external_api=external_api,
            tier=tier,
        )

        return tier
