import customtkinter as ctk
from config import COLORS

class PlaceholderPage(ctk.CTkFrame):
    def __init__(self, master, title, subtitle):
        super().__init__(master, fg_color=COLORS["background"], corner_radius=0)
        ctk.CTkLabel(
            self, text=title, text_color=COLORS["text"],
            font=ctk.CTkFont(size=30, weight="bold")
        ).pack(anchor="w", padx=36, pady=(40, 6))
        ctk.CTkLabel(
            self, text=subtitle, text_color=COLORS["muted"],
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=38)
        panel = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=16)
        panel.pack(fill="both", expand=True, padx=36, pady=30)
        ctk.CTkLabel(
            panel, text="Coming in the next update",
            text_color=COLORS["muted"], font=ctk.CTkFont(size=16)
        ).place(relx=0.5, rely=0.5, anchor="center")
