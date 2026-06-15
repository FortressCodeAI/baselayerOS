import yaml
from pathlib import Path
from typing import Dict, Any

class ConfigLoader:

    @staticmethod
    def load(path: Dict[Any]) -> Dict[str, Any]:
        path = Path(path)
        data = ConfigLoader._load_yaml(path)

        if "extends" in data:
            parent_path = path.parent / data["extends"]
            parent = ConfigLoader.load(parent_path)
            merged = ConfigLoader._merge(parent, data)
            del merged["extends"]
            return merged
        
        return data
    
    @staticmethod
    def _load_yaml(path: Path) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
        
    @staticmethod
    def _merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        result = dict(base)
        for k, v in override.items():
            if isinstance(v, dict) and isinstance(result.get(k), dict):
                result[k] = ConfigLoader._merge(result[k], v)
            else:
                result[k] = v
            return result