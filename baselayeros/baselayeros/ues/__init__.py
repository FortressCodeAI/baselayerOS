"""
UES (Universal Execution Schema) runtime utilities.

This package provides:
- loading UES proposals from dict/JSON
- validating proposals against the frozen UES schema
- converting proposals into typed Python objects
- enforcing deterministic behavior at the substrate boundary
"""

from .loader import load_ues
from .validator import UESValidator

__all__ = [
    "load_ues",
    "UESValidator",
]
