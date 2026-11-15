
import tkinter as tk
from datetime import datetime

from ui import theme
from ui.components import create_card, create_heading


class DashboardPage(tk.Frame):

    def __init__(
        self,
        parent,
        timetable_manager=None,
        task_manager=None,
        attendance_manager=None,
        cgpa_manager=None
    ):
        super().__init__(parent, bg=theme.BG)

        self.timetable_manager = timetable_manager
        self.task_manager = task_manager
        self.attendance_manager = attendance_manager
        self.cgpa_manager = cgpa_manager

        self.create_dashboard()

    def create_dashboard(self):

        heading = create_heading(
            self,
            "Dashboard",
            "Welcome to your student productivity dashboard."
        )
        heading.pack(anchor="w", pady=(10, 25))

        # Calculate actual values
        subjects = (
            self.attendance_manager.get_all_subjects()
            if self.attendance_manager else []
        )

        tasks = (
            self.task_manager.get_tasks("Pending")
            if self.task_manager else []
        )

        attendance_values = []

        for subject in subjects:
            total = subject["total_classes"]
            attended = subject["attended_classes"]

            if total > 0:
                attendance_values.append(
                    (attended / total) * 100
                )

        average_attendance = (
            sum(attendance_values) / len(attendance_values)
            if attendance_values else 0
        )

        sgpa = (
            self.cgpa_manager.calculate_sgpa()
            if self.cgpa_manager else 0
        )

        stats = [
            ("Total Subjects", str(len(subjects)), theme.PRIMARY),
            ("Attendance", f"{average_attendance:.1f}%", theme.SUCCESS),
            ("Pending Tasks", str(len(tasks)), theme.WARNING),
            ("Current SGPA", f"{sgpa:.2f}", theme.PRIMARY)
        ]

        stats_frame = tk.Frame(self, bg=theme.BG)
        stats_frame.pack(fill="x")

        for title, value, color in stats:
            card = create_card(stats_frame)
            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=(0, 12),
                pady=5
            )

            tk.Label(
                card,
                text=title,
                font=(theme.FONT, 10),
                bg=theme.CARD,
                fg=theme.MUTED
            ).pack(anchor="w")

            tk.Label(
                card,
                text=value,
                font=(theme.FONT, 23, "bold"),
                bg=theme.CARD,
                fg=color
            ).pack(anchor="w", pady=(8, 0))

        # Today's timetable
        schedule_card = create_card(self)
        schedule_card.pack(fill="x", pady=20)

        tk.Label(
            schedule_card,
            text="Today's Schedule",
            font=(theme.FONT, 15, "bold"),
            bg=theme.CARD,
            fg=theme.TEXT
        ).pack(anchor="w", pady=(0, 15))

        today = datetime.now().strftime("%A")

        classes = (
            self.timetable_manager.get_classes(today)
            if self.timetable_manager else []
        )

        if classes:
            for item in classes:
                text = (
                    f'{item["start_time"]} - {item["end_time"]}   '
                    f'{item["subject"]}   |   {item["room"]}'
                )

                tk.Label(
                    schedule_card,
                    text=text,
                    font=(theme.FONT, 11),
                    bg=theme.CARD,
                    fg=theme.TEXT
                ).pack(anchor="w", pady=7)

        else:
            tk.Label(
                schedule_card,
                text="No classes scheduled for today.",
                font=(theme.FONT, 11),
                bg=theme.CARD,
                fg=theme.MUTED
            ).pack(anchor="w", pady=7)

        # Quick overview
        overview = create_card(self)
        overview.pack(fill="x")

        tk.Label(
            overview,
            text="Quick Overview",
            font=(theme.FONT, 15, "bold"),
            bg=theme.CARD,
            fg=theme.TEXT
        ).pack(anchor="w", pady=(0, 10))

        tk.Label(
            overview,
            text=(
                "Manage your timetable, track attendance, "
                "organize assignments and monitor your academic "
                "performance from one place."
            ),
            font=(theme.FONT, 10),
            bg=theme.CARD,
            fg=theme.MUTED,
            wraplength=750,
            justify="left"
        ).pack(anchor="w")
