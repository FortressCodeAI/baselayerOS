import json
from pathlib import Path

class Storage:
    def __init__(self, base_path="data"):
        self.base = Path(base_path)
        self.base.mkdir(exist_ok=True)

    def write_json(self, name, payload):
        path = self.base / f"{name}.json"
        with open(path, "w") as f:
            json.dump(payload, f, indent=2)

    def read_json(self, name):
        path = self.base / f"{name}.json"
        if not path.exists():
            return None
        with open(path, "r") as f:
            return json.load(f)
