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

from ..kali import core
from ..kali import operators
from ..kali import neural
from ..kali import symbolic
from ..kali import councils
from ..kali import substrate

__all__ = [
    "core",
    "operators",
    "neural",
    "symbolic",
    "councils",
    "substrate",
]
