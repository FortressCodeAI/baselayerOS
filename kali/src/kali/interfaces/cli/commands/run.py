import importlib.util
import json
from pathlib import Path

def run_operator(file: str):
    path = Path(file)
    if not path.exists():
        print(f"❌ File not found: {file}")
        return

    spec = importlib.util.spec_from_file_location("module", file)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {file}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "main"):
        print("❌ Operator must define main()")
        return

    result = module.main()
    print(json.dumps(result, indent=2))
