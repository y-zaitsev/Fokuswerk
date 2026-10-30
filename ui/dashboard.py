
from datetime import datetime
import customtkinter as ctk

from config import COLORS


class Dashboard(ctk.CTkFrame):
    def __init__(self, master, db=None, on_start_focus=None):
        super().__init__(
            master,
            fg_color=COLORS["background"],
            corner_radius=0
        )

        self.db = db
        self.on_start_focus = on_start_focus
        self.metric_values = {}

        self.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="cards")
        self.grid_rowconfigure(3, weight=1)

        today = datetime.now().strftime("%A, %B %d")

        ctk.CTkLabel(
            self,
            text="Good afternoon 👋",
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=30, weight="bold")
        ).grid(
            row=0, column=0, columnspan=4,
            sticky="w", padx=34, pady=(34, 2)
        )

        ctk.CTkLabel(
            self,
            text=f"Make today count.  •  {today}",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=13)
        ).grid(
            row=1, column=0, columnspan=4,
            sticky="w", padx=36, pady=(0, 26)
        )

        metrics = [
            ("TOTAL TASKS", "0", "Across your workspace", COLORS["accent"]),
            ("COMPLETED", "0", "Tasks finished", COLORS["success"]),
            ("FOCUS TIME", "0m", "Focused today", COLORS["warning"]),
            ("DAILY PROGRESS", "0%", "Tasks completed", COLORS["accent"]),
        ]

        for col, (label, value, hint, accent) in enumerate(metrics):
            self._metric_card(col, label, value, hint, accent)

        # Tasks section
        self.tasks_card = ctk.CTkFrame(
            self,
            fg_color=COLORS["card"],
            corner_radius=16
        )
        self.tasks_card.grid(
            row=3, column=0, columnspan=3,
            sticky="nsew", padx=(34, 10), pady=(22, 30)
        )
        self.tasks_card.grid_columnconfigure(0, weight=1)
        self.tasks_card.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self.tasks_card,
            text="Your tasks",
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=22, pady=(20, 4))

        ctk.CTkLabel(
            self.tasks_card,
            text="Your workspace at a glance.",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, sticky="w", padx=22, pady=(0, 14))

        self.task_list = ctk.CTkScrollableFrame(
            self.tasks_card,
            fg_color="transparent"
        )
        self.task_list.grid(
            row=2, column=0, sticky="nsew",
            padx=12, pady=(0, 12)
        )

        # Focus section
        focus_card = ctk.CTkFrame(
            self,
            fg_color=COLORS["card"],
            corner_radius=16
        )
        focus_card.grid(
            row=3, column=3,
            sticky="nsew", padx=(10, 34), pady=(22, 30)
        )

        ctk.CTkLabel(
            focus_card,
            text="Focus session",
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=18, pady=(20, 6))

        ctk.CTkLabel(
            focus_card,
            text="TIME TO FOCUS",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(pady=(24, 4))

        ctk.CTkLabel(
            focus_card,
            text="25:00",
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=38, weight="bold")
        ).pack(pady=4)

        ctk.CTkLabel(
            focus_card,
            text="One thing at a time.",
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=11)
        ).pack(pady=(0, 18))

        ctk.CTkButton(
            focus_card,
            text="Start focusing",
            height=40,
            corner_radius=10,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            command=self._start_focus
        ).pack(fill="x", padx=18, pady=(0, 18))

        self.refresh()

    def _metric_card(self, column, label, value, hint, accent):
        card = ctk.CTkFrame(
            self,
            fg_color=COLORS["card"],
            corner_radius=14
        )

        card.grid(
            row=2, column=column,
            sticky="ew",
            padx=(34 if column == 0 else 10,
                  10 if column < 3 else 34),
            pady=0
        )

        ctk.CTkLabel(
            card,
            text=label,
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(anchor="w", padx=17, pady=(17, 8))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            text_color=accent,
            font=ctk.CTkFont(size=27, weight="bold")
        )
        value_label.pack(anchor="w", padx=17)

        ctk.CTkLabel(
            card,
            text=hint,
            text_color=COLORS["muted"],
            font=ctk.CTkFont(size=10)
        ).pack(anchor="w", padx=17, pady=(3, 17))

        self.metric_values[label] = value_label

    def refresh(self):
        if self.db is None:
            return

        tasks = self.db.get_tasks()

        total = len(tasks)
        completed = sum(
            1 for task in tasks
            if task["status"] == "completed"
        )

        progress = round(completed / total * 100) if total else 0

        today = datetime.now().strftime("%Y-%m-%d")

        sessions = self.db.get_focus_sessions()

        focus_minutes = sum(
            session["duration_minutes"]
            for session in sessions
            if session["session_type"] == "focus"
            and session["completed"]
            and session["started_at"].startswith(today)
        )

        if focus_minutes >= 60:
            focus_text = f"{focus_minutes // 60}h {focus_minutes % 60}m"
        else:
            focus_text = f"{focus_minutes}m"

        self.metric_values["TOTAL TASKS"].configure(text=str(total))
        self.metric_values["COMPLETED"].configure(text=str(completed))
        self.metric_values["FOCUS TIME"].configure(text=focus_text)
        self.metric_values["DAILY PROGRESS"].configure(text=f"{progress}%")

        self._refresh_tasks(tasks)

    def _refresh_tasks(self, tasks):
        for widget in self.task_list.winfo_children():
            widget.destroy()

        if not tasks:
            ctk.CTkLabel(
                self.task_list,
                text="No tasks yet. Add your first task!",
                text_color=COLORS["muted"],
                font=ctk.CTkFont(size=13)
            ).pack(pady=25)
            return

        # Show the latest 8 tasks
        for task in tasks[:8]:
            self._task_row(task)

    def _task_row(self, task):
        row = ctk.CTkFrame(
            self.task_list,
            fg_color=COLORS["card_alt"],
            corner_radius=10
        )
        row.pack(fill="x", padx=6, pady=5)

        is_done = task["status"] == "completed"

        checkbox = ctk.CTkCheckBox(
            row,
            text=task["title"],
            checkbox_width=18,
            checkbox_height=18,
            font=ctk.CTkFont(size=12),
            text_color=COLORS["muted"] if is_done else COLORS["text"],
            hover_color=COLORS["accent"],
            fg_color=COLORS["accent"],
            command=lambda t=task: self._toggle_task(t, checkbox)
        )
        checkbox.pack(side="left", padx=13, pady=13)

        if is_done:
            checkbox.select()

        priority = task["priority"].upper()

        priority_colors = {
            "HIGH": COLORS["danger"],
            "MEDIUM": COLORS["warning"],
            "LOW": COLORS["success"]
        }

        ctk.CTkLabel(
            row,
            text=priority,
            text_color=priority_colors.get(priority, COLORS["muted"]),
            font=ctk.CTkFont(size=9, weight="bold")
        ).pack(side="right", padx=13)

    def _toggle_task(self, task, checkbox):
        new_status = "completed" if checkbox.get() else "pending"
        self.db.set_task_status(task["id"], new_status)
        self.refresh()

    def _start_focus(self):
        if self.on_start_focus:
            self.on_start_focus()

    def on_show(self):
        self.refresh()
