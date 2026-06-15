from datetime import datetime

class GIULedger:
    def __init__(self):
        self.entries = []

    def record(self, source: str, amount: int, direction: str):
        self.entries.append({
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
            "amount": amount,
            "direction": direction  # "burn" | "credit"
        })
