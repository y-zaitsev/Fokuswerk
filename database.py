from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class Database:
    """SQLite storage for Mindrift.

    The database file is created automatically in the project's data/ folder.
    """

    def __init__(self, db_path: str | Path | None = None):
        project_dir = Path(__file__).resolve().parent
        self.db_path = Path(db_path) if db_path else project_dir / "data" / "mindrift.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

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
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    completed_at TEXT
                );

                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS focus_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    duration_minutes INTEGER NOT NULL,
                    session_type TEXT NOT NULL DEFAULT 'focus'
                        CHECK(session_type IN ('focus', 'short_break', 'long_break')),
                    started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    completed INTEGER NOT NULL DEFAULT 1
                        CHECK(completed IN (0, 1))
                );

                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                """
            )

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
                """INSERT INTO tasks (title, description, priority, due_date)
                   VALUES (?, ?, ?, ?)""",
                (title, description, priority, due_date),
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
                                           THEN CURRENT_TIMESTAMP ELSE NULL END
                   WHERE id = ?""",
                (status, status, task_id),
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
                "INSERT INTO notes (title, content) VALUES (?, ?)",
                (title, content),
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
                   SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (title.strip(), content, note_id),
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
    ) -> int:
        if duration_minutes <= 0:
            raise ValueError("Duration must be greater than zero.")
        with self._connect() as conn:
            cursor = conn.execute(
                """INSERT INTO focus_sessions
                   (duration_minutes, session_type, completed)
                   VALUES (?, ?, ?)""",
                (duration_minutes, session_type, int(completed)),
            )
            return int(cursor.lastrowid)

    def get_focus_sessions(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM focus_sessions ORDER BY started_at DESC, id DESC"
            ).fetchall()
            return [dict(row) for row in rows]

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
