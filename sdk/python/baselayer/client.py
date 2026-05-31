"""
BaseLayerOS Python SDK — Client

This client provides a minimal interface for interacting with
BaseLayerOS‑conformant runtimes. It does NOT implement deterministic
execution — that is the responsibility of enterprise runtimes.

This client is intentionally lightweight and public‑safe.
"""

from typing import Any, Dict, Optional


class BaseLayerClient:
    """
    Minimal client for submitting workflows and modules to a conformant runtime.

    This class is intentionally simple. Enterprise runtimes may expose
    additional capabilities, but the public SDK defines only the stable,
    standard interface surface.
    """

    def __init__(self, endpoint: str):
        self.endpoint = endpoint.rstrip("/")

    def run_workflow(self, workflow_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submit a workflow execution request.

        Parameters:
            workflow_id: The workflow identifier.
            payload: The workflow input payload.

        Returns:
            A dictionary containing:
                - output: workflow output
                - trace_id: replay trace identifier
                - audit_events: optional audit metadata
        """
        # NOTE: This is a placeholder for integrators.
        # Actual HTTP calls are runtime‑specific and not part of the public standard.
        raise NotImplementedError(
            "BaseLayerClient.run_workflow must be implemented by a conformant runtime client."
        )

    def get_trace(self, trace_id: str) -> Dict[str, Any]:
        """
        Retrieve a replay trace from the runtime.

        Parameters:
            trace_id: The trace identifier.

        Returns:
            A dictionary representing the replay trace.
        """
        raise NotImplementedError(
            "BaseLayerClient.get_trace must be implemented by a conformant runtime client."
        )

    def get_audit_log(self, workflow_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve audit log entries.

        Parameters:
            workflow_id: Optional workflow filter.

        Returns:
            A dictionary or list of audit events.
        """
        raise NotImplementedError(
            "BaseLayerClient.get_audit_log must be implemented by a conformant runtime client."
        )
