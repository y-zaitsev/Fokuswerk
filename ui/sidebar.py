import customtkinter as ctk
from config import COLORS

class Sidebar(ctk.CTkFrame):
    ITEMS = ["Dashboard", "Tasks", "Focus Timer", "Statistics", "Notes", "Settings"]

    def __init__(self, master, on_navigate):
        super().__init__(master, width=220, corner_radius=0, fg_color=COLORS["sidebar"])
        self.on_navigate = on_navigate
        self.buttons = {}
        self.grid_propagate(False)

        ctk.CTkLabel(
            self, text="◈  FocusDesk", font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w", padx=22, pady=(28, 36))

        ctk.CTkLabel(
            self, text="WORKSPACE", font=ctk.CTkFont(size=10, weight="bold"),
            text_color=COLORS["muted"]
        ).pack(anchor="w", padx=22, pady=(0, 12))

        for item in self.ITEMS:
            button = ctk.CTkButton(
                self, text=f"   {item}", anchor="w", height=42,
                corner_radius=10, border_spacing=10,
                fg_color="transparent", hover_color=COLORS["card_alt"],
                text_color=COLORS["muted"],
                font=ctk.CTkFont(size=14),
                command=lambda name=item: self.on_navigate(name)
            )
            button.pack(fill="x", padx=12, pady=3)
            self.buttons[item] = button

        ctk.CTkFrame(self, fg_color="transparent").pack(expand=True, fill="both")
        ctk.CTkLabel(
            self, text="VERSION 0.1.0", text_color=COLORS["muted"],
            font=ctk.CTkFont(size=10)
        ).pack(anchor="w", padx=22, pady=22)

    def set_active(self, active_name):
        for name, button in self.buttons.items():
            selected = name == active_name
            button.configure(
                fg_color=COLORS["accent"] if selected else "transparent",
                text_color=COLORS["text"] if selected else COLORS["muted"],
                hover_color=COLORS["accent_hover"] if selected else COLORS["card_alt"]
            )
