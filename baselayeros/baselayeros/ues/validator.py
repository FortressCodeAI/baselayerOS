from __future__ import annotations

import json
from jsonschema import Draft202012Validator
from pathlib import Path
from typing import Any, Dict

from schemas.ues.v1_0_0.ues_types import UES
from baselayeros.errors import UESValidationError


class UESValidator:
    """
    Validates UES proposals against the frozen UES schema (v1.0.0).
    Converts validated proposals into typed UES dataclass instances.
    """

    def __init__(self, schema_path: str):
        path = Path(schema_path)
        if not path.exists():
            raise FileNotFoundError(f"UES schema not found at: {schema_path}")

        with path.open("r", encoding="utf-8") as f:
            self.schema = json.load(f)

        self.validator = Draft202012Validator(self.schema)

    def validate(self, proposal: Dict[str, Any]) -> UES:
        """
        Validate a UES proposal dict against the schema.
        Returns a fully typed UES object.
        """

        errors = sorted(self.validator.iter_errors(proposal), key=lambda e: e.path)
        if errors:
            formatted = [
                f"{'/'.join(map(str, err.path))}: {err.message}"
                for err in errors
            ]
            raise UESValidationError("\n".join(formatted))

        try:
            return UES(**proposal)
        except TypeError as e:
            raise UESValidationError(f"Failed to construct UES object: {e}") from e
