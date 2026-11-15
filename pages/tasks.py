
import tkinter as tk
from tkinter import ttk, messagebox

from ui import theme
from logic.task_logic import TaskManager


class TasksPage(tk.Frame):

    def __init__(self, parent, manager=None):
        super().__init__(parent, bg=theme.BG)

        self.manager = manager if manager is not None else TaskManager()
        self.selected_index = None

        self.create_page()
        self.refresh_tasks()

    def create_page(self):

        tk.Label(
            self,
            text="Task Manager",
            font=(theme.FONT, 24, "bold"),
            bg=theme.BG,
            fg=theme.TEXT
        ).pack(anchor="w", pady=(10, 5))

        tk.Label(
            self,
            text="Organise assignments, exams and deadlines",
            font=(theme.FONT, 10),
            bg=theme.BG,
            fg=theme.MUTED
        ).pack(anchor="w", pady=(0, 20))

        # Task input form
        form = tk.Frame(self, bg=theme.CARD, padx=15, pady=15)
        form.pack(fill="x", pady=(0, 20))

        self.entries = {}

        fields = [
            ("Task Title", "title"),
            ("Subject", "subject"),
            ("Deadline", "deadline")
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

            entry.grid(row=1, column=column, padx=5, pady=8, ipady=7)

            self.entries[key] = entry

        # Priority selection
        tk.Label(
            form,
            text="Priority",
            bg=theme.CARD,
            fg=theme.TEXT
        ).grid(row=0, column=3, sticky="w", padx=5)

        self.priority_var = tk.StringVar(value="Medium")

        self.priority_box = ttk.Combobox(
            form,
            textvariable=self.priority_var,
            values=["High", "Medium", "Low"],
            state="readonly",
            width=15
        )

        self.priority_box.grid(row=1, column=3, padx=5, pady=8)

        # Action buttons
        buttons = tk.Frame(form, bg=theme.CARD)
        buttons.grid(row=2, column=0, columnspan=4, sticky="w", pady=10)

        actions = [
            ("Add Task", self.add_task, theme.PRIMARY),
            ("Update", self.update_task, theme.SUCCESS),
            ("Complete", self.complete_task, theme.SUCCESS),
            ("Delete", self.delete_task, theme.DANGER),
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
                padx=14,
                pady=7
            ).pack(side="left", padx=5)

        # Filter section
        filter_frame = tk.Frame(self, bg=theme.BG)
        filter_frame.pack(fill="x", pady=(0, 10))

        tk.Label(
            filter_frame,
            text="Filter Tasks:",
            font=(theme.FONT, 11, "bold"),
            bg=theme.BG,
            fg=theme.TEXT
        ).pack(side="left", padx=(0, 10))

        self.filter_var = tk.StringVar(value="All")

        self.filter_box = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=["All", "Pending", "Completed"],
            state="readonly",
            width=15
        )

        self.filter_box.pack(side="left")
        self.filter_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_tasks()
        )

        # Task table
        table_frame = tk.Frame(self, bg=theme.CARD, padx=15, pady=15)
        table_frame.pack(fill="both", expand=True)

        tk.Label(
            table_frame,
            text="Your Tasks",
            font=(theme.FONT, 15, "bold"),
            bg=theme.CARD,
            fg=theme.TEXT
        ).pack(anchor="w", pady=(0, 12))

        columns = ("title", "subject", "deadline", "priority", "status")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        headings = {
            "title": "Task",
            "subject": "Subject",
            "deadline": "Deadline",
            "priority": "Priority",
            "status": "Status"
        }

        for column, heading in headings.items():
            self.tree.heading(column, text=heading)
            self.tree.column(column, width=140, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.select_task)

    def add_task(self):

        values = self.get_form_values()

        if not values:
            return

        self.manager.add_task(*values)
        self.refresh_tasks()
        self.clear_form()

    def update_task(self):

        if self.selected_index is None:
            messagebox.showwarning(
                "Selection Required",
                "Please select a task to update."
            )
            return

        values = self.get_form_values()

        if not values:
            return

        self.manager.update_task(self.selected_index, *values)
        self.refresh_tasks()
        self.clear_form()

    def complete_task(self):

        if self.selected_index is None:
            messagebox.showwarning(
                "Selection Required",
                "Please select a task to complete."
            )
            return

        self.manager.complete_task(self.selected_index)
        self.refresh_tasks()
        self.clear_form()

    def delete_task(self):

        if self.selected_index is None:
            messagebox.showwarning(
                "Selection Required",
                "Please select a task to delete."
            )
            return

        self.manager.delete_task(self.selected_index)
        self.refresh_tasks()
        self.clear_form()

    def get_form_values(self):

        title = self.entries["title"].get().strip()
        subject = self.entries["subject"].get().strip()
        deadline = self.entries["deadline"].get().strip()
        priority = self.priority_var.get()

        if not title or not subject or not deadline:
            messagebox.showerror(
                "Missing Information",
                "Please fill in all the fields."
            )
            return None

        return title, subject, deadline, priority

    def refresh_tasks(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        tasks = self.manager.get_tasks(self.filter_var.get())

        for index, task in enumerate(self.manager.tasks):

            if task not in tasks:
                continue

            status = "Completed" if task["completed"] else "Pending"

            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    task["title"],
                    task["subject"],
                    task["deadline"],
                    task["priority"],
                    status
                )
            )

    def select_task(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        self.selected_index = int(selected[0])
        task = self.manager.tasks[self.selected_index]

        self.entries["title"].delete(0, tk.END)
        self.entries["title"].insert(0, task["title"])

        self.entries["subject"].delete(0, tk.END)
        self.entries["subject"].insert(0, task["subject"])

        self.entries["deadline"].delete(0, tk.END)
        self.entries["deadline"].insert(0, task["deadline"])

        self.priority_var.set(task["priority"])

    def clear_form(self):

        self.selected_index = None

        for entry in self.entries.values():
            entry.delete(0, tk.END)

        self.priority_var.set("Medium")

        for item in self.tree.selection():
            self.tree.selection_remove(item)
