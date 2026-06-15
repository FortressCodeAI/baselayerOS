class BaseLayerError(Exception):
    """
    Base class for all deterministic substrate errors.
    """
    pass


# ---------------------------------------------------------
# UES / Validation Errors
# ---------------------------------------------------------
class UESValidationError(BaseLayerError):
    """
    Raised when a UES proposal fails schema or council validation.
    """
    pass


class StateTransitionError(BaseLayerError):
    """
    Raised when an invalid UES lifecycle transition is attempted.
    """
    pass


# ---------------------------------------------------------
# Audit Errors
# ---------------------------------------------------------
class AuditError(BaseLayerError):
    """
    Raised when audit chain integrity is violated.
    """
    pass


# ---------------------------------------------------------
# Compilation Errors
# ---------------------------------------------------------
class CompilationError(BaseLayerError):
    """
    Raised when the compiler fails preconditions or code generation.
    """
    pass


# ---------------------------------------------------------
# Execution Errors
# ---------------------------------------------------------
class ExecutionError(BaseLayerError):
    """
    Raised when a capability fails or a postcondition is violated.
    """
    pass
