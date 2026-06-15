from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from baselayeros.config import BaseLayerConfig
from baselayeros.errors import UESValidationError


class SchemaLoader:
    """
    Deterministic loader for UES schemas.

    Responsibilities:
    - load schema from configured path
    - validate schema structure
    - provide schema metadata to other subsystems
    """

    def __init__(self, config: BaseLayerConfig | None = None):
        self.config = config or BaseLayerConfig.from_env()
        self.schema_path = Path(self.config.ues_schema_path)
        self.schema = self._load_schema()

    # ---------------------------------------------------------
    # Schema loading
    # ---------------------------------------------------------
    def _load_schema(self) -> Dict[str, Any]:
        if not self.schema_path.exists():
            raise UESValidationError(
                f"UES schema not found at: {self.schema_path}"
            )

        try:
            with self.schema_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            raise UESValidationError(f"Failed to load UES schema: {e}")

        # Minimal structural validation
        if "title" not in data or "type" not in data:
            raise UESValidationError("Invalid UES schema: missing required fields")

        return data

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------
    def get_schema(self) -> Dict[str, Any]:
        """
        Return the loaded schema.
        """
        return self.schema

    def get_version(self) -> str:
        """
        Extract schema version from the file path.
        """
        # Example: schema/ues/v1_0_0/ues.schema.json → v1_0_0
        parts = self.schema_path.parts
        for p in parts:
            if p.startswith("v") and "_" in p:
                return p
        return "unknown"
