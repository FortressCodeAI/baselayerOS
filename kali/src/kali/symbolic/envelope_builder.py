"""
Kali v1.0.0 — Envelope Builder

Every request MUST be wrapped in a deterministic governance envelope.

Envelope structure (v1.0.0):
{
    "envelope_id": str,
    "request": {...},
    "risk_tier": str,
    "capability_scope": str,
    "timestamp": str,
    "kali_standard": str,
}

EnvelopeBuilder MUST:
- generate deterministic envelope IDs
- enforce Kali Standard Level 1 minimum
- attach timestamp
- attach request metadata
"""

from __future__ import annotations
import uuid
import datetime
from typing import Dict, Any

from kali.core.config import KaliConfig
from kali.core.logging import KaliLogger
from kali.core.constants import KALI_STANDARD_LV1
from kali.core.errors import EnvelopeError


class EnvelopeBuilder:
    def __init__(self, config: KaliConfig, logger: KaliLogger):
        self.config = config
        self.logger = logger

    def build(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a deterministic governance envelope.
        """
        if not isinstance(request, dict):
            raise EnvelopeError("Request must be a dictionary.")

        envelope_id = str(uuid.uuid4())
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"

        envelope = {
            "envelope_id": envelope_id,
            "request": request,
            "risk_tier": None,  # assigned later
            "capability_scope": None,  # assigned later
            "timestamp": timestamp,
            "kali_standard": KALI_STANDARD_LV1,
        }

        self.logger.info(
            "envelope_built",
            envelope_id=envelope_id,
            timestamp=timestamp,
            request=request,
        )

        return envelope
