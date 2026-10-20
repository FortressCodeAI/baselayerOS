"""
Kali v1.0.0 — Request Operator

This operator is responsible for:
- validating incoming requests
- normalizing request structure
- ensuring required fields exist
- preparing request for GovernanceOperator

This is the "front door" of Kali.
"""

from __future__ import annotations
from typing import Dict, Any

from kali.core.logging import KaliLogger
from kali.core.errors import EnvelopeError


class RequestOperator:
    def __init__(self, logger: KaliLogger):
        self.logger = logger

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize incoming request into Kali's expected structure.
        """

        if not isinstance(raw, dict):
            raise EnvelopeError("Request must be a dictionary.")

        # Required fields for v1.0.0
        required = ["action"]
        missing = [f for f in required if f not in raw]

        if missing:
            raise EnvelopeError(f"Missing required request fields: {missing}")

        normalized = {
            "action": raw.get("action"),
            "resource_type": raw.get("resource_type", "data"),
            "external_api": raw.get("external_api", False),
            "capability_scope": raw.get("capability_scope", "read_only"),
            "prompt": raw.get("prompt", ""),
            "description": raw.get("description", ""),
        }

        self.logger.info("request_normalized", request=normalized)
        return normalized
