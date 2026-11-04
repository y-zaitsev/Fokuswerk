"""Tests für die Datenbank. Nutzen eine temporäre Datei, niemals die echte Datenbank.

Start:  py -m unittest -v
"""
import sqlite3
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from database import Database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.db = Database(Path(self._tmp.name) / "test.db")

    def tearDown(self):
        self._tmp.cleanup()

    def test_tasks_roundtrip(self):
        task_id = self.db.add_task("Test task", "desc", "high")
        self.assertEqual(self.db.get_tasks()[0]["title"], "Test task")

        self.db.set_task_status(task_id, "completed")
        self.assertEqual(self.db.get_completed_task_count(), 1)
        self.assertIsNotNone(self.db.get_tasks("completed")[0]["completed_at"])

        self.db.set_task_status(task_id, "pending")
        self.assertEqual(self.db.get_completed_task_count(), 0)

        self.db.delete_task(task_id)
        self.assertEqual(self.db.get_tasks(), [])

    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            self.db.add_task("   ")
        with self.assertRaises(ValueError):
            self.db.add_note("")

    def test_notes_roundtrip(self):
        note_id = self.db.add_note("Title", "Body")
        self.db.update_note(note_id, "New", "Body 2")
        note = self.db.get_notes()[0]
        self.assertEqual((note["title"], note["content"]), ("New", "Body 2"))
        self.db.delete_note(note_id)
        self.assertEqual(self.db.get_notes(), [])

    def test_focus_total_counts_only_finished_focus_sessions(self):
        self.db.add_focus_session(25)                                  # zählt
        self.db.add_focus_session(25)                                  # zählt
        self.db.add_focus_session(5, session_type="short_break")       # Pause: nein
        self.db.add_focus_session(25, completed=False)                 # abgebrochen: nein
        self.assertEqual(self.db.get_focus_total_minutes(), 50)
        self.assertEqual(self.db.count_focus_sessions(), 2)

    def test_focus_seconds_for_day_uses_local_date(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.db.add_focus_session(25)
        self.db.add_focus_session(10, started_at="2000-01-01 12:00:00")
        self.assertEqual(self.db.get_focus_seconds_for_day(today), 25 * 60)
        self.assertEqual(self.db.get_focus_seconds_for_day("2000-01-01"), 10 * 60)

    def test_settings_roundtrip(self):
        self.assertIsNone(self.db.get_setting("x"))
        self.db.set_setting("x", "1")
        self.db.set_setting("x", "2")
        self.assertEqual(self.db.get_setting("x"), "2")

    def test_connections_are_closed(self):
        # Windows kann eine Datei mit offener Verbindung nicht löschen.
        self.db.add_task("x")
        Path(self.db.db_path).unlink()

    def test_old_utc_timestamps_are_converted_once(self):
        old = Path(self._tmp.name) / "old.db"
        conn = sqlite3.connect(old)
        conn.executescript("""
            CREATE TABLE tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '', priority TEXT NOT NULL DEFAULT 'medium',
                status TEXT NOT NULL DEFAULT 'pending', due_date TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, completed_at TEXT);
            INSERT INTO tasks (title, created_at) VALUES ('alt', '2026-01-15 12:00:00');
        """)
        conn.commit(); conn.close()

        db = Database(old)
        first = db.get_tasks()[0]["created_at"]
        Database(old)  # zweiter Start darf nicht erneut umrechnen
        self.assertEqual(db.get_tasks()[0]["created_at"], first)
        self.assertEqual(db.get_setting("timestamps_local"), "1")


if __name__ == "__main__":
    unittest.main()
