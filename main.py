
import customtkinter as ctk

from config import APP_NAME, COLORS
from database import Database

from ui.sidebar import Sidebar
from ui.dashboard import Dashboard
from ui.tasks import TasksPage
from ui.timer import TimerPage
from ui.notes import NotesPage
from ui.statistics import StatisticsPage
from ui.settings import SettingsPage


class MindriftApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.db = Database()

        self.title(APP_NAME)
        self.geometry("1200x750")
        self.minsize(950, 600)

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

        if hasattr(page, "on_show"):
            page.on_show()

        if hasattr(page, "refresh"):
            page.refresh()

        self.sidebar.set_active(page_name)

    def on_close(self):

        timer = self.pages.get("Focus Timer")

        if timer and timer.after_id:
            timer.after_cancel(timer.after_id)

        self.destroy()


if __name__ == "__main__":

    app = MindriftApp()
    app.mainloop()
