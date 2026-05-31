from __future__ import annotations

import importlib
import pkgutil
from typing import Callable, Dict

# Global registry
_ACTION_REGISTRY: Dict[str, Callable] = {}
_LOADED = False


def register_action(action_id: str, fn: Callable):
    _ACTION_REGISTRY[action_id] = fn


def get_action_registry() -> Dict[str, Callable]:
    return _ACTION_REGISTRY


def load_all_modules() -> Dict[str, Callable]:
    """
    Auto-imports baselayeros.modules.* and lets them call register_action().
    """
    global _LOADED
    if _LOADED:
        return _ACTION_REGISTRY

    import baselayeros.modules as modules_pkg

    for mod in pkgutil.iter_modules(modules_pkg.__path__, modules_pkg.__name__ + "."):
        importlib.import_module(mod.name)

    _LOADED = True
    return _ACTION_REGISTRY


def load_all_packs() -> Dict[str, Callable]:
    """
    Same idea for packs; packs can also call register_action().
    """
    import baselayeros.packs as packs_pkg

    for mod in pkgutil.iter_modules(packs_pkg.__path__, packs_pkg.__name__ + "."):
        importlib.import_module(mod.name)

    return _ACTION_REGISTRY
