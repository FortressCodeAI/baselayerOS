# src/substrate/credits/pricing.py

from typing import Dict


class PricingTable:
    """
    Deterministic GIU pricing table.

    This is intentionally minimal for open-source:
    - static mapping
    - no dynamic pricing
    - no enterprise overrides
    """

    def __init__(self):
        self._prices: Dict[str, int] = {}

    def set_price(self, action_name: str, version: str, giu_cost: int):
        key = f"{action_name}:{version}"
        if giu_cost < 0:
            raise ValueError("GIU cost must be non-negative.")
        self._prices[key] = giu_cost

    def get_price(self, action_name: str, version: str) -> int:
        key = f"{action_name}:{version}"
        if key not in self._prices:
            raise KeyError(f"No GIU price set for action '{key}'.")
        return self._prices[key]

    def list_prices(self) -> Dict[str, int]:
        return dict(self._prices)


# Global pricing table
pricing = PricingTable()
