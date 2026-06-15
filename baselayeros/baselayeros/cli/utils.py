import json
from pathlib import Path
from baselayeros.cli.exceptions import CLIError


def load_json(path: Path):
    if not path.exists():
        raise CLIError(f"File not found: {path}")
    try:
        return json.loads(path.read_text())
    except Exception as e:
        raise CLIError(f"Invalid JSON in {path}: {e}")
