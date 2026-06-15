"""
BaseLayerOS — deterministic execution substrate built on the Universal Execution Schema (UES).
"""

from importlib.metadata import version, PackageNotFoundError

__all__ = ["__version__"]

try:
    __version__ = version("baselayeros")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0"
