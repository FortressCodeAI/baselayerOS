from __future__ import annotations

from schema.ues.v1_0_0.ues_types import UES
from baselayeros.capabilities.registry import CapabilityRegistry


class RoutingEngine:
    """
    Domain-level routing for BaseLayerOS.

    Responsibilities:
    - determine which capabilities are required
    - ensure all capabilities exist in the registry
    - provide lookup for executor
    """

    def __init__(self):
        self.registry = CapabilityRegistry()

    def validate_capabilities(self, ues: UES) -> None:
        """
        Ensure all capabilities referenced in the UES exist.
        """

        for cap in ues.capabilities:
            if not self.registry.exists(cap.id):
                raise ValueError(f"Unknown capability: {cap.id}")

    def get(self, capability_id: str):
        """
        Retrieve a capability implementation.
        """
        return self.registry.get(capability_id)
