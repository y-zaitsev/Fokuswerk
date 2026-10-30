
import customtkinter as ctk


class TasksPage(ctk.CTkFrame):
    def __init__(self, master, db):
        super().__init__(master, fg_color="transparent")

        self.db = db

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self,
            text="Tasks",
            font=("Arial", 28, "bold")
        ).grid(row=0, column=0, padx=30, pady=(30, 5), sticky="w")

        ctk.CTkLabel(
            self,
            text="Manage your tasks and stay focused.",
            text_color="gray"
        ).grid(row=1, column=0, padx=30, sticky="w")

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(
            row=2, column=0, padx=30, pady=20, sticky="new"
        )
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.task_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Enter a new task..."
        )
        self.task_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        ctk.CTkButton(
            self.input_frame,
            text="Add task",
            command=self.add_task
        ).grid(row=0, column=1)

        self.task_list = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.task_list.grid(
            row=3, column=0, padx=30, pady=(0, 30), sticky="nsew"
        )

        self.grid_rowconfigure(3, weight=1)

        self.refresh()

    def add_task(self):
        title = self.task_entry.get().strip()

        if not title:
            return

        self.db.add_task(title)
        self.task_entry.delete(0, "end")
        self.refresh()

    def toggle_task(self, task):
        new_status = (
            "completed"
            if task["status"] == "pending"
            else "pending"
        )

        self.db.set_task_status(task["id"], new_status)
        self.refresh()

    def refresh(self):
        for widget in self.task_list.winfo_children():
            widget.destroy()

        tasks = self.db.get_tasks()

        if not tasks:
            ctk.CTkLabel(
                self.task_list,
                text="No tasks yet. Add your first task above.",
                text_color="gray"
            ).pack(pady=20)
            return

        for task in tasks:
            row = ctk.CTkFrame(self.task_list)
            row.pack(fill="x", padx=5, pady=5)

            completed = task["status"] == "completed"

            ctk.CTkCheckBox(
                row,
                text=task["title"],
                command=lambda t=task: self.toggle_task(t)
            ).pack(side="left", padx=12, pady=12)

            if completed:
                # The task remains marked as completed in the database.
                pass

            ctk.CTkButton(
                row,
                text="Delete",
                width=70,
                fg_color="#8B3030",
                hover_color="#A13A3A",
                command=lambda task_id=task["id"]: self.delete_task(task_id)
            ).pack(side="right", padx=10, pady=8)

            if completed:
                # Show completed tasks as checked.
                for child in row.winfo_children():
                    if isinstance(child, ctk.CTkCheckBox):
                        child.select()

    def delete_task(self, task_id):
        self.db.delete_task(task_id)
        self.refresh()
