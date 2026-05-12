# src/substrate/utils/validation.py

import json
from jsonschema import Draft7Validator # type: ignore
from typing import Any, Dict


class SchemaValidator:
    """
    Deterministic JSON schema validator.
    - no network access
    - no dynamic schema loading
    - stable error ordering
    """

    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema
        self.validator = Draft7Validator(schema)

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate data against the schema.
        Returns the data unchanged if valid.
        Raises ValueError with deterministic error messages if invalid.
        """
        errors = sorted(self.validator.iter_errors(data), key=lambda e: e.path)

        if errors:
            formatted = [
                {
                    "path": list(err.path),
                    "message": err.message,
                }
                for err in errors
            ]
            raise ValueError(f"Schema validation failed: {json.dumps(formatted)}")

        return data
