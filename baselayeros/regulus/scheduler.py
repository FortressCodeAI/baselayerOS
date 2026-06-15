# baselayeros/regulus/scheduler.py

from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List

from baselayeros.regulus.interface import RegulusInterface


@dataclass
class ScheduledJob:
    name: str
    operation: str
    context: Dict[str, Any]
    fn: Callable[[], Any]


@dataclass
class RegulusScheduler:
    """
    Minimal deterministic scheduler that runs jobs through Regulus.
    No real time-based scheduling; you call run_all() explicitly.
    """

    regulus: RegulusInterface
    jobs: List[ScheduledJob] = field(default_factory=list)

    def add_job(
        self,
        name: str,
        operation: str,
        context: Dict[str, Any],
        fn: Callable[[], Any],
    ) -> None:
        self.jobs.append(
            ScheduledJob(
                name=name,
                operation=operation,
                context=context,
                fn=fn,
            )
        )

    def run_all(self) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []

        for job in self.jobs:
            result = self.regulus.run_with_regulus(
                operation=job.operation,
                context=job.context,
                fn=job.fn,
            )
            results.append(
                {
                    "job": job.name,
                    "operation": job.operation,
                    "result": result,
                }
            )

        return results
