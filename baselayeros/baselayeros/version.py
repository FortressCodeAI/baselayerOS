"""
BaseLayerOS versioning module.

The version is deterministic and manually incremented for each release.
"""

__version__ = "1.0.0"


def get_version() -> str:
    """
    Return the BaseLayerOS version string.
    """
    return __version__
