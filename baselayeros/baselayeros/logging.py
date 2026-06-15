from __future__ import annotations

import sys
from datetime import datetime


class Logger:
    """
    Deterministic logging interface for BaseLayerOS.

    Characteristics:
    - writes to stdout only
    - timestamps are ISO-8601 UTC
    - no dynamic configuration
    - no nondeterministic formatting
    """

    LEVELS = {"DEBUG", "INFO", "WARN", "ERROR"}

    def __init__(self, level: str = "INFO"):
        level = level.upper()
        if level not in self.LEVELS:
            raise ValueError(f"Invalid log level: {level}")
        self.level = level

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------
    def _should_log(self, level: str) -> bool:
        order = ["DEBUG", "INFO", "WARN", "ERROR"]
        return order.index(level) >= order.index(self.level)

    def _emit(self, level: str, message: str) -> None:
        timestamp = datetime.utcnow().isoformat()
        sys.stdout.write(f"{timestamp} [{level}] {message}\n")

    # ---------------------------------------------------------
    # Public logging methods
    # ---------------------------------------------------------
    def debug(self, message: str) -> None:
        if self._should_log("DEBUG"):
            self._emit("DEBUG", message)

    def info(self, message: str) -> None:
        if self._should_log("INFO"):
            self._emit("INFO", message)

    def warn(self, message: str) -> None:
        if self._should_log("WARN"):
            self._emit("WARN", message)

    def error(self, message: str) -> None:
        if self._should_log("ERROR"):
            self._emit("ERROR", message)
