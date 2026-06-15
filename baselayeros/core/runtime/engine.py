# baselayeros/core/runtime/engine.py

"""
ExecutionEngine: deterministic single-step execution core for BaseLayerOS.

This is the minimal correct version that:
- integrates with Refusal
- integrates with commit_state
- integrates with AuditChain
- integrates with AuthorityGate
- provides a deterministic run() method
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional

from kali.refusal import Refusal
from kali.commit import commit_state
from kali.audit_chain import AuditChain
from kali.authority_gate import AuthorityGate


@dataclass
class ExecutionResult:
    success: bool
    value: Any | None
    error: Optional[str] = None
    committed: bool = False


class ExecutionEngine:
    """
    Minimal deterministic execution engine.

    Responsibilities:
    - enforce authority gate
    - execute an operation
    - catch Refusal and convert to deterministic result
    - commit state changes
    - write audit events
    """

    def __init__(
        self,
        audit_chain: AuditChain,
        authority: AuthorityGate,
    ) -> None:
        self.audit_chain = audit_chain
        self.authority = authority

    def run(
        self,
        actor: str,
        operation: str,
        fn: Callable[[], Any],
    ) -> ExecutionResult:
        """
        Execute a function deterministically under governance.

        actor:     who is performing the action
        operation: name of the operation (string)
        fn:        zero-arg function that performs the action
        """

        # 1. Authority check
        if not self.authority.allow(actor, operation):
            reason = f"Actor '{actor}' not authorized for '{operation}'"
            self.audit_chain.record_refusal(actor, operation, reason)
            return ExecutionResult(
                success=False,
                value=None,
                error=reason,
                committed=False,
            )

        # 2. Execute the operation
        try:
            result = fn()

        except Refusal as r:
            # Deterministic refusal path
            self.audit_chain.record_refusal(actor, operation, str(r))
            return ExecutionResult(
                success=False,
                value=None,
                error=str(r),
                committed=False,
            )

        except Exception as exc:  # noqa: BLE001
            # Hard failure path
            self.audit_chain.record_error(actor, operation, str(exc))
            return ExecutionResult(
                success=False,
                value=None,
                error=str(exc),
                committed=False,
            )

        # 3. Commit state
        committed = commit_state(result)
        self.audit_chain.record_commit(actor, operation, committed.state)

        return ExecutionResult(
            success=True,
            value=committed.state,
            error=None,
            committed=True,
        )
