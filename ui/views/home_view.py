"""Home view: filters + CV uploader + status."""
import tkinter as tk
from tkinter import ttk
from config import APP_NAME
from ui.components.filters_panel import FiltersPanel
from ui.components.pdf_uploader import PdfUploader
from utils.i18n import t


class HomeView(ttk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, padding=12, **kwargs)
        self.app = app
        lang = app.lang
        ttk.Label(self, text=APP_NAME, font=("Segoe UI", 16, "bold"),
                  foreground="#1d4ed8").pack(anchor="w")
        ttk.Label(self, text=t("tagline", lang),
                  foreground="#475569").pack(anchor="w", pady=(0, 8))
        FiltersPanel(self, on_search=app.search_jobs, lang=lang).pack(fill="x", pady=4)
        ttk.Separator(self).pack(fill="x", pady=8)
        PdfUploader(self, on_analyzed=app.set_cv, lang=lang).pack(fill="x", pady=4)
        self.info = ttk.Label(self, text="", foreground="#334155",
                              wraplength=640, justify="left")
        self.info.pack(anchor="w", pady=8)

    def set_info(self, text: str):
        self.info.config(text=text)
