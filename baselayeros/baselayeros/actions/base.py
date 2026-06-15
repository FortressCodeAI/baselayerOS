from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class ActionMetadata:
    name: str
    giu_cost: int = 1
    description: str = ""


class ExecutionContext:

    def __init__(self, user: str, params: Dict[str, Any]):
        self.user = user
        self.params = params

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user": self.user,
            "params": self.params,
        }


class BaseAction(ABC):

    metadata: ActionMetadata

    @classmethod
    def name(cls) -> str:
        return cls.metadata.name

    @abstractmethod
    def validate(self, ctx: ExecutionContext) -> None:
        raise NotImplementedError

    @abstractmethod
    def execute(self, ctx: ExecutionContext) -> Dict[str, Any]:
        raise NotImplementedError
