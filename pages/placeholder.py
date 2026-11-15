import tkinter as tk
from ui import theme


class PlaceholderPage(tk.Frame):

    def __init__(self, parent, title):
        super().__init__(parent, bg=theme.BG)

        tk.Label(
            self,
            text=title,
            font=(theme.FONT, 24, "bold"),
            bg=theme.BG,
            fg=theme.TEXT
        ).pack(anchor="w", pady=20)

        tk.Label(
            self,
            text="This module is under development.",
            font=(theme.FONT, 12),
            bg=theme.BG,
            fg=theme.MUTED
        ).pack(anchor="w")