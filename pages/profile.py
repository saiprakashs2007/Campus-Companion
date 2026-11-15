
import tkinter as tk
from tkinter import messagebox

from ui import theme


# Temporary in-memory profile storage
PROFILE_DATA = {
    "name": "",
    "roll_number": "",
    "department": "",
    "program": "",
    "year": "",
    "section": "",
    "email": ""
}


class ProfilePage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=theme.BG)

        self.entries = {}

        self.create_page()
        self.load_profile()

    def create_page(self):

        tk.Label(
            self,
            text="Student Profile",
            font=(theme.FONT, 24, "bold"),
            bg=theme.BG,
            fg=theme.TEXT
        ).pack(anchor="w", pady=(10, 5))

        tk.Label(
            self,
            text="Manage your personal and academic information",
            font=(theme.FONT, 10),
            bg=theme.BG,
            fg=theme.MUTED
        ).pack(anchor="w", pady=(0, 25))

        # Profile card
        card = tk.Frame(
            self,
            bg=theme.CARD,
            padx=30,
            pady=25
        )
        card.pack(fill="x", pady=(0, 20))

        tk.Label(
            card,
            text="Personal Information",
            font=(theme.FONT, 16, "bold"),
            bg=theme.CARD,
            fg=theme.TEXT
        ).grid(row=0, column=0, columnspan=2,
               sticky="w", pady=(0, 20))

        fields = [
            ("Full Name", "name"),
            ("Roll Number", "roll_number"),
            ("Department", "department"),
            ("Program", "program"),
            ("Academic Year", "year"),
            ("Section", "section"),
            ("Email Address", "email")
        ]

        for index, (label, key) in enumerate(fields):

            row = (index // 2) + 1
            column = (index % 2) * 2

            tk.Label(
                card,
                text=label,
                font=(theme.FONT, 10),
                bg=theme.CARD,
                fg=theme.MUTED
            ).grid(
                row=row * 2 - 1,
                column=column,
                sticky="w",
                padx=10,
                pady=(12, 4)
            )

            entry = tk.Entry(
                card,
                width=28,
                font=(theme.FONT, 11),
                bg=theme.BG,
                fg=theme.TEXT,
                insertbackground=theme.TEXT,
                relief="flat"
            )

            entry.grid(
                row=row * 2,
                column=column,
                columnspan=2,
                sticky="ew",
                padx=10,
                pady=(0, 5),
                ipady=8
            )

            self.entries[key] = entry

        card.grid_columnconfigure(1, weight=1)
        card.grid_columnconfigure(3, weight=1)

        # Save button
        tk.Button(
            self,
            text="Save Profile",
            command=self.save_profile,
            font=(theme.FONT, 11, "bold"),
            bg=theme.PRIMARY,
            fg="white",
            activebackground=theme.PRIMARY,
            relief="flat",
            padx=25,
            pady=10,
            cursor="hand2"
        ).pack(anchor="w", pady=10)

        # Information message
        tk.Label(
            self,
            text="Your profile details are stored temporarily and reset when the application closes.",
            font=(theme.FONT, 9),
            bg=theme.BG,
            fg=theme.MUTED
        ).pack(anchor="w", pady=10)

    def load_profile(self):

        for key, entry in self.entries.items():

            entry.delete(0, tk.END)
            entry.insert(0, PROFILE_DATA[key])

    def save_profile(self):

        name = self.entries["name"].get().strip()

        if not name:
            messagebox.showerror(
                "Missing Information",
                "Please enter your full name."
            )
            return

        for key, entry in self.entries.items():
            PROFILE_DATA[key] = entry.get().strip()

        messagebox.showinfo(
            "Profile Saved",
            "Your profile has been updated successfully!"
        )
