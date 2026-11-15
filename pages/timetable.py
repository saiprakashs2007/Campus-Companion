
import tkinter as tk
from tkinter import ttk, messagebox

from ui import theme
from logic.timetable_logic import TimetableManager


class TimetablePage(tk.Frame):

    def __init__(self, parent, manager=None):
        super().__init__(parent, bg=theme.BG)

        self.manager = manager if manager is not None else TimetableManager()
        self.selected_index = None

        self.create_page()
        self.refresh_table()

    def create_page(self):

        tk.Label(
            self,
            text="Weekly Timetable",
            font=(theme.FONT, 24, "bold"),
            bg=theme.BG,
            fg=theme.TEXT
        ).pack(anchor="w", pady=(10, 5))

        tk.Label(
            self,
            text="Manage your weekly class schedule",
            font=(theme.FONT, 10),
            bg=theme.BG,
            fg=theme.MUTED
        ).pack(anchor="w", pady=(0, 20))

        # Input section
        form = tk.Frame(self, bg=theme.CARD, padx=15, pady=15)
        form.pack(fill="x", pady=(0, 20))

        tk.Label(
            form, text="Day", bg=theme.CARD, fg=theme.TEXT
        ).grid(row=0, column=0, sticky="w", padx=5)

        self.day_var = tk.StringVar(value="Monday")

        self.day_box = ttk.Combobox(
            form,
            textvariable=self.day_var,
            values=["Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday"],
            state="readonly",
            width=15
        )
        self.day_box.grid(row=1, column=0, padx=5, pady=8)

        fields = [
            ("Subject", "subject"),
            ("Start Time", "start"),
            ("End Time", "end"),
            ("Room", "room")
        ]

        self.entries = {}

        for column, (label, key) in enumerate(fields, start=1):

            tk.Label(
                form,
                text=label,
                bg=theme.CARD,
                fg=theme.TEXT
            ).grid(row=0, column=column, sticky="w", padx=5)

            entry = tk.Entry(
                form,
                width=16,
                bg=theme.BG,
                fg=theme.TEXT,
                insertbackground=theme.TEXT,
                relief="flat"
            )

            entry.grid(row=1, column=column, padx=5, pady=8, ipady=7)

            self.entries[key] = entry

        # Buttons
        buttons = tk.Frame(form, bg=theme.CARD)
        buttons.grid(row=2, column=0, columnspan=5, sticky="w", pady=10)

        tk.Button(
            buttons,
            text="Add Class",
            command=self.add_class,
            bg=theme.PRIMARY,
            fg="white",
            relief="flat",
            padx=15,
            pady=7
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Update Class",
            command=self.update_class,
            bg=theme.SUCCESS,
            fg="white",
            relief="flat",
            padx=15,
            pady=7
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Delete Class",
            command=self.delete_class,
            bg=theme.DANGER,
            fg="white",
            relief="flat",
            padx=15,
            pady=7
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Clear",
            command=self.clear_form,
            bg=theme.CARD_HOVER,
            fg=theme.TEXT,
            relief="flat",
            padx=15,
            pady=7
        ).pack(side="left", padx=5)

        # Table section
        table_frame = tk.Frame(self, bg=theme.CARD, padx=15, pady=15)
        table_frame.pack(fill="both", expand=True)

        tk.Label(
            table_frame,
            text="Your Classes",
            font=(theme.FONT, 15, "bold"),
            bg=theme.CARD,
            fg=theme.TEXT
        ).pack(anchor="w", pady=(0, 12))

        columns = ("day", "subject", "start", "end", "room")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        headings = {
            "day": "Day",
            "subject": "Subject",
            "start": "Start Time",
            "end": "End Time",
            "room": "Room"
        }

        for column, heading in headings.items():
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=130, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.select_class)

    def add_class(self):

        values = self.get_form_values()

        if not values:
            return

        self.manager.add_class(*values)
        self.refresh_table()
        self.clear_form()

    def update_class(self):

        if self.selected_index is None:
            messagebox.showwarning(
                "Selection Required",
                "Please select a class to update."
            )
            return

        values = self.get_form_values()

        if not values:
            return

        self.manager.update_class(self.selected_index, *values)
        self.refresh_table()
        self.clear_form()

    def delete_class(self):

        if self.selected_index is None:
            messagebox.showwarning(
                "Selection Required",
                "Please select a class to delete."
            )
            return

        self.manager.delete_class(self.selected_index)
        self.refresh_table()
        self.clear_form()

    def get_form_values(self):

        day = self.day_var.get()
        subject = self.entries["subject"].get().strip()
        start = self.entries["start"].get().strip()
        end = self.entries["end"].get().strip()
        room = self.entries["room"].get().strip()

        if not subject or not start or not end or not room:
            messagebox.showerror(
                "Missing Information",
                "Please fill in all the fields."
            )
            return None

        return day, subject, start, end, room

    def refresh_table(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, cls in enumerate(self.manager.get_classes()):
            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    cls["day"],
                    cls["subject"],
                    cls["start_time"],
                    cls["end_time"],
                    cls["room"]
                )
            )

    def select_class(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        self.selected_index = int(selected[0])
        cls = self.manager.classes[self.selected_index]

        self.day_var.set(cls["day"])

        self.entries["subject"].delete(0, tk.END)
        self.entries["subject"].insert(0, cls["subject"])

        self.entries["start"].delete(0, tk.END)
        self.entries["start"].insert(0, cls["start_time"])

        self.entries["end"].delete(0, tk.END)
        self.entries["end"].insert(0, cls["end_time"])

        self.entries["room"].delete(0, tk.END)
        self.entries["room"].insert(0, cls["room"])

    def clear_form(self):

        self.selected_index = None
        self.day_var.set("Monday")

        for entry in self.entries.values():
            entry.delete(0, tk.END)

        for item in self.tree.selection():
            self.tree.selection_remove(item)
