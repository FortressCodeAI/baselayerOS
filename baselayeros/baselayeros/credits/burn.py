                                                                                                             # src/substrate/credits/burn.py

from typing import Dict, Any

from .ledger import CreditLedger


class CreditBurner:
    """
    Deterministic GIU burn engine.
    - burns credits for each action
    - records events in the ledger
    - no side effects beyond ledger append
    """

    def __init__(self, ledger: CreditLedger):
        self.ledger = ledger

    def burn(self, action_name: str, version: str, amount: int) -> Dict[str, Any]:
        """
        Burn GIU credits deterministically.
        Returns a deterministic receipt.
        """
        if amount < 0:
            raise ValueError("GIU burn amount must be non-negative.")

        key = f"{action_name}:{version}"

        self.ledger.append(key, amount)

        return {
            "action": key,
            "amount": amount,
            "total_burned": self.ledger.total_burned(),
        }


# Global burner + ledger for substrate
ledger = CreditLedger()
burner = CreditBurner(ledger)
                                                                                                                                             