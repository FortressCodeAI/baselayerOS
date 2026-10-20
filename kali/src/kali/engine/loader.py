import importlib.util
from pathlib import Path


def load_operator(path: str):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Operator not found: {path}")

    spec = importlib.util.spec_from_file_location("operator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load operator: {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
