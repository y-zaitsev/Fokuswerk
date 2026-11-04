from __future__ import annotations

import shutil
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator

from config import DB_FILENAME, LEGACY_DB_FILENAME, get_data_dir


def _now() -> str:
    """Lokale Zeit im Format von CURRENT_TIMESTAMP (das aber UTC liefert)."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Database:
    """SQLite storage for Fokuswerk.

    The database file is created automatically (see config.get_data_dir()).
    """

    def __init__(self, db_path: str | Path | None = None):
        if db_path:
            self.db_path = Path(db_path)
        else:
            data_dir = get_data_dir()
            self.db_path = data_dir / DB_FILENAME
            legacy = data_dir / LEGACY_DB_FILENAME
            if not self.db_path.exists() and legacy.exists():
                shutil.copy2(legacy, self.db_path)  # Daten vom alten Namen übernehmen
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        """Open a connection, commit/rollback on exit and ALWAYS close it.

        (``with sqlite3.connect(...)`` alone only commits - it never closes.)
        """
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    
    def initialize(self) -> None:
        """Create all application tables if they do not exist yet."""
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    priority TEXT NOT NULL DEFAULT 'medium'
                        CHECK(priority IN ('low', 'medium', 'high')),
                    status TEXT NOT NULL DEFAULT 'pending'
                        CHECK(status IN ('pending', 'completed')),
                    due_date TEXT,
                    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                    completed_at TEXT
                );

                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                    updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
                );

                CREATE TABLE IF NOT EXISTS focus_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    duration_minutes INTEGER NOT NULL,
                    session_type TEXT NOT NULL DEFAULT 'focus'
                        CHECK(session_type IN ('focus', 'short_break', 'long_break')),
                    started_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                    completed INTEGER NOT NULL DEFAULT 1
                        CHECK(completed IN (0, 1))
                );

                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                """
            )

            # Migration: add seconds column to existing databases
            columns = [
                row["name"]
                for row in conn.execute(
                    "PRAGMA table_info(focus_sessions)"
                ).fetchall()
            ]

            if "duration_seconds" not in columns:
                conn.execute(
                    """
                    ALTER TABLE focus_sessions
                    ADD COLUMN duration_seconds INTEGER NOT NULL DEFAULT 0
                    """
                )

            # Preserve the duration of older sessions
            conn.execute(
                """
                UPDATE focus_sessions
                SET duration_seconds = duration_minutes * 60
                WHERE duration_seconds = 0
                """
            )

            self._migrate_timestamps_to_local(conn)


    @staticmethod
    def _migrate_timestamps_to_local(conn: sqlite3.Connection) -> None:
        """Ältere Versionen speicherten UTC (CURRENT_TIMESTAMP). Einmalig auf lokale Zeit umstellen."""
        done = conn.execute(
            "SELECT 1 FROM settings WHERE key = 'timestamps_local'"
        ).fetchone()
        if done:
            return
        conn.execute(
            """UPDATE tasks SET
                   created_at = COALESCE(datetime(created_at, 'localtime'), created_at),
                   completed_at = COALESCE(datetime(completed_at, 'localtime'), completed_at)"""
        )
        conn.execute(
            """UPDATE notes SET
                   created_at = COALESCE(datetime(created_at, 'localtime'), created_at),
                   updated_at = COALESCE(datetime(updated_at, 'localtime'), updated_at)"""
        )
        conn.execute(
            """UPDATE focus_sessions SET
                   started_at = COALESCE(datetime(started_at, 'localtime'), started_at)"""
        )
        conn.execute("INSERT INTO settings (key, value) VALUES ('timestamps_local', '1')")

    # Tasks
    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        due_date: str | None = None,
    ) -> int:
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        with self._connect() as conn:
            cursor = conn.execute(
                """INSERT INTO tasks (title, description, priority, due_date, created_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (title, description, priority, due_date, _now()),
            )
            return int(cursor.lastrowid)

    def get_tasks(self, status: str | None = None) -> list[dict[str, Any]]:
        with self._connect() as conn:
            if status is None:
                rows = conn.execute(
                    "SELECT * FROM tasks ORDER BY created_at DESC, id DESC"
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC, id DESC",
                    (status,),
                ).fetchall()
            return [dict(row) for row in rows]

    def set_task_status(self, task_id: int, status: str) -> None:
        if status not in {"pending", "completed"}:
            raise ValueError("Status must be 'pending' or 'completed'.")
        with self._connect() as conn:
            conn.execute(
                """UPDATE tasks
                   SET status = ?,
                       completed_at = CASE WHEN ? = 'completed'
                                           THEN ? ELSE NULL END
                   WHERE id = ?""",
                (status, status, _now(), task_id),
            )

    def delete_task(self, task_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    # Notes
    def add_note(self, title: str, content: str = "") -> int:
        title = title.strip()
        if not title:
            raise ValueError("Note title cannot be empty.")
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO notes (title, content, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (title, content, _now(), _now()),
            )
            return int(cursor.lastrowid)

    def get_notes(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM notes ORDER BY updated_at DESC, id DESC"
            ).fetchall()
            return [dict(row) for row in rows]

    def update_note(self, note_id: int, title: str, content: str) -> None:
        with self._connect() as conn:
            conn.execute(
                """UPDATE notes
                   SET title = ?, content = ?, updated_at = ?
                   WHERE id = ?""",
                (title.strip(), content, _now(), note_id),
            )

    def delete_note(self, note_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))

    
    # Focus sessions
    def add_focus_session(
        self,
        duration_minutes: int,
        session_type: str = "focus",
        completed: bool = True,
        started_at: str | None = None,
    ) -> int:
        if duration_minutes <= 0:
            raise ValueError("Duration must be greater than zero.")

        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO focus_sessions
                (duration_minutes, duration_seconds, session_type, completed, started_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    duration_minutes,
                    duration_minutes * 60,
                    session_type,
                    int(completed),
                    started_at or _now(),
                ),
            )
            return int(cursor.lastrowid)

    def save_focus_session(
        self,
        session_id: int | None,
        duration_seconds: int,
        session_type: str = "focus",
        completed: bool = False,
    ) -> int | None:
        duration_seconds = max(0, int(duration_seconds))

        if duration_seconds == 0:
            return session_id

        duration_minutes = max(1, duration_seconds // 60)

        with self._connect() as conn:
            if session_id is None:
                cursor = conn.execute(
                    """
                    INSERT INTO focus_sessions
                    (duration_minutes, duration_seconds, session_type, completed, started_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        duration_minutes,
                        duration_seconds,
                        session_type,
                        int(completed),
                        _now(),
                    ),
                )
                return int(cursor.lastrowid)

            conn.execute(
                """
                UPDATE focus_sessions
                SET duration_minutes = ?,
                    duration_seconds = ?,
                    session_type = ?,
                    completed = ?
                WHERE id = ?
                """,
                (
                    duration_minutes,
                    duration_seconds,
                    session_type,
                    int(completed),
                    session_id,
                ),
            )
            return session_id

    def get_focus_sessions(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM focus_sessions
                ORDER BY started_at DESC, id DESC
                """
            ).fetchall()

            return [dict(row) for row in rows]


    # Statistics
    def get_completed_task_count(self) -> int:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS n FROM tasks WHERE status = 'completed'"
            ).fetchone()
            return int(row["n"])

    def get_focus_total_minutes(self) -> int:
        """Total minutes of finished focus sessions (breaks are not counted)."""
        with self._connect() as conn:
            row = conn.execute(
                """SELECT COALESCE(SUM(duration_seconds), 0) AS s
                   FROM focus_sessions
                   WHERE session_type = 'focus' AND completed = 1"""
            ).fetchone()
            return int(row["s"]) // 60

    def count_focus_sessions(self) -> int:
        with self._connect() as conn:
            row = conn.execute(
                """SELECT COUNT(*) AS n FROM focus_sessions
                   WHERE session_type = 'focus' AND completed = 1"""
            ).fetchone()
            return int(row["n"])

    def get_focus_seconds_for_day(self, day: str) -> int:
        """Focus seconds for a local date 'YYYY-MM-DD'."""
        with self._connect() as conn:
            row = conn.execute(
                """SELECT COALESCE(SUM(duration_seconds), 0) AS s
                   FROM focus_sessions
                   WHERE session_type = 'focus' AND completed = 1
                     AND substr(started_at, 1, 10) = ?""",
                (day,),
            ).fetchone()
            return int(row["s"])

    # Settings
    def set_setting(self, key: str, value: str) -> None:
        with self._connect() as conn:
            conn.execute(
                """INSERT INTO settings (key, value) VALUES (?, ?)
                   ON CONFLICT(key) DO UPDATE SET value = excluded.value""",
                (key, value),
            )

    def get_setting(self, key: str, default: str | None = None) -> str | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT value FROM settings WHERE key = ?", (key,)
            ).fetchone()
            return row["value"] if row else default
