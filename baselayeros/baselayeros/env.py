from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Environment:
    """
    Represents the BaseLayerOS runtime environment.

    This is intentionally minimal in v1.0.0.
    Future versions may include:
    - secrets
    - distributed execution settings
    - tenant isolation
    """

    environment: str
    region: str

    @staticmethod
    def load() -> "Environment":
        """
        Load environment variables with deterministic defaults.
        """

        env = os.getenv("BASELAYER_ENV", "local")
        region = os.getenv("BASELAYER_REGION", "us-east-1")

        return Environment(
            environment=env,
            region=region,
        )
