from datetime import datetime
import customtkinter as ctk
from config import COLORS

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, db=None, on_start_focus=None):
        super().__init__(master, fg_color=COLORS["background"], corner_radius=0)
        self.db = db
        self.on_start_focus = on_start_focus
        self.pack_propagate(False)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="cards")
        self.grid_rowconfigure(3, weight=1)

        today = datetime.now().strftime("%A, %B %d")
        ctk.CTkLabel(
            self, text="Good afternoon 👋", text_color=COLORS["text"],
            font=ctk.CTkFont(size=30, weight="bold")
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=34, pady=(34, 2))
        ctk.CTkLabel(
            self, text=f"Make today count.  •  {today}",
            text_color=COLORS["muted"], font=ctk.CTkFont(size=13)
        ).grid(row=1, column=0, columnspan=4, sticky="w", padx=36, pady=(0, 26))

        metrics = [
            ("TOTAL TASKS", "08", "Across your workspace", COLORS["accent"]),
            ("COMPLETED", "05", "Tasks finished today", COLORS["success"]),
            ("FOCUS TIME", "1h 25m", "Time well spent", COLORS["warning"]),
            ("DAILY PROGRESS", "62%", "Keep it going", COLORS["accent"]),
        ]
        for col, (label, value, hint, accent) in enumerate(metrics):
            self._metric_card(col, label, value, hint, accent)

        tasks_card = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=16)
        tasks_card.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=(34, 10), pady=(22, 30))
        tasks_card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            tasks_card, text="Today's tasks", text_color=COLORS["text"],
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=22, pady=(20, 4))
        ctk.CTkLabel(
            tasks_card, text="A little progress adds up.",
            text_color=COLORS["muted"], font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=22, pady=(0, 14))

        sample_tasks = [
            ("Review project roadmap", "HIGH", COLORS["danger"], True),
            ("Read 20 pages", "MEDIUM", COLORS["warning"], False),
            ("Organize workspace", "LOW", COLORS["success"], False),
            ("Plan tomorrow", "MEDIUM", COLORS["warning"], True),
        ]
        for title, priority, color, done in sample_tasks:
            self._task_row(tasks_card, title, priority, color, done)

        focus_card = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=16)
        focus_card.grid(row=3, column=3, sticky="nsew", padx=(10, 34), pady=(22, 30))
        ctk.CTkLabel(
            focus_card, text="Focus session", text_color=COLORS["text"],
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=18, pady=(20, 6))
        ctk.CTkLabel(
            focus_card, text="TIME TO FOCUS", text_color=COLORS["muted"],
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(pady=(24, 4))
        ctk.CTkLabel(
            focus_card, text="25:00", text_color=COLORS["text"],
            font=ctk.CTkFont(size=38, weight="bold")
        ).pack(pady=4)
        ctk.CTkLabel(
            focus_card, text="One thing at a time.", text_color=COLORS["muted"],
            font=ctk.CTkFont(size=11)
        ).pack(pady=(0, 18))
        ctk.CTkButton(
            focus_card, text="Start focusing", height=40, corner_radius=10,
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            command=lambda: None
        ).pack(fill="x", padx=18, pady=(0, 18))

    def _metric_card(self, column, label, value, hint, accent):
        card = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=14)
        card.grid(row=2, column=column, sticky="ew", padx=(34 if column == 0 else 10, 10 if column < 3 else 34), pady=0)
        ctk.CTkLabel(
            card, text=label, text_color=COLORS["muted"],
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="w", padx=17, pady=(17, 8))
        ctk.CTkLabel(
            card, text=value, text_color=accent,
            font=ctk.CTkFont(size=27, weight="bold")
        ).pack(anchor="w", padx=17)
        ctk.CTkLabel(
            card, text=hint, text_color=COLORS["muted"],
            font=ctk.CTkFont(size=10)
        ).pack(anchor="w", padx=17, pady=(3, 17))

    def _task_row(self, parent, title, priority, color, done):
        row = ctk.CTkFrame(parent, fg_color=COLORS["card_alt"], corner_radius=10)
        row.pack(fill="x", padx=18, pady=5)
        checkbox = ctk.CTkCheckBox(
            row, text=title, checkbox_width=18, checkbox_height=18,
            font=ctk.CTkFont(size=12),
            text_color=COLORS["muted"] if done else COLORS["text"],
            hover_color=COLORS["accent"], fg_color=COLORS["accent"]
        )
        checkbox.pack(side="left", padx=13, pady=13)
        if done:
            checkbox.select()
        ctk.CTkLabel(
            row, text=priority, text_color=color,
            font=ctk.CTkFont(size=9, weight="bold")
        ).pack(side="right", padx=13)
