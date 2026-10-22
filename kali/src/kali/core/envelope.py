# src/kali/core/envelope.py
import json
import time
import hashlib

class ExecutionEnvelope:
    def __init__(self, plan_id: str, action_slug: str, arguments: dict, mode: str = "shadow", giu_budget: int = 10):
        self.envelope_id = f"env_{int(time.time()*1000)}"
        self.plan_id = plan_id
        self.action_slug = action_slug
        self.arguments = arguments
        self.mode = mode
        self.giu_budget = giu_budget
        self.timestamp = time.time()
        self.signature = self._generate_signature()

    def _generate_signature(self) -> str:
        """Generates cryptographic hash of envelope contents to prevent tampering."""
        raw_payload = f"{self.envelope_id}:{self.plan_id}:{self.action_slug}:{json.dumps(self.arguments, sort_keys=True)}"
        return hashlib.sha256(raw_payload.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "envelope_id": self.envelope_id,
            "plan_id": self.plan_id,
            "action_slug": self.action_slug,
            "arguments": self.arguments,
            "mode": self.mode,
            "giu_budget": self.giu_budget,
            "timestamp": self.timestamp,
            "signature": self.signature
        }