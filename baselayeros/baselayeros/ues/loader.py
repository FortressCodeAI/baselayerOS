from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Union

from .validator import UESValidator
from schemas.ues.v1_0_0.ues_types import UES
from baselayeros.config import BaseLayerConfig
from baselayeros.errors import UESValidationError


def load_ues(source: Union[str, Dict[str, Any], Path]) -> UES:
    """
    Load and validate a UES proposal from:
    - a Python dict
    - a JSON string
    - a filesystem path to a JSON file

    Returns a fully typed UES object.
    """

    config = BaseLayerConfig.from_env()
    validator = UESValidator(config.ues_schema_path)

    # Case 1: dict
    if isinstance(source, dict):
        return validator.validate(source)

    # Case 2: JSON string
    if isinstance(source, str) and source.strip().startswith("{"):
        try:
            data = json.loads(source)
        except json.JSONDecodeError as e:
            raise UESValidationError(f"Invalid JSON string: {e}") from e
        return validator.validate(data)

    # Case 3: file path
    path = Path(source)
    if not path.exists():
        raise UESValidationError(f"UES file not found: {path}")

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise UESValidationError(f"Failed to read UES file: {e}") from e

    return validator.validate(data)
