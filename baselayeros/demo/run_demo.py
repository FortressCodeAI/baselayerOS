import json
import hmac
import hashlib
import requests # type: ignore
from textwrap import indent

SUBSTRATE_URL = "http://localhost:8000"
SHARED_SECRET = "change-me-in-production"

def print_header(title: str):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72 + "\n")

def sign_identity(identity_json: str) -> str:
    mac = hmac.new(
        SHARED_SECRET.encode("utf-8"),
        identity_json.encode("utf-8"),
        hashlib.sha256,
    )
    return mac.hexdigest()

def pretty(obj):
    return json.dumps(obj, indent=2, sort_keys=True)

def main():
    # ----------------------------------------------------------------------
    print_header("1. Constructing identity")

    identity = {
        "subject": "demo-user",
        "roles": ["analyst"]
    }
    identity_json = json.dumps(identity, separators=(",", ":"), sort_keys=True)
    signature = sign_identity(identity_json)

    print("Identity:")
    print(indent(pretty(identity), "  "))
    print("\nSignature:")
    print(f"  {signature}")

    # ----------------------------------------------------------------------
    print_header("2. Submitting governed action: credit_risk.evaluate")

    payload = {
        "action": "credit_risk.evaluate",
        "payload": {
            "income": 90000,
            "credit_score": 720,
            "existing_debt": 15000
        }
    }

    response = requests.post(
        f"{SUBSTRATE_URL}/execute",
        headers={
            "X-Substrate-Identity": identity_json,
            "X-Substrate-Signature": signature,
            "Content-Type": "application/json",
        },
        data=json.dumps(payload),
    )

    if response.status_code != 200:
        print("Execution failed:")
        print(response.text)
        return

    result = response.json()

    print("Execution Result:")
    print(indent(pretty(result), "  "))

    audit_id = result["audit_id"]

    # ----------------------------------------------------------------------
    print_header("3. Fetching audit envelope")

    audit_response = requests.get(f"{SUBSTRATE_URL}/audit/{audit_id}")

    if audit_response.status_code != 200:
        print("Failed to fetch audit record:")
        print(audit_response.text)
        return

    audit = audit_response.json()

    print("Audit Envelope:")
    print(indent(pretty(audit), "  "))

    # ----------------------------------------------------------------------
    print_header("4. Replay (proving determinism)")

    replay_response = requests.get(f"{SUBSTRATE_URL}/audit/{audit_id}")

    if replay_response.status_code != 200:
        print("Replay failed:")
        print(replay_response.text)
        return

    replay = replay_response.json()

    print("Replay Result (must match original):")
    print(indent(pretty(replay), "  "))

    # ----------------------------------------------------------------------
    print_header("Demo complete")

    print("This is governance infrastructure in action.")
    print("Deterministic. Auditable. Replayable. Enterprise‑grade.\n")


if __name__ == "__main__":
    main()
