"""
Schema integration layer for BaseLayerOS.

Provides:
- SchemaLoader: deterministic loader for UES schemas
"""

from .loader import SchemaLoader

__all__ = [
    "SchemaLoader",
]
