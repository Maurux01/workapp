"""Shared modern theme for the desktop app: colors, fonts, ttk styles."""
from tkinter import ttk

PRIMARY = "#4f46e5"      # indigo-600
PRIMARY_DARK = "#312e81"  # indigo-900 (header)
PRIMARY_SOFT = "#eef2ff"  # indigo-50
BG = "#f4f4f6"
CARD = "#ffffff"
INK = "#18181b"
MUTED = "#71717a"
LINE = "#e4e4e7"
SUCCESS_BG = "#dcfce7"
SUCCESS_FG = "#166534"
DANGER_BG = "#fee2e2"
DANGER_FG = "#991b1b"
GOLD_BG = "#fef3c7"
GOLD_FG = "#92400e"

TITLE_FONT = ("Segoe UI", 15, "bold")
SUBTITLE_FONT = ("Segoe UI", 10)
SECTION_FONT = ("Segoe UI", 11, "bold")
BODY_FONT = ("Segoe UI", 10)
SMALL_FONT = ("Segoe UI", 9)


def apply(root) -> None:
    """Apply the Workapp theme to a Tk root (idempotent)."""
    style = ttk.Style(root)
    for theme in ("clam", "vista", "xpnative", "default"):
        if theme in style.theme_names():
            style.theme_use(theme)
            break
    root.configure(background=BG)
    style.configure("TFrame", background=BG)
    style.configure("Card.TFrame", background=CARD)
    style.configure("Header.TFrame", background=PRIMARY_DARK)
    style.configure("Header.TLabel", background=PRIMARY_DARK, foreground="white",
                    font=BODY_FONT)
    style.configure("HeaderTitle.TLabel", background=PRIMARY_DARK,
                    foreground="white", font=TITLE_FONT)
    style.configure("HeaderSub.TLabel", background=PRIMARY_DARK,
                    foreground="#c7d2fe", font=SUBTITLE_FONT)
    style.configure("Title.TLabel", background=BG, foreground=INK, font=TITLE_FONT)
    style.configure("Section.TLabel", background=BG, foreground=INK, font=SECTION_FONT)
    style.configure("Muted.TLabel", background=BG, foreground=MUTED, font=SMALL_FONT)
    style.configure("CardMuted.TLabel", background=CARD, foreground=MUTED, font=SMALL_FONT)
    style.configure("CardBody.TLabel", background=CARD, foreground="#3f3f46", font=BODY_FONT)
    style.configure("CardTitle.TLabel", background=CARD, foreground=INK,
                    font=("Segoe UI", 11, "bold"))
    style.configure("TLabel", background=BG, font=BODY_FONT)
    style.configure("TCheckbutton", background=BG, font=BODY_FONT)
    style.configure("TLabelframe", background=BG, bordercolor=LINE)
    style.configure("TLabelframe.Label", background=BG, foreground=PRIMARY,
                    font=("Segoe UI", 10, "bold"))
    style.configure("Accent.TButton", background=PRIMARY, foreground="white",
                    font=("Segoe UI", 10, "bold"), padding=(18, 8), borderwidth=0)
    style.map("Accent.TButton", background=[("active", "#4338ca")])
    style.configure("Ghost.TButton", background=CARD, foreground=PRIMARY,
                    font=BODY_FONT, padding=(10, 5))
    style.configure("TEntry", padding=6)
    style.configure("TScrollbar", background=BG)
