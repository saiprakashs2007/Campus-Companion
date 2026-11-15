
import tkinter as tk
from tkinter import ttk, messagebox

from ui import theme
from logic.cgpa_logic import CgpaManager


class CgpaPage(tk.Frame):

    def __init__(self, parent, manager=None):
        super().__init__(parent, bg=theme.BG)

        self.manager = manager if manager is not None else CgpaManager()
        self.selected_index = None
        self.semester_records = []

        self.create_page()
        self.refresh_table()

    def create_page(self):

        tk.Label(
            self,
            text="CGPA Calculator",
            font=(theme.FONT, 24, "bold"),
            bg=theme.BG,
            fg=theme.TEXT
        ).pack(anchor="w", pady=(10, 5))

        tk.Label(
            self,
            text="Calculate your SGPA and cumulative CGPA",
            font=(theme.FONT, 10),
            bg=theme.BG,
            fg=theme.MUTED
        ).pack(anchor="w", pady=(0, 20))

        # Subject input form
        form = tk.Frame(
            self,
            bg=theme.CARD,
            padx=15,
            pady=15
        )
        form.pack(fill="x", pady=(0, 15))

        self.entries = {}

        fields = [
            ("Subject Name", "subject"),
            ("Credits", "credits")
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

        # Grade point selection
        tk.Label(
            form,
            text="Grade Point",
            bg=theme.CARD,
            fg=theme.TEXT
        ).grid(row=0, column=2, sticky="w", padx=5)

        self.grade_var = tk.StringVar(value="10")

        self.grade_box = ttk.Combobox(
            form,
            textvariable=self.grade_var,
            values=[str(i) for i in range(11)],
            state="readonly",
            width=18
        )

        self.grade_box.grid(row=1, column=2, padx=5, pady=8)

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

        # Subject table
        table_frame = tk.Frame(
            self,
            bg=theme.CARD,
            padx=15,
            pady=15
        )
        table_frame.pack(fill="both", expand=True, pady=(0, 15))

        tk.Label(
            table_frame,
            text="Subject Records",
            font=(theme.FONT, 15, "bold"),
            bg=theme.CARD,
            fg=theme.TEXT
        ).pack(anchor="w", pady=(0, 10))

        columns = ("subject", "credits", "grade", "points")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=6
        )

        headings = {
            "subject": "Subject",
            "credits": "Credits",
            "grade": "Grade Point",
            "points": "Credit × Grade"
        }

        for column, heading in headings.items():
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=150, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_subject
        )

        # SGPA display
        self.sgpa_label = tk.Label(
            self,
            text="Current SGPA: 0.00",
            font=(theme.FONT, 18, "bold"),
            bg=theme.CARD,
            fg=theme.SUCCESS,
            padx=15,
            pady=12
        )

        self.sgpa_label.pack(fill="x", pady=(0, 15))

        # Previous semester CGPA section
        cgpa_frame = tk.Frame(
            self,
            bg=theme.CARD,
            padx=15,
            pady=15
        )
        cgpa_frame.pack(fill="x")

        tk.Label(
            cgpa_frame,
            text="Cumulative CGPA",
            font=(theme.FONT, 15, "bold"),
            bg=theme.CARD,
            fg=theme.TEXT
        ).pack(anchor="w", pady=(0, 10))

        input_frame = tk.Frame(cgpa_frame, bg=theme.CARD)
        input_frame.pack(fill="x")

        tk.Label(
            input_frame,
            text="Previous Semester SGPA:",
            bg=theme.CARD,
            fg=theme.TEXT
        ).pack(side="left")

        self.previous_sgpa = tk.Entry(
            input_frame,
            width=10,
            bg=theme.BG,
            fg=theme.TEXT,
            insertbackground=theme.TEXT,
            relief="flat"
        )
        self.previous_sgpa.pack(side="left", padx=8, ipady=5)

        tk.Label(
            input_frame,
            text="Total Credits:",
            bg=theme.CARD,
            fg=theme.TEXT
        ).pack(side="left", padx=(15, 0))

        self.previous_credits = tk.Entry(
            input_frame,
            width=10,
            bg=theme.BG,
            fg=theme.TEXT,
            insertbackground=theme.TEXT,
            relief="flat"
        )
        self.previous_credits.pack(side="left", padx=8, ipady=5)

        tk.Button(
            cgpa_frame,
            text="Calculate CGPA",
            command=self.calculate_cgpa,
            bg=theme.PRIMARY,
            fg="white",
            relief="flat",
            padx=15,
            pady=7
        ).pack(anchor="w", pady=12)

        self.cgpa_label = tk.Label(
            cgpa_frame,
            text="Cumulative CGPA: 0.00",
            font=(theme.FONT, 17, "bold"),
            bg=theme.CARD,
            fg=theme.SUCCESS
        )

        self.cgpa_label.pack(anchor="w")

    def get_form_values(self):

        subject = self.entries["subject"].get().strip()

        try:
            credits = float(self.entries["credits"].get())
            grade = float(self.grade_var.get())

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter valid credits and grade points."
            )
            return None

        if not subject:
            messagebox.showerror(
                "Missing Information",
                "Enter a subject name."
            )
            return None

        if credits <= 0 or grade < 0 or grade > 10:
            messagebox.showerror(
                "Invalid Input",
                "Credits must be positive and grade point must be 0–10."
            )
            return None

        return subject, credits, grade

    def add_subject(self):

        values = self.get_form_values()

        if not values:
            return

        subject = values[0]

        if any(
            item["subject"].lower() == subject.lower()
            for item in self.manager.get_subjects()
        ):
            messagebox.showerror(
                "Duplicate Subject",
                "This subject already exists."
            )
            return

        self.manager.add_subject(*values)
        self.refresh_table()
        self.clear_form()

    def update_subject(self):

        if self.selected_index is None:
            messagebox.showwarning(
                "Selection Required",
                "Select a subject to update."
            )
            return

        values = self.get_form_values()

        if not values:
            return

        subject = values[0]

        if any(
            i != self.selected_index
            and item["subject"].lower() == subject.lower()
            for i, item in enumerate(self.manager.get_subjects())
        ):
            messagebox.showerror(
                "Duplicate Subject",
                "This subject already exists."
            )
            return

        self.manager.update_subject(
            self.selected_index,
            *values
        )

        self.refresh_table()
        self.clear_form()

    def delete_subject(self):

        if self.selected_index is None:
            messagebox.showwarning(
                "Selection Required",
                "Select a subject to delete."
            )
            return

        self.manager.delete_subject(self.selected_index)

        self.refresh_table()
        self.clear_form()

    def refresh_table(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, subject in enumerate(self.manager.get_subjects()):

            credits = subject["credits"]
            grade = subject["grade_point"]
            points = credits * grade

            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    subject["subject"],
                    credits,
                    grade,
                    f"{points:.2f}"
                )
            )

        sgpa = self.manager.calculate_sgpa()

        self.sgpa_label.config(
            text=f"Current SGPA: {sgpa:.2f}"
        )

    def select_subject(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        self.selected_index = int(selected[0])

        subject = self.manager.get_subjects()[self.selected_index]

        self.entries["subject"].delete(0, tk.END)
        self.entries["subject"].insert(0, subject["subject"])

        self.entries["credits"].delete(0, tk.END)
        self.entries["credits"].insert(0, str(subject["credits"]))

        self.grade_var.set(str(subject["grade_point"]))

    def clear_form(self):

        self.selected_index = None

        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.grade_var.set("10")

        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def calculate_cgpa(self):

        try:
            previous_sgpa = float(self.previous_sgpa.get())
            previous_credits = float(self.previous_credits.get())

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter valid previous SGPA and credits."
            )
            return

        if not (0 <= previous_sgpa <= 10) or previous_credits < 0:
            messagebox.showerror(
                "Invalid Input",
                "SGPA must be 0–10 and credits cannot be negative."
            )
            return

        current_credits = sum(
            item["credits"] for item in self.manager.get_subjects()
        )

        if current_credits == 0:
            messagebox.showwarning(
                "No Current Subjects",
                "Add subjects before calculating CGPA."
            )
            return

        current_sgpa = self.manager.calculate_sgpa()

        semester_data = [
            (previous_sgpa, previous_credits),
            (current_sgpa, current_credits)
        ]

        cgpa = self.manager.calculate_cgpa(semester_data)

        self.cgpa_label.config(
            text=f"Cumulative CGPA: {cgpa:.2f}"
        )
