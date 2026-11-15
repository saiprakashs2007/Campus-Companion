
import tkinter as tk
from tkinter import ttk, messagebox

from ui import theme
from logic.attendance_logic import AttendanceManager


class AttendancePage(tk.Frame):

    def __init__(self, parent, manager=None):
        super().__init__(parent, bg=theme.BG)

        self.manager = manager if manager is not None else AttendanceManager()
        self.selected_subject = None

        self.create_page()
        self.refresh_table()

    def create_page(self):

        tk.Label(
            self,
            text="Attendance Manager",
            font=(theme.FONT, 24, "bold"),
            bg=theme.BG,
            fg=theme.TEXT
        ).pack(anchor="w", pady=(10, 5))

        tk.Label(
            self,
            text="Track your attendance and maintain the 75% requirement",
            font=(theme.FONT, 10),
            bg=theme.BG,
            fg=theme.MUTED
        ).pack(anchor="w", pady=(0, 20))

        # Input form
        form = tk.Frame(
            self,
            bg=theme.CARD,
            padx=15,
            pady=15
        )
        form.pack(fill="x", pady=(0, 20))

        self.entries = {}

        fields = [
            ("Subject Name", "subject"),
            ("Total Classes", "total"),
            ("Attended Classes", "attended")
        ]

        for column, (label, key) in enumerate(fields):

            tk.Label(
                form,
                text=label,
                bg=theme.CARD,
                fg=theme.TEXT
            ).grid(row=0, column=column, sticky="w", padx=5)

            entry = tk.Entry(
                form,
                width=22,
                bg=theme.BG,
                fg=theme.TEXT,
                insertbackground=theme.TEXT,
                relief="flat"
            )

            entry.grid(
                row=1,
                column=column,
                padx=5,
                pady=8,
                ipady=7
            )

            self.entries[key] = entry

        # Buttons
        buttons = tk.Frame(form, bg=theme.CARD)
        buttons.grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="w",
            pady=10
        )

        actions = [
            ("Add Subject", self.add_subject, theme.PRIMARY),
            ("Update", self.update_subject, theme.SUCCESS),
            ("Delete", self.delete_subject, theme.DANGER),
            ("Clear", self.clear_form, theme.CARD_HOVER)
        ]

        for text, command, color in actions:

            tk.Button(
                buttons,
                text=text,
                command=command,
                bg=color,
                fg="white",
                relief="flat",
                padx=15,
                pady=7
            ).pack(side="left", padx=5)

        # Attendance summary
        self.summary = tk.Frame(self, bg=theme.BG)
        self.summary.pack(fill="x", pady=(0, 15))

        # Table
        table_frame = tk.Frame(
            self,
            bg=theme.CARD,
            padx=15,
            pady=15
        )
        table_frame.pack(fill="both", expand=True)

        tk.Label(
            table_frame,
            text="Subject Attendance Records",
            font=(theme.FONT, 15, "bold"),
            bg=theme.CARD,
            fg=theme.TEXT
        ).pack(anchor="w", pady=(0, 12))

        columns = (
            "subject",
            "total",
            "attended",
            "percentage",
            "needed",
            "status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10
        )

        headings = {
            "subject": "Subject",
            "total": "Total Classes",
            "attended": "Attended",
            "percentage": "Attendance %",
            "needed": "Classes Needed",
            "status": "Status"
        }

        for column, heading in headings.items():

            self.tree.heading(column, text=heading)
            self.tree.column(
                column,
                width=115,
                anchor="center"
            )

        self.tree.pack(fill="both", expand=True)

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_subject
        )

    def add_subject(self):

        values = self.get_form_values()

        if not values:
            return

        subject, total, attended = values

        if any(
            item["subject"].lower() == subject.lower()
            for item in self.manager.get_all_subjects()
        ):
            messagebox.showerror(
                "Duplicate Subject",
                "This subject already exists."
            )
            return

        self.manager.add_subject(subject, total, attended)

        self.refresh_table()
        self.clear_form()

    def update_subject(self):

        if self.selected_subject is None:
            messagebox.showwarning(
                "Selection Required",
                "Select a subject to update."
            )
            return

        values = self.get_form_values()

        if not values:
            return

        subject, total, attended = values

        if subject.lower() != self.selected_subject.lower():
            if any(
                item["subject"].lower() == subject.lower()
                for item in self.manager.get_all_subjects()
            ):
                messagebox.showerror(
                    "Duplicate Subject",
                    "This subject already exists."
                )
                return

            self.manager.delete_subject(self.selected_subject)
            self.manager.add_subject(subject, total, attended)

        else:
            self.manager.update_attendance(
                self.selected_subject,
                total,
                attended
            )

        self.refresh_table()
        self.clear_form()

    def delete_subject(self):

        if self.selected_subject is None:
            messagebox.showwarning(
                "Selection Required",
                "Select a subject to delete."
            )
            return

        self.manager.delete_subject(self.selected_subject)

        self.refresh_table()
        self.clear_form()

    def get_form_values(self):

        subject = self.entries["subject"].get().strip()

        try:
            total = int(self.entries["total"].get())
            attended = int(self.entries["attended"].get())

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter valid whole numbers for classes."
            )
            return None

        if not subject:
            messagebox.showerror(
                "Missing Subject",
                "Enter a subject name."
            )
            return None

        if total < 0 or attended < 0:
            messagebox.showerror(
                "Invalid Input",
                "Class counts cannot be negative."
            )
            return None

        if attended > total:
            messagebox.showerror(
                "Invalid Input",
                "Attended classes cannot exceed total classes."
            )
            return None

        return subject, total, attended

    def refresh_table(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        subjects = self.manager.get_all_subjects()

        for index, item in enumerate(subjects):

            subject = item["subject"]

            percentage = self.manager.get_attendance_percentage(
                subject
            )

            needed = self.manager.get_classes_needed(subject)

            status = (
                "Safe" if percentage >= 75 else "Below 75%"
            )

            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    subject,
                    item["total_classes"],
                    item["attended_classes"],
                    f"{percentage:.2f}%",
                    needed,
                    status
                )
            )

        self.update_summary()

    def update_summary(self):

        for widget in self.summary.winfo_children():
            widget.destroy()

        subjects = self.manager.get_all_subjects()

        total_subjects = len(subjects)

        if total_subjects == 0:
            average = 0
        else:
            percentages = [
                self.manager.get_attendance_percentage(
                    item["subject"]
                )
                for item in subjects
            ]

            average = sum(percentages) / total_subjects

        cards = [
            ("Total Subjects", str(total_subjects)),
            ("Average Attendance", f"{average:.2f}%"),
            (
                "Below 75%",
                str(sum(
                    1 for item in subjects
                    if self.manager.get_attendance_percentage(
                        item["subject"]
                    ) < 75
                ))
            )
        ]

        for title, value in cards:

            card = tk.Frame(
                self.summary,
                bg=theme.CARD,
                padx=20,
                pady=15
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=(0, 12)
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
                font=(theme.FONT, 20, "bold"),
                bg=theme.CARD,
                fg=theme.TEXT
            ).pack(anchor="w", pady=(5, 0))

    def select_subject(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        index = int(selected[0])

        item = self.manager.get_all_subjects()[index]

        self.selected_subject = item["subject"]

        self.entries["subject"].delete(0, tk.END)
        self.entries["subject"].insert(0, item["subject"])

        self.entries["total"].delete(0, tk.END)
        self.entries["total"].insert(
            0,
            str(item["total_classes"])
        )

        self.entries["attended"].delete(0, tk.END)
        self.entries["attended"].insert(
            0,
            str(item["attended_classes"])
        )

    def clear_form(self):

        self.selected_subject = None

        for entry in self.entries.values():
            entry.delete(0, tk.END)

        for item in self.tree.selection():
            self.tree.selection_remove(item)
