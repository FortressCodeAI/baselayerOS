"""
Kali Shadow Mode Demo Runner
Executes a simulated 3-step agent workflow through the ShadowSidecar 
to demonstrate live telemetry and infraction logging for tomorrow's meeting.
"""
import sys
from pathlib import Path

# Add src to path for package resolution
SRC_DIR = Path(r"C:\baselayeros\kali\src")
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kali.src.kali.runtime.shadow_sidecar import ShadowSidecar  # noqa: E402


def main():
    print("==========================================================================")
    print("       KALI GOVERNANCE SUBSTRATE — SHADOW MODE SIDECAR DEMO             ")
    print("==========================================================================")
    print("Status: Silent Observer Active. Zero Production Disruption Mode.\n")

    sidecar = ShadowSidecar(audit_log_path="audit_chain.json")

    transactions = [
        {
            "action": "fetch_public_transit_schedule",
            "payload": {"route_id": "WATERLOO_LRT_01", "is_write_operation": False}
        },
        {
            "action": "update_citizen_tax_record",
            "payload": {
                "citizen_name": "Arthur Pendelton",
                "ohip": "4892-102-391-XX",
                "phone": "519-886-5000",
                "is_write_operation": True
            }
        },
        {
            "action": "log_municipal_inquiry",
            "payload": {"citizen_email": "resident@waterloo.ca", "is_write_operation": False}
        }
    ]

    for idx, tx in enumerate(transactions, 1):
        print(f"--- Transaction {idx}: {tx['action']} ---")
        result = sidecar.observe(tx["action"], tx["payload"])
        
        print("  Execution State:  PASSED (Silently Allowed)")
        print(f"  Infractions Found: {result['violations_count']}")
        if result["violations"]:
            for v in result["violations"]:
                print(f"    ⚠️  [SHADOW FLAG] {v}")
        print(f"  Audit Hash Anchor: {result['audit_receipt_hash']}...")
        print()

    print("==========================================================================")
    print("✨ Shadow trace complete. Audit trail successfully anchored to audit_chain.json")
    print("==========================================================================")


if __name__ == "__main__":
    main()