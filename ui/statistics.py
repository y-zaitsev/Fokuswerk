
import customtkinter as ctk


class StatisticsPage(ctk.CTkFrame):
    def __init__(self, master, db):
        super().__init__(master, fg_color="transparent")

        self.db = db

        self.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            self,
            text="Statistics",
            font=("Arial", 28, "bold")
        ).grid(
            row=0, column=0, columnspan=2,
            padx=30, pady=(30, 5), sticky="w"
        )

        ctk.CTkLabel(
            self,
            text="Your productivity at a glance.",
            text_color="gray"
        ).grid(
            row=1, column=0, columnspan=2,
            padx=30, sticky="w"
        )

        self.tasks_card = self.create_card(
            "Completed tasks", "0", 2, 0
        )

        self.focus_card = self.create_card(
            "Focus time", "0 min", 2, 1
        )

        self.sessions_card = self.create_card(
            "Focus sessions", "0", 3, 0
        )

        self.refresh()

    def create_card(self, title, value, row, column):
        card = ctk.CTkFrame(self, corner_radius=12)
        card.grid(
            row=row, column=column,
            padx=15, pady=15, sticky="nsew"
        )

        ctk.CTkLabel(
            card,
            text=title,
            text_color="gray",
            font=("Arial", 14)
        ).pack(anchor="w", padx=20, pady=(20, 5))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 30, "bold")
        )
        value_label.pack(anchor="w", padx=20, pady=(5, 20))

        return value_label

    def refresh(self):
        completed_tasks = self.db.get_completed_task_count()
        focus_minutes = self.db.get_focus_total_minutes()
        focus_sessions = self.db.count_focus_sessions()

        hours = focus_minutes // 60
        minutes = focus_minutes % 60

        self.tasks_card.configure(text=str(completed_tasks))
        self.focus_card.configure(
            text=f"{hours} h {minutes} min"
        )
        self.sessions_card.configure(text=str(focus_sessions))

    def on_show(self):
        self.refresh()
