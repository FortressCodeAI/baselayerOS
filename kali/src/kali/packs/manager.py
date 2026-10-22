"""
BaseLayerOS Pack Manager
Manages loading, mounting, and execution of compliance and governance packs.
"""

from typing import Dict, Any


class CompliancePackError(Exception):
    pass


class PackManager:
    def __init__(self, license_tier: str = "PRO_SAAS"):
        self.license_tier = license_tier.upper()
        self.mounted_packs: Dict[str, Any] = {}

    def mount_gov_pack(self) -> Any:
        """Dynamically imports and mounts the Ontario Municipal Compliance Pack."""
        try:
            from .gov_municipal import OntarioGovMunicipalPack
        except ImportError:
            # Fallback for relative path execution
            from .gov_municipal import OntarioGovMunicipalPack

        pack = OntarioGovMunicipalPack(license_tier=self.license_tier)
        self.mounted_packs[pack.PACK_ID] = pack
        return pack

    def evaluate_all(self, action_slug: str, raw_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Runs the payload through all mounted compliance packs."""
        all_violations = []
        sanitized_arguments = dict(raw_payload)
        metadata = {"mounted_packs": list(self.mounted_packs.keys()), "sanitized_pii": False}

        for pack_id, pack in self.mounted_packs.items():
            result = pack.evaluate_pre_execution(action_slug, sanitized_arguments)
            if not result["passed"]:
                all_violations.extend(result["violations"])
            sanitized_arguments = result["sanitized_arguments"]
            if result["compliance_metadata"].get("sanitized_pii"):
                metadata["sanitized_pii"] = True

        return {
            "passed": len(all_violations) == 0,
            "violations": all_violations,
            "sanitized_arguments": sanitized_arguments,
            "metadata": metadata
        }