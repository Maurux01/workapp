"""Shared modern theme: light/dark palettes + ttk styles. Rebuild views on switch."""
import json
import os
from tkinter import ttk

PALETTES = {
    "light": {
        "PRIMARY": "#4f46e5", "PRIMARY_DARK": "#312e81", "PRIMARY_SOFT": "#eef2ff",
        "BG": "#f4f4f6", "CARD": "#ffffff", "INK": "#18181b", "MUTED": "#71717a",
        "LINE": "#e4e4e7", "SUCCESS_BG": "#dcfce7", "SUCCESS_FG": "#166534",
        "DANGER_BG": "#fee2e2", "DANGER_FG": "#991b1b",
    },
    "dark": {
        "PRIMARY": "#818cf8", "PRIMARY_DARK": "#1e1b4b", "PRIMARY_SOFT": "#312e81",
        "BG": "#09090b", "CARD": "#18181b", "INK": "#f4f4f5", "MUTED": "#a1a1aa",
        "LINE": "#27272a", "SUCCESS_BG": "#14532d", "SUCCESS_FG": "#bbf7d0",
        "DANGER_BG": "#7f1d1d", "DANGER_FG": "#fecaca",
    },
}

MODE = "light"

TITLE_FONT = ("Segoe UI", 15, "bold")
SUBTITLE_FONT = ("Segoe UI", 10)
SECTION_FONT = ("Segoe UI", 11, "bold")
BODY_FONT = ("Segoe UI", 10)
SMALL_FONT = ("Segoe UI", 9)


def _conf_path() -> str:
    try:
        from config import CACHE_DIR
        return os.path.join(str(CACHE_DIR), ".theme.json")
    except Exception:  # noqa: BLE001
        return os.path.join("data", "cache", ".theme.json")


def load_mode() -> str:
    """Persisted choice wins; fresh installs default to dark."""
    try:
        with open(_conf_path(), encoding="utf-8") as fh:
            mode = json.load(fh).get("mode", "dark")
            return mode if mode in PALETTES else "dark"
    except (OSError, ValueError):
        return "dark"


def save_mode(mode: str) -> None:
    try:
        os.makedirs(os.path.dirname(_conf_path()), exist_ok=True)
        with open(_conf_path(), "w", encoding="utf-8") as fh:
            json.dump({"mode": mode}, fh)
    except OSError:
        pass


def set_mode(mode: str) -> None:
    global MODE
    MODE = mode if mode in PALETTES else "light"
    for key, value in PALETTES[MODE].items():
        globals()[key] = value
    save_mode(MODE)


# Expose current palette as module constants (refreshed by set_mode).
set_mode(load_mode())


def apply(root) -> None:
    """Apply the Workapp theme to a Tk root (idempotent)."""
    style = ttk.Style(root)
    # clam first: it honors custom colors in BOTH modes.
    # vista/xpnative draw native controls and ignore dark backgrounds.
    for theme in ("clam", "vista", "xpnative", "default"):
        if theme in style.theme_names():
            style.theme_use(theme)
            break
    is_dark = MODE == "dark"
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
    style.configure("Header.TButton", background="#4338ca", foreground="white",
                    font=BODY_FONT, padding=(10, 4), borderwidth=0)
    style.map("Header.TButton", background=[("active", "#4f46e5")])
    style.configure("Title.TLabel", background=BG, foreground=INK, font=TITLE_FONT)
    style.configure("Section.TLabel", background=BG, foreground=INK, font=SECTION_FONT)
    style.configure("Muted.TLabel", background=BG, foreground=MUTED, font=SMALL_FONT)
    style.configure("CardMuted.TLabel", background=CARD, foreground=MUTED, font=SMALL_FONT)
    style.configure("CardBody.TLabel", background=CARD, foreground=INK, font=BODY_FONT)
    style.configure("CardTitle.TLabel", background=CARD, foreground=INK,
                    font=("Segoe UI", 11, "bold"))
    style.configure("TLabel", background=BG, foreground=INK, font=BODY_FONT)
    style.configure("TCheckbutton", background=BG, foreground=INK, font=BODY_FONT)
    style.map("TCheckbutton", background=[("active", BG)], foreground=[("active", INK)])
    style.configure("TLabelframe", background=BG, bordercolor=LINE)
    style.configure("TLabelframe.Label", background=BG, foreground=PRIMARY,
                    font=("Segoe UI", 10, "bold"))
    style.configure("Accent.TButton", background=PALETTES["light"]["PRIMARY"],
                    foreground="white", font=("Segoe UI", 10, "bold"),
                    padding=(18, 8), borderwidth=0)
    style.map("Accent.TButton", background=[("active", "#4338ca")])
    style.configure("Ghost.TButton", background=CARD, foreground=PRIMARY,
                    font=BODY_FONT, padding=(10, 5), borderwidth=1,
                    relief="solid")
    style.map("Ghost.TButton", background=[("active", PRIMARY_SOFT)])
    style.configure("TEntry", padding=6, fieldbackground=CARD, foreground=INK,
                    bordercolor=LINE, lightcolor=PRIMARY, darkcolor=LINE)
    style.configure("TCombobox", fieldbackground=CARD, foreground=INK,
                    background=CARD, arrowcolor=PRIMARY)
    style.map("TCombobox",
              fieldbackground=[("readonly", CARD)],
              foreground=[("readonly", INK)])
    style.configure("TScrollbar", background=BG, troughcolor=BG, bordercolor=BG)
    style.configure("TProgressbar", background=PRIMARY, troughcolor=LINE,
                    borderwidth=0, thickness=10)
    style.configure("Match.Horizontal.TProgressbar", background=PRIMARY,
                    troughcolor=LINE, borderwidth=0, thickness=8)
    if is_dark:
        style.configure("TSeparator", background=LINE)
