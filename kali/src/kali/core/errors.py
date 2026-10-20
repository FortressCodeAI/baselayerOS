"""
Kali v1.0.0 — Error Types

Explicit, governed error types for:
- envelope issues
- risk classification
- capability violations
- council failures
- HITL enforcement
"""

class KaliError(Exception):
    """Base class for all Kali-specific errors."""
    pass


class EnvelopeError(KaliError):
    """Raised when an envelope is invalid or missing required fields."""
    pass


class RiskClassificationError(KaliError):
    """Raised when risk tier cannot be determined or is inconsistent."""
    pass


class CapabilityViolationError(KaliError):
    """Raised when a requested action exceeds the allowed capability scope."""
    pass


class CouncilError(KaliError):
    """Raised when a council fails, disagrees, or returns an invalid result."""
    pass


class HITLError(KaliError):
    """Raised when HITL is required but not satisfied."""
    pass


class SubstrateError(KaliError):
    """Raised when substrate integration fails or behaves unexpectedly."""
    pass
