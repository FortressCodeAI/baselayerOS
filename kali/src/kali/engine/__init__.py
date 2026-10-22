import json
from ..core.envelope import ExecutionEnvelope
from ..runtime.baselayer_bridge import BaseLayerOSBridge
"""
Kali Engine Package
"""

class KaliVetoError(Exception):
    """Raised when a governance policy vetoes or blocks an execution."""
    pass
class KaliEngine:
    def __init__(self, mode: str = "shadow", log_path: str = "./src/kali/audit/audit_chain.json"):
        self.mode = mode.lower()
        self.log_path = log_path
        self.baselayer_bridge = BaseLayerOSBridge()

    def process_plan_and_execute(self, plan_id: str, action_slug: str, action_args: dict) -> dict:
        print(f"🧠 [Kali] Planning & governance verification for plan '{plan_id}'...")

        # 1. Create Envelope for BaseLayerOS
        envelope = ExecutionEnvelope(
            plan_id=plan_id,
            action_slug=action_slug,
            arguments=action_args,
            mode=self.mode
        )

        print(f"📦 [Kali] Created execution envelope {envelope.envelope_id}. Handing over to BaseLayerOS Substrate...")

        # 2. Hand Off Execution to BaseLayerOS
        execution_response = self.baselayer_bridge.execute_envelope(envelope)

        # 3. Log Audit Trace Back to Kali Ledger
        self._write_audit_chain(execution_response["audit_trace"])

        print(f"✅ [Kali] Execution complete. Audit trace logged to {self.log_path}.")

        return {
            "status": "SUCCESS",
            "execution_result": execution_response["result"],
            "audit_trace": execution_response["audit_trace"]
        }

    def _write_audit_chain(self, audit_trace: dict):
        """Appends audit trace to persistent JSON ledger."""
        try:
            with open(self.log_path, "r") as f:
                chain = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            chain = []

        chain.append(audit_trace)

        with open(self.log_path, "w") as f:
            json.dump(chain, f, indent=2)