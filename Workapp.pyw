# Workapp — DOBLE CLIC AQUI. No abre terminal (usa pythonw).
# DOUBLE-CLICK THIS. No console window (runs under pythonw).
import os
import sys
import traceback

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

MISSING = []
for _mod in ("flask", "requests", "bs4", "lxml", "pypdf", "dotenv"):
    try:
        __import__(_mod)
    except ImportError:
        MISSING.append(_mod)

if MISSING:
    import tkinter as tk
    from tkinter import messagebox
    _r = tk.Tk()
    _r.withdraw()
    messagebox.showerror(
        "Workapp",
        "Faltan dependencias:\n" + ", ".join(MISSING)
        + "\n\nAbre Workapp.bat una vez para instalarlas.\n"
        + "Missing packages — run Workapp.bat once to install them.",
    )
    _r.destroy()
    sys.exit(1)


def _log_crash(text):
    try:
        with open("Workapp-error.log", "a", encoding="utf-8") as _fh:
            _fh.write(text + "\n")
    except OSError:
        pass


try:
    from ui.main_window import MainWindow
    MainWindow().mainloop()
except Exception:  # noqa: BLE001
    _log_crash(traceback.format_exc())
    raise
