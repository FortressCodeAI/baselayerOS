# src/substrate/invariants/postconditions.py

from typing import Any, Dict, List, Callable
from dataclasses import dataclass


PostconditionFn = Callable[[Dict[str, Any], Dict[str, Any], Dict[str, Any]], bool]


@dataclass(frozen=True)
class PostconditionViolation:
    name: str
    message: str
    details: Dict[str, Any]


@dataclass(frozen=True)
class Postcondition:
    name: str
    check_fn: PostconditionFn

    def evaluate(self, prev_state, next_state, result):
        return self.check_fn(prev_state, next_state, result)


class PostconditionSet:
    def __init__(self):
        self._postconditions: List[Postcondition] = []
        self._frozen: bool = False

    def register(self, postcondition: Postcondition):
        if self._frozen:
            raise RuntimeError("PostconditionSet is frozen; no further registrations allowed.")
        self._postconditions.append(postcondition)

    def evaluate_all(self, prev_state, next_state, result):
        violations = []
        for post in self._postconditions:
            if not post.evaluate(prev_state, next_state, result):
                violations.append(
                    PostconditionViolation(
                        name=post.name,
                        message=f"Postcondition '{post.name}' failed.",
                        details={
                            "prev_state": prev_state,
                            "next_state": next_state,
                            "result": result,
                        },
                    )
                )
        return violations

    def freeze(self):
        self._frozen = True

    @property
    def frozen(self) -> bool:
        return self._frozen


postconditions = PostconditionSet()


def _result_keys_must_exist_in_next_state(prev_state, next_state, result):
    for key in result.keys():
        if key not in next_state:
            return False
    return True


postconditions.register(
    Postcondition(
        name="result_keys_must_exist_in_next_state",
        check_fn=_result_keys_must_exist_in_next_state,
    )
)
