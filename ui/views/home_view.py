"""Home view: hero + search card + CV card + status."""
from tkinter import ttk
from ui.components.filters_panel import FiltersPanel
from ui.components.pdf_uploader import PdfUploader
from ui import theme as TH
from utils.i18n import t


class HomeView(ttk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, padding=14, **kwargs)
        self.app = app
        lang = app.lang
        hero = ttk.Frame(self, style="Card.TFrame", padding=16)
        hero.pack(fill="x", pady=(0, 12))
        ttk.Label(hero, text="💼 Workapp", style="CardTitle.TLabel",
                  font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ttk.Label(hero, text=t("tagline", lang),
                  style="CardMuted.TLabel").pack(anchor="w", pady=(2, 0))
        FiltersPanel(self, on_search=app.search_jobs, lang=lang).pack(fill="x")
        PdfUploader(self, on_analyzed=app.set_cv, lang=lang).pack(fill="x", pady=(12, 0))
        self.info = ttk.Label(self, text="", foreground=TH.PRIMARY,
                              font=("Segoe UI", 10, "bold"),
                              wraplength=660, justify="left")
        self.info.pack(anchor="w", pady=10)

    def set_info(self, text: str):
        self.info.config(text=text)
