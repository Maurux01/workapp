"""Home view: filters + CV uploader + status."""
import tkinter as tk
from ui.components.filters_panel import FiltersPanel
from ui.components.pdf_uploader import PdfUploader


class HomeView(tk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        tk.Label(self, text="Workapp — La forma inteligente de conseguir trabajo / The smart way to get a job",
                 font=("Arial", 11, "bold"), wraplength=600, justify="left").pack(anchor="w", pady=8)
        FiltersPanel(self, on_search=app.search_jobs).pack(fill="x", pady=6)
        PdfUploader(self, on_analyzed=app.set_cv).pack(fill="x", pady=6)
        self.info = tk.Label(self, text="", fg="#333", wraplength=600, justify="left")
        self.info.pack(anchor="w", pady=6)

    def set_info(self, text: str):
        self.info.config(text=text)
