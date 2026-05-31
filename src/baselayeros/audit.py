from __future__ import annotations

import json
import os
import hashlib
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable


# ---------- Canonical JSON + hashing ----------

def canonical_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_transcript(transcript: Dict[str, Any]) -> str:
    return sha256_hex(canonical_json(transcript).encode("utf-8"))


# ---------- Signing identity ----------

class SigningIdentity:
    """
    Minimal deterministic signing identity.
    Private key stored at ~/.baselayeros/key
    """

    def __init__(self) -> None:
        home = Path.home() / ".baselayeros"
        home.mkdir(exist_ok=True)
        self.key_path = home / "key"

        if not self.key_path.exists():
            self.key_path.write_bytes(os.urandom(32))

        self._private_key = self.key_path.read_bytes()

    @property
    def key_id(self) -> str:
        return sha256_hex(self._private_key)

    def sign(self, message: str) -> str:
        # Deterministic HMAC-like signature
        return sha256_hex(self._private_key + message.encode("utf-8"))

    def to_dict(self) -> Dict[str, str]:
        return {"key_id": self.key_id}


# ---------- Audit envelope ----------

@dataclass(frozen=True)
class AuditEnvelope:
    # Core identifiers
    id: str
    request_id: str
    action: str

    # Identity
    identity_subject: str
    identity_roles: list[str]

    # Execution
    payload: Dict[str, Any]
    result: Dict[str, Any]
    giu_cost: int

    # State hashes (optional, for stateful runtimes)
    state_hash_before: str | None
    state_hash_after: str | None

    # Time
    created_at: str

    # Cryptographic fields
    transcript_hash: str
    signature: str
    signer: Dict[str, str]

    # Chain-of-custody
    prev_envelope_hash: str | None


class AuditLog:
    """
    Append-only JSONL audit log with cryptographic chaining.
    Each envelope includes:
      - transcript hash
      - signature
      - signer identity
      - previous envelope hash (log chain)
    """

    def __init__(self, log_path: Path) -> None:
        self._path = log_path
        self._path.parent.mkdir(parents=True, exist_ok=True)

    # ----- public API -----

    def append(self, envelope: AuditEnvelope) -> None:
        record = asdict(envelope)
        with self._path.open("a", encoding="utf-8") as f:
            f.write(canonical_json(record))
            f.write("\n")

    def get_by_id(self, audit_id: str) -> AuditEnvelope | None:
        for record in self._iter_records():
            if record.get("id") == audit_id:
                return AuditEnvelope(**record)
        return None

    def verify_chain(self) -> bool:
        """
        Verify that:
          - each record is well-formed
          - prev_envelope_hash matches the hash of the previous record
        """
        prev_hash: str | None = None
        for record in self._iter_records():
            encoded = canonical_json(record).encode("utf-8")
            current_hash = sha256_hex(encoded)

            if record.get("prev_envelope_hash") != prev_hash:
                return False

            prev_hash = current_hash

        return True

    # ----- envelope factory -----

    @staticmethod
    def new_envelope(
        *,
        audit_id: str,
        request_id: str,
        action: str,
        identity_subject: str,
        identity_roles: list[str],
        payload: Dict[str, Any],
        result: Dict[str, Any],
        giu_cost: int,
        state_hash_before: str | None,
        state_hash_after: str | None,
        prev_envelope_hash: str | None,
    ) -> "AuditEnvelope":
        signer = SigningIdentity()

        # Deterministic transcript (what we hash & sign)
        transcript = {
            "id": audit_id,
            "request_id": request_id,
            "action": action,
            "identity_subject": identity_subject,
            "identity_roles": identity_roles,
            "payload": payload,
            "result": result,
            "giu_cost": giu_cost,
            "state_hash_before": state_hash_before,
            "state_hash_after": state_hash_after,
            "prev_envelope_hash": prev_envelope_hash,
        }

        transcript_hash = hash_transcript(transcript)
        signature = signer.sign(transcript_hash)

        return AuditEnvelope(
            id=audit_id,
            request_id=request_id,
            action=action,
            identity_subject=identity_subject,
            identity_roles=identity_roles,
            payload=payload,
            result=result,
            giu_cost=giu_cost,
            state_hash_before=state_hash_before,
            state_hash_after=state_hash_after,
            created_at=datetime.now(timezone.utc).isoformat(),
            transcript_hash=transcript_hash,
            signature=signature,
            signer=signer.to_dict(),
            prev_envelope_hash=prev_envelope_hash,
        )

    # ----- internals -----

    def _iter_records(self) -> Iterable[Dict[str, Any]]:
        if not self._path.exists():
            return []
        with self._path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                yield json.loads(line)
                
# ---------- Convenience API for runtime.server ----------

_AUDIT_LOG_PATH = Path(".baselayeros") / "audit.log"
_AUDIT_LOG = AuditLog(_AUDIT_LOG_PATH)


def _compute_last_envelope_hash() -> str | None:
    """
    Walk the log and return the hash of the last envelope, or None if empty.
    """
    prev_hash: str | None = None
    for record in _AUDIT_LOG._iter_records():
        encoded = canonical_json(record).encode("utf-8")
        prev_hash = sha256_hex(encoded)
    return prev_hash


def write_audit_envelope(
    *,
    action: str,
    payload: Dict[str, Any],
    result: Dict[str, Any],
    identity: Dict[str, Any],
    meta: Dict[str, Any],
) -> str:
    """
    Compatibility wrapper used by baselayeros.runtime.server.

    Creates a new AuditEnvelope, appends it to the chained audit log,
    and returns the audit_id.
    """
    # You can swap this for a deterministic ID scheme if you want.
    # For now, use a hash of (action, payload, result, timestamp).
    transcript_seed = {
        "action": action,
        "payload": payload,
        "result": result,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    audit_id = hash_transcript(transcript_seed)

    request_id = audit_id  # simple 1:1 mapping for now

    identity_subject = identity.get("subject", "unknown")
    identity_roles = list(identity.get("roles", []))

    giu_cost = int(meta.get("giu_burn", 0))

    prev_hash = _compute_last_envelope_hash()

    envelope = AuditLog.new_envelope(
        audit_id=audit_id,
        request_id=request_id,
        action=action,
        identity_subject=identity_subject,
        identity_roles=identity_roles,
        payload=payload,
        result=result,
        giu_cost=giu_cost,
        state_hash_before=None,
        state_hash_after=None,
        prev_envelope_hash=prev_hash,
    )

    _AUDIT_LOG.append(envelope)
    return audit_id

