
import tkinter as tk
from ui import theme

from pages.dashboard import DashboardPage
from pages.timetable import TimetablePage
from pages.tasks import TasksPage
from pages.attendance import AttendancePage
from pages.cgpa import CgpaPage
from pages.profile import ProfilePage
from pages.placeholder import PlaceholderPage

from logic.timetable_logic import TimetableManager
from logic.task_logic import TaskManager
from logic.attendance_logic import AttendanceManager
from logic.cgpa_logic import CgpaManager

from ui.components import configure_table_styles

class CampusCompanion:

    def __init__(self, root):
        self.root = root
        self.root.title("Campus Companion")
        self.root.geometry("1200x750")
        self.root.minsize(950, 600)
        self.root.configure(bg=theme.BG)
        configure_table_styles(self.root)

        # Shared data managers
        self.timetable_manager = TimetableManager()
        self.task_manager = TaskManager()
        self.attendance_manager = AttendanceManager()
        self.cgpa_manager = CgpaManager()

        self.nav_buttons = {}

        self.create_sidebar()
        self.create_content()
        self.show_page("Dashboard")

    def create_sidebar(self):
        self.sidebar = tk.Frame(
            self.root, bg=theme.SIDEBAR, width=230
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="Campus Companion",
            font=(theme.FONT, 15, "bold"),
            bg=theme.SIDEBAR,
            fg=theme.TEXT
        ).pack(pady=(30, 5), padx=10)

        tk.Label(
            self.sidebar,
            text="STUDENT PRODUCTIVITY",
            font=(theme.FONT, 8, "bold"),
            bg=theme.SIDEBAR,
            fg=theme.MUTED
        ).pack(pady=(0, 30))

        menu_items = [
            "Dashboard",
            "Timetable",
            "Task Manager",
            "Attendance",
            "CGPA Calculator",
            "Profile"
        ]

        for page in menu_items:
            button = tk.Button(
                self.sidebar,
                text="   " + page,
                font=(theme.FONT, 11),
                bg=theme.SIDEBAR,
                fg=theme.MUTED,
                activebackground=theme.CARD_HOVER,
                activeforeground=theme.TEXT,
                relief="flat",
                anchor="w",
                padx=15,
                pady=12,
                cursor="hand2",
                command=lambda p=page: self.show_page(p)
            )

            button.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[page] = button

    def create_content(self):
        self.content = tk.Frame(self.root, bg=theme.BG)
        self.content.pack(side="right", fill="both", expand=True)

    def show_page(self, page):

        for widget in self.content.winfo_children():
            widget.destroy()

        for name, button in self.nav_buttons.items():
            button.configure(
                bg=theme.SIDEBAR,
                fg=theme.MUTED
            )

        self.nav_buttons[page].configure(
            bg=theme.CARD_HOVER,
            fg=theme.TEXT
        )

        if page == "Dashboard":
            frame = DashboardPage(
            self.content,
            self.timetable_manager,
            self.task_manager,
            self.attendance_manager,
            self.cgpa_manager
    )

        elif page == "Timetable":
            frame = TimetablePage(
                self.content, self.timetable_manager
            )

        elif page == "Task Manager":
            frame = TasksPage(
                self.content, self.task_manager
            )

        elif page == "Attendance":
            frame = AttendancePage(
                self.content, self.attendance_manager
            )

        elif page == "CGPA Calculator":
            frame = CgpaPage(
                self.content, self.cgpa_manager
            )

        elif page == "Profile":
            frame = ProfilePage(self.content)

        else:
            frame = PlaceholderPage(self.content, page)

        frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )
