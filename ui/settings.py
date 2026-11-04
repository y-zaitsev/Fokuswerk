
import customtkinter as ctk

from config import APP_NAME


class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, db, app):
        super().__init__(master, fg_color="transparent")

        self.db = db
        self.app = app

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Settings",
            font=("Arial", 28, "bold")
        ).pack(anchor="w", padx=30, pady=(30, 5))

        ctk.CTkLabel(
            self,
            text=f"Customize your {APP_NAME} experience.",
            text_color="gray"
        ).pack(anchor="w", padx=30, pady=(0, 20))

        timer_frame = ctk.CTkFrame(self)
        timer_frame.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(
            timer_frame,
            text="Pomodoro durations",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 10))

        self.focus_entry = self.create_setting(
            timer_frame, "Focus duration (minutes)", "focus_duration", 25
        )

        self.short_entry = self.create_setting(
            timer_frame, "Short break (minutes)", "short_break_duration", 5
        )

        self.long_entry = self.create_setting(
            timer_frame, "Long break (minutes)", "long_break_duration", 15
        )

        appearance_frame = ctk.CTkFrame(self)
        appearance_frame.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(
            appearance_frame,
            text="Appearance",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 10))

        # Die Farben sind fest auf Dark ausgelegt - ein "Light"-Modus würde die
        # Oberfläche zerschießen. Bis es eine echte helle Palette gibt: nur Hinweis.
        ctk.CTkLabel(
            appearance_frame,
            text="Dark theme (a light theme is planned).",
            text_color="gray"
        ).pack(anchor="w", padx=20, pady=(0, 15))

        ctk.CTkButton(
            self,
            text="Save settings",
            command=self.save_settings
        ).pack(anchor="w", padx=30, pady=15)

        self.status_label = ctk.CTkLabel(
            self, text="", text_color="gray"
        )
        self.status_label.pack(anchor="w", padx=30)

    def read_setting(self, key, default):
        try:
            value = self.db.get_setting(key)
            return value if value is not None else default
        except (AttributeError, TypeError):
            return default

    def create_setting(self, parent, label, key, default):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(
            row, text=label
        ).pack(side="left")

        entry = ctk.CTkEntry(row, width=100)
        entry.pack(side="right")

        value = self.read_setting(key, str(default))
        entry.insert(0, str(value))

        return entry

    def save_settings(self):
        try:
            focus = int(self.focus_entry.get())
            short = int(self.short_entry.get())
            long = int(self.long_entry.get())

            if not all(1 <= value <= 180 for value in [focus, short, long]):
                raise ValueError

        except ValueError:
            self.status_label.configure(
                text="Enter durations between 1 and 180 minutes.",
                text_color="#E06C75"
            )
            return

        self.db.set_setting("focus_duration", str(focus))
        self.db.set_setting("short_break_duration", str(short))
        self.db.set_setting("long_break_duration", str(long))

        self.status_label.configure(
            text="Settings saved successfully!",
            text_color="#75C98B"
        )

    def refresh(self):
        pass

    def on_show(self):
        pass
