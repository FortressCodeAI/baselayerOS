"""
BaseLayerOS Marketplace & Compliance Pack Subscriptions Manager
Manages ARR subscriptions for legal, health, fintech, and council packs.
"""

from typing import Dict


class PackMarketplace:
    CATALOG = {
        "PACK-GOV-ONTARIO-V1": {
            "name": "Ontario Municipal Compliance Pack (EDSTA / MFIPPA)",
            "annual_fee_cad": 15000.00,
            "category": "Government"
        },
        "PACK-HEALTH-PHIPA-V1": {
            "name": "Ontario Healthcare PHI Isolation Pack (PHIPA)",
            "annual_fee_cad": 20000.00,
            "category": "Healthcare"
        },
        "PACK-FIN-FINTRAC-V1": {
            "name": "Fintech Ledger & AML Compliance Pack (FINTRAC)",
            "annual_fee_cad": 25000.00,
            "category": "Finance"
        },
        "TOPOLOGY-COUNCIL-12": {
            "name": "Council of Twelve Voting Matrix & Councilor Zero Veto Engine",
            "annual_fee_cad": 5000.00,
            "category": "Governance"
        }
    }

    def __init__(self, client_id: str):
        self.client_id = client_id
        self.active_subscriptions: Dict[str, dict] = {}

    def subscribe(self, pack_id: str) -> dict:
        if pack_id not in self.CATALOG:
            raise ValueError(f"Pack {pack_id} not found in marketplace catalog.")
            
        pack_info = self.CATALOG[pack_id]
        self.active_subscriptions[pack_id] = {
            "status": "ACTIVE",
            "annual_fee_cad": pack_info["annual_fee_cad"],
            "renews_at": "2027-10-21"
        }
        return {
            "client_id": self.client_id,
            "pack_id": pack_id,
            "name": pack_info["name"],
            "billed_annual_cad": pack_info["annual_fee_cad"],
            "status": "SUBSCRIBED"
        }

    def calculate_total_arr(self) -> float:
        return sum(item["annual_fee_cad"] for item in self.active_subscriptions.values())