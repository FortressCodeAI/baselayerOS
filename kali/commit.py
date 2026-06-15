# baselayeros/kali/commit.py

"""
Deterministic state commit primitive.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CommitResult:
    state: Any
    committed: bool = True


def commit_state(state: Any) -> CommitResult:
    """
    Deterministically wrap a state object as a committed result.
    """
    return CommitResult(state=state)
