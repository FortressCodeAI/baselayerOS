import json
from pathlib import Path

AUDIT_LOG = Path.home() / ".kali_audit.jsonl"


def record_audit(action: str, input_data: dict, output_data: dict):
    entry = {
        "action": action,
        "input": input_data,
        "output": output_data,
    }
    with AUDIT_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")
