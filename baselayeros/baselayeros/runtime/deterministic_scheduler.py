# baselayeros/runtime/scheduler.py

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from copy import deepcopy
import hashlib
import json


@dataclass
class ScheduledTask:
    id: str
    fn: Callable[[Dict[str, Any]], Dict[str, Any]]
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


class DeterministicScheduler:

    def __init__(self) -> None:
        self._queue: List[ScheduledTask] = []
        self._log: List[Dict[str, Any]] = []
        self._logical_clock: int = 0
        self._last_hash: str = "0" * 64 

    def enqueue(self, task: ScheduledTask) -> None:
        self._queue.append(task)

    def run_next(self) -> Optional[Dict[str, Any]]:
    

        if not self._queue:
            return None

        task = self._queue.pop(0)
        self._logical_clock += 1

        # Execute task with deep-copied payload
        result = task.fn(deepcopy(task.payload))

        entry = {
            "task_id": task.id,
            "payload": deepcopy(task.payload),
            "metadata": deepcopy(task.metadata),
            "result": deepcopy(result),
            "logical_clock": self._logical_clock,
            "prev_hash": self._last_hash,
        }

        # Compute deterministic hash
        entry_hash = self._compute_hash(entry)
        entry["_entry_hash"] = entry_hash

        # Commit to log
        self._log.append(entry)
        self._last_hash = entry_hash

        return deepcopy(entry)

    def run_all(self) -> List[Dict[str, Any]]:
        """Run all queued tasks deterministically."""
        results = []
        while self._queue:
            results.append(self.run_next())
        return results

    def get_log(self) -> List[Dict[str, Any]]:
        """Return a deep copy of the schedule log."""
        return deepcopy(self._log)

    def replay(
        self,
        handler: Callable[[Dict[str, Any]], None],
    ) -> None:
        for entry in self._log:
            handler(deepcopy(entry))


    def _compute_hash(self, entry: Dict[str, Any]) -> str:
        serialized = json.dumps(entry, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
