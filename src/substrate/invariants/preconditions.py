# src/substrate/invariants/preconditions.py

from typing import Any, Dict, List, Callable
from dataclasses import dataclass


PreconditionFn = Callable[[Dict[str, Any], Dict[str, Any]], bool]


@dataclass(frozen=True)
class PreconditionViolation:
    name: str
    message: str
    details: Dict[str, Any]


@dataclass(frozen=True)
class Precondition:
    name: str
    check_fn: PreconditionFn

    def evaluate(self, params: Dict[str, Any], state: Dict[str, Any]) -> bool:
        return self.check_fn(params, state)


class PreconditionSet:
    def __init__(self):
        self._preconditions: List[Precondition] = []
        self._frozen: bool = False

    def register(self, precondition: Precondition):
        if self._frozen:
            raise RuntimeError("PreconditionSet is frozen; no further registrations allowed.")
        self._preconditions.append(precondition)

    def evaluate_all(self, params, state):
        violations = []
        for pre in self._preconditions:
            if not pre.evaluate(params, state):
                violations.append(
                    PreconditionViolation(
                        name=pre.name,
                        message=f"Precondition '{pre.name}' failed.",
                        details={"params": params, "state": state},
                    )
                )
        return violations

    def freeze(self):
        self._frozen = True

    @property
    def frozen(self) -> bool:
        return self._frozen


preconditions = PreconditionSet()


def _params_must_be_object(params, state):
    return isinstance(params, dict)


preconditions.register(
    Precondition(
        name="params_must_be_object",
        check_fn=_params_must_be_object,
    )
)
