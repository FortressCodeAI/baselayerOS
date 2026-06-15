import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional


class SQLiteStateStore:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS state (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    hash TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS state_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    hash TEXT NOT NULL,
                    request_id TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT value, version, hash FROM state WHERE key = ?", (key,)
            ).fetchone()
            if not row:
                return None
            return {
                "value": json.loads(row["value"]),
                "version": row["version"],
                "hash": row["hash"],
            }

    def set(
        self,
        *,
        key: str,
        value: Dict[str, Any],
        version: int,
        hash_value: str,
        request_id: str,
    ) -> None:
        value_json = json.dumps(value, separators=(",", ":"), sort_keys=True)
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO state (key, value, version, hash)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    version = excluded.version,
                    hash = excluded.hash
                """,
                (key, value_json, version, hash_value),
            )
            conn.execute(
                """
                INSERT INTO state_history (key, value, version, hash, request_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (key, value_json, version, hash_value, request_id),
            )
            conn.commit()
