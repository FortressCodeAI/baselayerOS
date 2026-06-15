# baselayeros/giu/metering.py

"""
GIU metering: tracks resource usage for deterministic governance.
"""

from dataclasses import dataclass


@dataclass
class Meter:
    count: int = 0

    def increment(self, amount: int = 1) -> None:
        self.count += amount
