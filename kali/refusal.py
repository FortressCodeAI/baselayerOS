# baselayeros/kali/refusal.py

from dataclasses import dataclass
from typing import Optional

from kali.events import build_refusal_event

@dataclass(frozen=True)
class Refusal(Exception):
    """
    A refusal event raised intentionally by the substrate or a module.

    Attributes:
        reason: Human‑readable explanation of why the action was refused.
        code: Optional machine‑readable refusal code.
    """
    reason: str
    code: Optional[str] = None

    def __str__(self) -> str:
        if self.code:
            return f"[{self.code}] {self.reason}"
        return self.reason


def refuse(reason: str, code: Optional[str] = None) -> None:
    """
    Deterministically raise a refusal event.

    This is the canonical way for any part of the substrate,
    module, or authority gate to halt execution safely.

    Example:
        refuse("Human approval required", code="HUMAN_APPROVAL")
    """
    raise Refusal(reason=reason, code=code)

def deterministic_refusal(node, input_payload, input_hash):
    """
    Deterministic refusal wrapper.

    Delegates to the canonical event builder in events.py.
    """
    return build_refusal_event(node, input_payload, input_hash)