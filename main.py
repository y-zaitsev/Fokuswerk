
import customtkinter as ctk

from tkinter import messagebox

from config import APP_NAME, COLORS, MIN_WINDOW_SIZE, WINDOW_SIZE
from database import Database

from ui.sidebar import Sidebar
from ui.dashboard import Dashboard
from ui.tasks import TasksPage
from ui.timer import TimerPage
from ui.notes import NotesPage
from ui.statistics import StatisticsPage
from ui.settings import SettingsPage


class FokuswerkApp(ctk.CTk):

    def __init__(self):
        # Die Oberfläche ist komplett dunkel gestaltet. Ohne diese Zeile folgt
        # CustomTkinter dem Windows-Theme und Standard-Widgets werden hell.
        ctk.set_appearance_mode("dark")

        super().__init__()

        self.db = Database()

        self.title(APP_NAME)
        self.geometry(WINDOW_SIZE)
        self.minsize(*MIN_WINDOW_SIZE)

        self.configure(fg_color=COLORS["background"])

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.content = ctk.CTkFrame(
            self,
            fg_color=COLORS["background"],
            corner_radius=0
        )

        self.content.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(
            self,
            on_navigate=self.show_page
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        self.pages = {
            "Dashboard": Dashboard(
                self.content,
                self.db,
                lambda: self.show_page("Focus Timer")
            ),

            "Tasks": TasksPage(
                self.content,
                self.db
            ),

            "Focus Timer": TimerPage(
                self.content,
                self.db
            ),

            "Statistics": StatisticsPage(
                self.content,
                self.db
            ),

            "Notes": NotesPage(
                self.content,
                self.db
            ),

            "Settings": SettingsPage(
                self.content,
                self.db,
                self
            )
        }

        self.show_page("Dashboard")

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

    def show_page(self, page_name):

        for page in self.pages.values():
            page.grid_forget()

        page = self.pages[page_name]

        page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        # on_show() lädt die Seite bereits neu - nicht zusätzlich refresh() aufrufen.
        if hasattr(page, "on_show"):
            page.on_show()
        elif hasattr(page, "refresh"):
            page.refresh()

        self.sidebar.set_active(page_name)

    def on_close(self):

        timer = self.pages.get("Focus Timer")

        if timer and timer.running:
            if not messagebox.askyesno(APP_NAME, "The timer is still running. Quit anyway?"):
                return

        if timer and timer.after_id:
            timer.after_cancel(timer.after_id)

        self.destroy()


if __name__ == "__main__":

    app = FokuswerkApp()
    app.mainloop()
