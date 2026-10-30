
import customtkinter as ctk


class NotesPage(ctk.CTkFrame):
    def __init__(self, master, db):
        super().__init__(master, fg_color="transparent")

        self.db = db

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self, text="Notes",
            font=("Arial", 28, "bold")
        ).grid(row=0, column=0, padx=30, pady=(30, 5), sticky="w")

        ctk.CTkLabel(
            self, text="Keep your thoughts in one place.",
            text_color="gray"
        ).grid(row=1, column=0, padx=30, sticky="w")

        editor = ctk.CTkFrame(self, fg_color="transparent")
        editor.grid(row=2, column=0, padx=30, pady=15, sticky="nsew")
        editor.grid_columnconfigure(0, weight=1)

        self.title_entry = ctk.CTkEntry(
            editor, placeholder_text="Note title..."
        )
        self.title_entry.grid(
            row=0, column=0, sticky="ew", pady=(0, 10)
        )

        self.content_box = ctk.CTkTextbox(
            editor, height=120
        )
        self.content_box.grid(
            row=1, column=0, sticky="ew", pady=(0, 10)
        )

        ctk.CTkButton(
            editor, text="Save note",
            command=self.add_note
        ).grid(row=2, column=0, sticky="w")

        ctk.CTkLabel(
            self, text="Your notes",
            font=("Arial", 18, "bold")
        ).grid(row=3, column=0, padx=30, pady=(10, 5), sticky="w")

        self.notes_list = ctk.CTkScrollableFrame(
            self, fg_color="transparent"
        )
        self.notes_list.grid(
            row=4, column=0, padx=30, pady=(0, 25), sticky="nsew"
        )

        self.grid_rowconfigure(4, weight=1)

        self.refresh()

    def add_note(self):
        title = self.title_entry.get().strip()
        content = self.content_box.get("1.0", "end").strip()

        if not title:
            title = "Untitled note"

        if not content:
            return

        self.db.add_note(title, content)

        self.title_entry.delete(0, "end")
        self.content_box.delete("1.0", "end")

        self.refresh()

    def edit_note(self, note):
        dialog = ctk.CTkInputDialog(
            text="Enter the new note title:",
            title="Edit note"
        )
        new_title = dialog.get_input()

        if not new_title or not new_title.strip():
            return

        self.db.update_note(
            note["id"],
            new_title.strip(),
            note["content"]
        )
        self.refresh()

    def delete_note(self, note_id):
        self.db.delete_note(note_id)
        self.refresh()

    def refresh(self):
        for widget in self.notes_list.winfo_children():
            widget.destroy()

        notes = self.db.get_notes()

        if not notes:
            ctk.CTkLabel(
                self.notes_list,
                text="No notes yet.",
                text_color="gray"
            ).pack(pady=20)
            return

        for note in notes:
            card = ctk.CTkFrame(self.notes_list)
            card.pack(fill="x", padx=5, pady=5)

            ctk.CTkLabel(
                card,
                text=note["title"],
                font=("Arial", 16, "bold")
            ).pack(anchor="w", padx=12, pady=(10, 2))

            preview = note["content"][:180]

            ctk.CTkLabel(
                card,
                text=preview,
                text_color="gray",
                wraplength=650,
                justify="left"
            ).pack(anchor="w", padx=12, pady=5)

            buttons = ctk.CTkFrame(card, fg_color="transparent")
            buttons.pack(anchor="e", padx=8, pady=8)

            ctk.CTkButton(
                buttons, text="Edit", width=70,
                command=lambda n=note: self.edit_note(n)
            ).pack(side="left", padx=4)

            ctk.CTkButton(
                buttons, text="Delete", width=70,
                fg_color="#8B3030",
                hover_color="#A13A3A",
                command=lambda nid=note["id"]: self.delete_note(nid)
            ).pack(side="left", padx=4)
