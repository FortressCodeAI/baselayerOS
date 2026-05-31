"""
BaseLayerOS Python SDK — Module Interface

This file defines the public interface for building BaseLayerOS modules.
Modules are deterministic units that expose actions, enforce invariants,
and operate under the substrate's execution rules.

This SDK does NOT execute modules — it only defines the structure
developers must follow when implementing them.
"""

from typing import Any, Dict


class BaseLayerModule:
    """
    Base class for all modules running on BaseLayerOS.

    Developers subclass this and implement:
      - invariants()
      - actions()
      - run_action(action_name, payload)

    The runtime handles:
      - deterministic state transitions
      - invariant enforcement
      - audit logging
      - replay
    """

    def invariants(self) -> Dict[str, str]:
        """
        Return a dictionary of invariant names to descriptions.

        Example:
            {
                "non_negative_balance": "Balance must never go below zero"
            }
        """
        raise NotImplementedError(
            "Modules must implement invariants() returning invariant definitions."
        )

    def actions(self) -> Dict[str, str]:
        """
        Return a dictionary of action names to descriptions.

        Example:
            {
                "score": "Compute a risk score",
                "validate": "Validate applicant data"
            }
        """
        raise NotImplementedError(
            "Modules must implement actions() returning action definitions."
        )

    def run_action(self, action_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a module action deterministically.

        Parameters:
            action_name: The action to execute.
            payload: The input payload for the action.

        Returns:
            A dictionary representing the action output.

        The runtime guarantees:
            - deterministic execution
            - pinned versions
            - invariant enforcement
            - audit logging
            - replay fidelity
        """
        raise NotImplementedError(
            f"Module does not implement action '{action_name}'."
        )
