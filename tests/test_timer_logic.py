"""Tests für die Timer-Logik OHNE Fenster (customtkinter wird durch eine Attrappe ersetzt)."""
import sys
import tempfile
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


class _Widget:
    """Universal-Attrappe: merkt sich configure(...) und ignoriert pack/grid/..."""

    def __init__(self, *args, **kwargs):
        self.options = dict(kwargs)
        self._callbacks = {}
        self._next_id = 0
        self.bell_count = 0

    def configure(self, **kwargs):
        self.options.update(kwargs)

    def __getattr__(self, name):
        return lambda *a, **k: None

    # kleiner Ersatz für Tk-after
    def after(self, ms, func):
        self._next_id += 1
        self._callbacks[self._next_id] = func
        return self._next_id

    def after_cancel(self, after_id):
        self._callbacks.pop(after_id, None)

    def bell(self):
        self.bell_count += 1


def _install_fake_ctk():
    fake = types.ModuleType("customtkinter")
    for name in ("CTkFrame", "CTkLabel", "CTkButton", "CTkProgressBar"):
        setattr(fake, name, type(name, (_Widget,), {}))
    sys.modules["customtkinter"] = fake


_install_fake_ctk()

import ui.timer as timer_module  # noqa: E402
from database import Database  # noqa: E402


class TimerLogicTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.db = Database(Path(self._tmp.name) / "t.db")
        self.clock = [1000.0]
        timer_module.time = types.SimpleNamespace(monotonic=lambda: self.clock[0])
        self.page = timer_module.TimerPage(None, self.db)

    def tearDown(self):
        self._tmp.cleanup()

    def advance(self, seconds):
        """Uhr vorstellen und geplante after()-Aufrufe ausführen."""
        self.clock[0] += seconds
        pending = list(self.page._callbacks.items())
        self.page._callbacks.clear()
        for _, func in pending:
            func()

    def test_page_switch_does_not_reset_running_timer(self):
        self.page.toggle_timer()
        self.advance(10)
        self.assertEqual(self.page.remaining, 25 * 60 - 10)

        self.page.on_show()      # passiert bei jedem Seitenwechsel
        self.page.refresh()
        self.assertEqual(self.page.remaining, 25 * 60 - 10)

    def test_page_switch_does_not_reset_paused_timer(self):
        self.page.toggle_timer()
        self.advance(300)
        self.page.toggle_timer()  # Pause
        self.page.on_show()
        self.assertEqual(self.page.remaining, 25 * 60 - 300)
        self.assertEqual(self.page.start_button.options["text"], "Resume")

        self.page.toggle_timer()  # weiter
        self.advance(60)
        self.assertEqual(self.page.remaining, 25 * 60 - 360)

    def test_no_drift_when_callbacks_are_late(self):
        self.page.toggle_timer()
        self.advance(1.7)   # after() kommt zu spät - früher ging dabei Zeit verloren
        self.advance(1.7)   # insgesamt 3,4 s Systemzeit
        self.assertEqual(self.page.remaining, 1497)  # ceil(1500 - 3.4), nicht 1498 wie bei "-= 1" pro Tick

    def test_finish_saves_once_and_restart_does_not_save_again(self):
        self.db.set_setting("focus_duration", "1")
        self.page.on_show()
        self.page.toggle_timer()
        self.advance(61)

        self.assertEqual(self.db.count_focus_sessions(), 1)
        self.assertEqual(self.page.remaining, 0)
        self.assertFalse(self.page.running)
        self.assertEqual(self.page.bell_count, 1)

        self.page.toggle_timer()  # Start nach Ablauf: darf NICHT sofort erneut speichern
        self.assertEqual(self.db.count_focus_sessions(), 1)
        self.assertEqual(self.page.remaining, 60)
        self.assertTrue(self.page.running)

    def test_reset_and_mode_switch(self):
        self.page.toggle_timer()
        self.advance(100)
        self.page.reset_timer()
        self.assertEqual(self.page.remaining, 25 * 60)
        self.assertFalse(self.page.started)

        self.page.set_mode("short_break")
        self.assertEqual(self.page.remaining, 5 * 60)


if __name__ == "__main__":
    unittest.main()
