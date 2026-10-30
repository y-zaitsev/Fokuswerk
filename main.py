import customtkinter as ctk
from config import APP_NAME, WINDOW_SIZE, MIN_WINDOW_SIZE, COLORS
from ui.sidebar import Sidebar
from ui.dashboard import Dashboard
from ui.placeholder import PlaceholderPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class FocusDeskApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry(WINDOW_SIZE)
        self.minsize(*MIN_WINDOW_SIZE)
        self.configure(fg_color=COLORS["background"])

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.content = ctk.CTkFrame(self, fg_color=COLORS["background"], corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.sidebar = Sidebar(self, on_navigate=self.show_page)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.pages = {
            "Dashboard": Dashboard(self.content),
            "Tasks": PlaceholderPage(self.content, "Tasks", "Your tasks will live here."),
            "Focus Timer": PlaceholderPage(self.content, "Focus Timer", "A focused session starts here."),
            "Statistics": PlaceholderPage(self.content, "Statistics", "Your productivity insights will appear here."),
            "Notes": PlaceholderPage(self.content, "Notes", "A quiet space for your thoughts."),
            "Settings": PlaceholderPage(self.content, "Settings", "Make FocusDesk work your way."),
        }
        self.show_page("Dashboard")

    def show_page(self, page_name: str):
        for page in self.pages.values():
            page.grid_forget()
        self.pages[page_name].grid(row=0, column=0, sticky="nsew")
        self.sidebar.set_active(page_name)


if __name__ == "__main__":
    app = FocusDeskApp()
    app.mainloop()
