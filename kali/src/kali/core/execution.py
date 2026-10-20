from dataclasses import dataclass
from typing import Dict, Any
import uuid


@dataclass
class Execution:

    execution_id: str
    execution_type: str
    action_slug: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any]

    @classmethod
    def create(
        cls,
        execution_type,
        action_slug,
        payload,
        metadata=None
    ):
        return cls(
            execution_id=str(uuid.uuid4()),
            execution_type=execution_type,
            action_slug=action_slug,
            payload=payload,
            metadata=metadata or {}
        )