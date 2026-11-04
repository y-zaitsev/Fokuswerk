
import math
import sqlite3
import time
from datetime import datetime

import customtkinter as ctk


class TimerPage(ctk.CTkFrame):
    def __init__(self, master, db):
        super().__init__(master, fg_color="transparent")

        self.db = db
        self.mode = "focus"
        self.remaining = 25 * 60
        self.running = False
        self.after_id = None
        self.started = False            # Sitzung läuft oder ist pausiert (nicht frisch)
        self.deadline = 0.0             # time.monotonic()-Zeitpunkt des Endes
        self.session_started_at = None  # lokaler Startzeitpunkt für die Datenbank

        self.durations = {
            "focus": 25,
            "short_break": 5,
            "long_break": 15
        }

        self.load_durations()

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self, text="Focus Timer",
            font=("Arial", 28, "bold")
        ).pack(pady=(35, 5))

        ctk.CTkLabel(
            self, text="Make time for what matters.",
            text_color="gray"
        ).pack(pady=(0, 25))

        self.mode_label = ctk.CTkLabel(
            self, text="FOCUS",
            font=("Arial", 16, "bold")
        )
        self.mode_label.pack(pady=10)

        self.time_label = ctk.CTkLabel(
            self, text="25:00",
            font=("Arial", 64, "bold")
        )
        self.time_label.pack(pady=20)

        self.progress = ctk.CTkProgressBar(self, width=350)
        self.progress.pack(pady=15)
        self.progress.set(1)

        mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        mode_frame.pack(pady=20)

        ctk.CTkButton(
            mode_frame, text="Focus",
            command=lambda: self.set_mode("focus")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            mode_frame, text="Short Break",
            command=lambda: self.set_mode("short_break")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            mode_frame, text="Long Break",
            command=lambda: self.set_mode("long_break")
        ).pack(side="left", padx=5)

        control_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_frame.pack(pady=15)

        self.start_button = ctk.CTkButton(
            control_frame, text="Start",
            width=120, height=40,
            command=self.toggle_timer
        )
        self.start_button.pack(side="left", padx=8)

        ctk.CTkButton(
            control_frame, text="Reset",
            width=120, height=40,
            fg_color="gray",
            command=self.reset_timer
        ).pack(side="left", padx=8)

        self.status_label = ctk.CTkLabel(
            self, text="Ready when you are.",
            text_color="gray"
        )
        self.status_label.pack(pady=15)

        self.update_display()

    def load_durations(self):
        for mode, default in self.durations.items():
            try:
                value = self.db.get_setting(mode + "_duration")
                self.durations[mode] = max(1, int(value or default))
            except (TypeError, ValueError):
                self.durations[mode] = default

        # Laufende oder pausierte Sitzungen NICHT anfassen. Sonst setzt jeder
        # Seitenwechsel (show_page -> on_show) den Countdown auf die volle Zeit zurück.
        if not self.started:
            self.remaining = self.durations[self.mode] * 60

    def set_mode(self, mode):
        self.pause_timer()
        self.mode = mode
        self.started = False
        self.session_started_at = None
        self.remaining = self.durations[mode] * 60
        self.status_label.configure(text="Ready when you are.")
        self.update_display()

    def toggle_timer(self):
        if self.running:
            self.pause_timer()
            self.start_button.configure(text="Resume")
            self.status_label.configure(text="Paused.")
            return

        # Nach Ablauf steht remaining auf 0: neue Sitzung starten statt sofort
        # eine weitere (leere) Sitzung zu speichern.
        if self.remaining <= 0:
            self.remaining = self.durations[self.mode] * 60

        if not self.started:
            self.started = True
            self.session_started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.running = True
        self.deadline = time.monotonic() + self.remaining
        self.start_button.configure(text="Pause")
        self.status_label.configure(text="Session in progress...")
        self.tick()

    def pause_timer(self):
        if self.running:
            self.remaining = max(0, math.ceil(self.deadline - time.monotonic()))

        self.running = False
        self.start_button.configure(text="Start")

        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

    def reset_timer(self):
        self.pause_timer()
        self.started = False
        self.session_started_at = None
        self.remaining = self.durations[self.mode] * 60
        self.status_label.configure(text="Timer reset.")
        self.update_display()

    def tick(self):
        if not self.running:
            return

        # Restzeit aus der Systemuhr berechnen statt "remaining -= 1":
        # after(1000) kommt immer etwas zu spät und der Fehler summiert sich.
        remaining = max(0, math.ceil(self.deadline - time.monotonic()))

        if remaining != self.remaining:
            self.remaining = remaining
            self.update_display()

        if self.remaining <= 0:
            self.finish_session()
            return

        self.after_id = self.after(200, self.tick)

    def finish_session(self):
        self.pause_timer()

        minutes = self.durations[self.mode]

        try:
            self.db.add_focus_session(
                minutes,
                session_type=self.mode,
                completed=True,
                started_at=self.session_started_at,
            )
            message = "Session completed!"
        except sqlite3.Error:
            message = "Session completed, but it could not be saved."

        self.started = False
        self.session_started_at = None
        self.remaining = 0
        self.update_display()
        self.status_label.configure(text=message)
        self.bell()

    def update_display(self):
        minutes = self.remaining // 60
        seconds = self.remaining % 60

        self.time_label.configure(
            text=f"{minutes:02d}:{seconds:02d}"
        )

        self.mode_label.configure(
            text=self.mode.replace("_", " ").upper()
        )

        total = self.durations[self.mode] * 60
        self.progress.set(self.remaining / total if total else 0)

    def refresh(self):
        self.load_durations()
        self.update_display()

    def on_show(self):
        self.load_durations()
        self.update_display()
