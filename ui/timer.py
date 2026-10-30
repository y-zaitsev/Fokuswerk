
import customtkinter as ctk


class TimerPage(ctk.CTkFrame):
    def __init__(self, master, db):
        super().__init__(master, fg_color="transparent")

        self.db = db
        self.mode = "focus"
        self.remaining = 25 * 60
        self.running = False
        self.after_id = None

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

        self.remaining = self.durations[self.mode] * 60

    def set_mode(self, mode):
        self.pause_timer()
        self.mode = mode
        self.remaining = self.durations[mode] * 60
        self.status_label.configure(text="Ready when you are.")
        self.update_display()

    def toggle_timer(self):
        if self.running:
            self.pause_timer()
        else:
            self.running = True
            self.start_button.configure(text="Pause")
            self.status_label.configure(text="Session in progress...")
            self.tick()

    def pause_timer(self):
        self.running = False
        self.start_button.configure(text="Start")

        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

    def reset_timer(self):
        self.pause_timer()
        self.remaining = self.durations[self.mode] * 60
        self.status_label.configure(text="Timer reset.")
        self.update_display()

    def tick(self):
        if not self.running:
            return

        if self.remaining <= 0:
            self.finish_session()
            return

        self.remaining -= 1
        self.update_display()

        self.after_id = self.after(1000, self.tick)

    def finish_session(self):
        self.pause_timer()

        minutes = self.durations[self.mode]

        try:
            self.db.add_focus_session(
                minutes,
                session_type=self.mode,
                completed=True
            )
        except TypeError:
            self.db.add_focus_session(minutes, self.mode)

        self.remaining = 0
        self.update_display()
        self.status_label.configure(text="Session completed!")

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
