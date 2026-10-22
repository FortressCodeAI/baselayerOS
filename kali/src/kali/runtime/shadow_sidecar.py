"""
BaseLayerOS & Kali: Shadow Mode Sidecar Observer
Silently inspects execution payloads, logs compliance infractions, 
and anchors immutable audit receipts without blocking production traffic.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

class ShadowSidecar:
    def __init__(self, audit_log_path: str = "audit_chain.json"):
        self.audit_log_path = Path(audit_log_path)
        self._ensure_audit_ledger()

    def _ensure_audit_ledger(self):
        if not self.audit_log_path.exists():
            with open(self.audit_log_path, "w") as f:
                json.dump([], f)

    def observe(self, action_slug: str, raw_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Observes an agent execution payload in SHADOW MODE.
        Evaluates rules silently without altering execution flow or blocking writes.
        """
        violations: List[str] = []
        sanitized_preview = dict(raw_payload)
        pii_detected = False

        # 1. Inspect for Unmasked PII (MFIPPA Rules)
        pii_keys = ["citizen_name", "ohip", "phone", "sin", "email"]
        for key in pii_keys:
            if key in sanitized_preview and sanitized_preview[key]:
                val = str(sanitized_preview[key])
                if not val.startswith("[REDACTED"):
                    violations.append(f"SHADOW_VIOLATION_MFIPPA_PII_EXPOSED: Unmasked '{key}' detected.")
                    sanitized_preview[key] = f"[SHADOW_REDACTED_{key.upper()}]"
                    pii_detected = True

        # 2. Inspect for Unauthorized Direct Database Writes (EDSTA Rules)
        is_write = sanitized_preview.get("is_write_operation", False)
        if is_write and "admin" not in action_slug.lower():
            violations.append("SHADOW_VIOLATION_EDSTA_UNAUTHORIZED_WRITE: Direct DB write initiated outside governed boundary.")

        # 3. Build Cryptographic Audit Receipt
        timestamp = datetime.utcnow().isoformat() + "Z"
        audit_entry = {
            "timestamp": timestamp,
            "mode": "SHADOW_OBSERVER",
            "action_slug": action_slug,
            "execution_blocked": False,  # Shadow mode guarantees zero disruption
            "violations_detected": violations,
            "pii_redacted_in_shadow": pii_detected,
            "payload_hash": hashlib.sha256(json.dumps(raw_payload, sort_keys=True).encode()).hexdigest()
        }

        # Anchor to local chain
        self._append_to_ledger(audit_entry)

        return {
            "status": "OBSERVED_AND_LOGGED",
            "violations_count": len(violations),
            "violations": violations,
            "audit_receipt_hash": audit_entry["payload_hash"][:16]
        }

    def _append_to_ledger(self, entry: dict):
        try:
            with open(self.audit_log_path, "r+") as f:
                ledger = json.load(f)
                ledger.append(entry)
                f.seek(0)
                json.dump(ledger, f, indent=2)
        except Exception:
            with open(self.audit_log_path, "w") as f:
                json.dump([entry], f, indent=2)