import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER_PATH = ROOT / "Demo" / "giu_ledger.json"

def load_ledger():
    if not LEDGER_PATH.exists():
        return {"builder_id": "james", "balance": 10000}
    return json.loads(LEDGER_PATH.read_text())

def save_ledger(data):
    LEDGER_PATH.write_text(json.dumps(data, indent=2))

def burn_gius(builder_id: str, amount: int, dry_run=False):
    ledger = load_ledger()

    if ledger["builder_id"] != builder_id:
        raise ValueError("Unknown builder")

    if not dry_run:
        if ledger["balance"] < amount:
            raise ValueError("Insufficient GIUs")
        ledger["balance"] -= amount
        save_ledger(ledger)

    return ledger["balance"]
