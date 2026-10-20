import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List

from kali.governance.engine import GovernanceEngine
from kali.runtime.engine import RuntimeEngine
from kali.core.proofs.engine import ProofEngine
from kali.audit.ledger import AuditLedger


class KaliVetoError(Exception):
    """Raised when Councilor Zero or active departments veto an action in Enforce mode."""
    pass


class KaliRuntime:
    """
    Manages runtime execution modes (shadow vs. enforce), active council 
    deliberations (including Councilor Zero), and audit trace logging.
    """
    def __init__(self, mode: str = "shadow", log_path: str = "./audit_trace.jsonl"):
        self.mode = mode.lower()  # "shadow" or "enforce"
        self.log_path = log_path

    def evaluate_councils(self, execution) -> List[Dict[str, Any]]:
        """
        Executes active multi-department council deliberation and Councilor Zero validation.
        """
        verdicts = []
        action_slug = getattr(execution, "action_slug", str(execution))
        arguments = getattr(execution, "arguments", {})

        # 1. Security Department
        if "eval" in str(arguments) or "exec" in str(arguments):
            verdicts.append({"department": "Security Department", "passed": False, "reason": "Dynamic code execution pattern detected."})
        else:
            verdicts.append({"department": "Security Department", "passed": True, "reason": "Payload verified."})

        # 2. Finance / Resource Department
        if action_slug == "transfer_funds" and arguments.get("amount", 0) > 10000:
            verdicts.append({"department": "Finance Council", "passed": False, "reason": "Transaction exceeds autonomous limit."})
        else:
            verdicts.append({"department": "Finance Council", "passed": True, "reason": "Within financial thresholds."})

        # 3. Councilor Zero (Adversarial Red-Team Veto)
        dangerous_tools = ["drop_database", "rm_rf", "exfiltrate_data", "bypass_kernel"]
        if action_slug in dangerous_tools:
            verdicts.append({"department": "Councilor Zero", "passed": False, "reason": f"Critical invariant breach on '{action_slug}'. Absolute veto."})
        else:
            verdicts.append({"department": "Councilor Zero", "passed": True, "reason": "No adversarial vectors identified."})

        return verdicts


class KaliEngine:
    def __init__(self, mode: str = "shadow", log_path: str = "./audit_trace.jsonl"):
        self.runtime_env = KaliRuntime(mode=mode, log_path=log_path)
        self.governance = GovernanceEngine()
        self.runtime = RuntimeEngine()
        self.audit = AuditLedger()

    def execute(self, execution):
        # 1. Evaluate baseline governance & active multi-department councils
        gov_decision = self.governance.evaluate(execution)
        council_verdicts = self.runtime_env.evaluate_councils(execution)
        
        failed_council = next((v for v in council_verdicts if not v["passed"]), None)
        gov_allowed = gov_decision.get("allowed", True)
        councils_passed = failed_council is None
        
        is_allowed = gov_allowed and councils_passed
        
        timestamp = datetime.now(timezone.utc).isoformat()
        execution_id = getattr(execution, "execution_id", "unknown")
        action_slug = getattr(execution, "action_slug", "unknown")

        # 2. Determine status based on runtime mode (shadow vs enforce)
        if is_allowed:
            status, action_taken = "PASSED", "allowed"
        elif self.runtime_env.mode == "shadow":
            status, action_taken = "VIOLATION_DETECTED", "shadow_allowed"
        else:
            status, action_taken = "VIOLATION_BLOCKED", "vetoed_by_councilor_zero"

        # 3. Record audit trail entry
        log_entry = {
            "timestamp": timestamp,
            "execution_id": execution_id,
            "action": action_slug,
            "policy_status": status,
            "mode": self.runtime_env.mode,
            "action_taken": action_taken,
            "reason": failed_council["reason"] if failed_council else gov_decision.get("reason", "All invariants satisfied"),
            "councils": council_verdicts
        }
        self._write_audit_log(log_entry)

        # 4. Enforce Mode Veto Handling
        if status == "VIOLATION_BLOCKED":
            reason = failed_council["reason"] if failed_council else "Governance policy violation"
            raise KaliVetoError(f"🛡️ KERNEL VETO: {reason}")

        # 5. Execute underlying runtime action
        result = self.runtime.execute(execution)

        execution_hash = ProofEngine.execution_hash(execution, result)
        audit_hash = self.audit.record({
            "execution_id": execution_id,
            "action": action_slug,
            "mode": self.runtime_env.mode,
            "governance_passed": is_allowed,
            "hash": execution_hash
        })

        return {
            "status": "executed" if is_allowed else "shadow_executed",
            "mode": self.runtime_env.mode,
            "execution_id": execution_id,
            "result": result,
            "decision": {
                "allowed": is_allowed,
                "governance": gov_decision,
                "councils": council_verdicts
            },
            "proofs": {
                "execution_hash": execution_hash,
                "audit_hash": audit_hash
            }
        }

    def _write_audit_log(self, entry: Dict[str, Any]):
        os.makedirs(os.path.dirname(os.path.abspath(self.runtime_env.log_path)), exist_ok=True)
        with open(self.runtime_env.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")