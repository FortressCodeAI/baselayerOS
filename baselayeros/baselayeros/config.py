from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BaseLayerConfig:
    """
    Deterministic configuration surface for BaseLayerOS.

    All configuration is derived from environment variables with strict defaults.
    No dynamic or runtime mutation is allowed.
    """

    ues_schema_path: str
    log_level: str

    @staticmethod
    def from_env() -> "BaseLayerConfig":
        """
        Load configuration from environment variables with deterministic defaults.
        """

        schema_path = os.getenv(
            "BASELAYER_UES_SCHEMA",
            "schema/ues/v1_0_0/ues.schema.json",
        )

        log_level = os.getenv("BASELAYER_LOG_LEVEL", "INFO").upper()

        # Validate schema path exists
        if not Path(schema_path).exists():
            raise FileNotFoundError(
                f"UES schema not found at configured path: {schema_path}"
            )

        return BaseLayerConfig(
            ues_schema_path=schema_path,
            log_level=log_level,
        )
