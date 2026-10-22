import hashlib

class LicenseError(Exception):
    pass


class LicenseManager:
    TIER_LIMITS = {
        "COMMUNITY": {"max_nodes": 1, "packs_allowed": [], "giu_rate_cad": 0.0},
        "PRO_SAAS": {"max_nodes": 5, "packs_allowed": ["PACK-GOV-ONTARIO-V1"], "giu_rate_cad": 0.25},
        "ENTERPRISE_OEM": {"max_nodes": 999, "packs_allowed": ["*"], "giu_rate_cad": 0.25}
    }

    def __init__(self, license_key: str, client_id: str, tier: str = "PRO_SAAS"):
        self.license_key = license_key
        self.client_id = client_id
        self.tier = tier.upper()
        
        if self.tier not in self.TIER_LIMITS:
            raise LicenseError(f"Invalid licensing tier: {self.tier}")
            
        self._verify_key()

    def _verify_key(self):
        """Simulates asymmetric verification of license signature against client ID."""
        expected_hash = hashlib.sha256(f"{self.client_id}:{self.tier}:SECRET_BASELAYER_2026".encode()).hexdigest()
        if self.license_key != f"LIC-{expected_hash}":
            raise LicenseError("Invalid license key format or signature tampered.")

    def can_mount_pack(self, pack_id: str) -> bool:
        allowed = self.TIER_LIMITS[self.tier]["packs_allowed"]
        return "*" in allowed or pack_id in allowed