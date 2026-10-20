# __init__.py at repo root (C:\baselayeros\kali\__init__.py)

"""
Kali — governed operator runtime for BaseLayerOS.

Public surface:
- core: configuration, state, logging, errors
- operators: operator-facing execution layer
- neural: neural execution layer
- symbolic: symbolic reasoning layer
- councils: governance councils
- substrate: substrate integration
"""

from .src import core
from .src import operators
from .src import neural
from .src import symbolic
from .src import councils
from .src import substrate

__all__ = [
    "core",
    "operators",
    "neural",
    "symbolic",
    "councils",
    "substrate",
]
