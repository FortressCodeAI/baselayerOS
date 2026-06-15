from __future__ import annotations

import os
from typing import Dict, Any


class Module:
    """
    Minimal module wrapper.
    In the future this can load YAML manifests, Python modules, workflows, etc.
    """

    def __init__(self, module_id: str, path: str):
        self.module_id = module_id
        self.path = path

    def to_request(self) -> Dict[str, Any]:
        """
        Convert this module into a substrate execution request.
        For now, this is a stub.
        """
        return {
            "action": "echo",
            "payload": {"module": self.module_id},
            "subject_id": "system",
            "roles": ["system"],
            "state": {},
            "request_id": f"module-{self.module_id}",
        }


class ModuleRegistry:
    """
    Discovers and loads modules from a directory.
    """

    def __init__(self, modules_root: str = "modules"):
        self.modules_root = modules_root
        self.modules: Dict[str, Module] = {}

    def load_all(self) -> None:
        """
        Load all modules from the modules_root directory.
        """
        if not os.path.isdir(self.modules_root):
            return

        for entry in os.listdir(self.modules_root):
            module_path = os.path.join(self.modules_root, entry)
            if os.path.isdir(module_path):
                self.modules[entry] = Module(entry, module_path)

    def get(self, module_id: str) -> Module:
        if module_id not in self.modules:
            raise KeyError(f"Module '{module_id}' not found.")
        return self.modules[module_id]
