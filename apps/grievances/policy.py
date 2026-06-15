from __future__ import annotations
from typing import Any, Dict
from pathlib import Path
import json
import yaml

from .config.settings import settings
from .schemas import Status


def _load_policy_file(name: str) -> Dict[str, Any]:
    json_path = settings.policy_dir / f"{name}.json"
    yaml_path = settings.policy_dir / f"{name}.yaml"
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    if yaml_path.exists():
        with open(yaml_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def check_status_transition(current: Status, target: Status) -> Dict[str, Any]:
    policy = _load_policy_file("status_transitions")
    allowed = policy.get("allowed", {})  # {current: [targets]}
    allowed_targets = allowed.get(current, [])
    if target in allowed_targets:
        return {"decision": "ALLOW", "reason": "Transition allowed by policy"}
    return {
        "decision": "DENY",
        "reason": f"Transition {current} -> {target} not allowed by policy",
    }
