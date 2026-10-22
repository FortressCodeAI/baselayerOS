# tests/test_gov_pack.py
from kali.src.kali.packs.manager import PackManager

def run_test():
    manager = PackManager(license_tier="PRO_SAAS")
    print(manager.mount_gov_pack())

    # Mock Input Payload with sensitive Ontario PII and an invalid write operation
    test_payload = {
        "citizen_name": "John Doe",
        "phone": "519-555-0199",
        "ohip": "1234-567-890-XX",
        "address": "Waterloo, ON N2L 3G1",
        "is_write_operation": True,
        "financial_commitment_cad": 150.00
    }

    print("\n--- Running Raw Payload Evaluation ---")
    eval_result = manager.evaluate_all(action_slug="db_write_citizen_record", arguments=test_payload)

    print(f"Passed Compliance: {eval_result['passed']}")
    print("Violations Caught:")
    for v in eval_result["violations"]:
        print(f"  ❌ {v}")

    print("\nSanitized Arguments (MFIPPA PII Redacted):")
    print(eval_result["sanitized_arguments"])

if __name__ == "__main__":
    run_test()