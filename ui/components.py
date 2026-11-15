
import tkinter as tk
from tkinter import ttk
from ui import theme


def create_card(parent, bg=None, padx=15, pady=15):
    card = tk.Frame(
        parent,
        bg=bg or theme.CARD,
        padx=padx,
        pady=pady,
        highlightbackground=theme.BORDER,
        highlightthickness=1
    )
    return card


def create_heading(parent, title, subtitle=None):
    heading_frame = tk.Frame(parent, bg=theme.BG)

    tk.Label(
        heading_frame,
        text=title,
        font=(theme.FONT, 24, "bold"),
        bg=theme.BG,
        fg=theme.TEXT
    ).pack(anchor="w")

    if subtitle:
        tk.Label(
            heading_frame,
            text=subtitle,
            font=(theme.FONT, 10),
            bg=theme.BG,
            fg=theme.MUTED
        ).pack(anchor="w", pady=(5, 0))

    return heading_frame


def create_stat_card(parent, title, value, color=None):
    card = create_card(parent)

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
        fg=color or theme.TEXT
    ).pack(anchor="w", pady=(8, 0))

    return card


def configure_table_styles(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background="#151D2D",
        foreground="#F1F3F9",
        fieldbackground="#151D2D",
        rowheight=36,
        font=("Segoe UI", 10),
        borderwidth=1,
        relief="solid"
    )

    style.configure(
        "Treeview.Heading",
        background="#6657D9",
        foreground="white",
        font=("Segoe UI", 10, "bold"),
        padding=(10, 12),
        relief="flat"
    )

    style.map(
        "Treeview.Heading",
        background=[("active", "#7C6CF2")]
    )

    style.map(
        "Treeview",
        background=[("selected", "#3B4770")],
        foreground=[("selected", "#FFFFFF")]
    )

    style.configure(
        "TCombobox",
        fieldbackground="#1A2233",
        background="#252F45",
        foreground="#F1F3F9",
        arrowcolor="#F1F3F9",
        padding=7
    )

    style.map(
        "TCombobox",
        fieldbackground=[("readonly", "#1A2233")],
        foreground=[("readonly", "#F1F3F9")]
    )
