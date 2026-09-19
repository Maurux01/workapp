"""Scrollable results list (themed, full-width cards)."""
import tkinter as tk
from tkinter import ttk
from ui import theme as TH
from ui.components.job_card import JobCard
from utils.i18n import t


class ResultView(ttk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, padding=10, **kwargs)
        self.app = app
        self.count = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.count,
                  font=("Segoe UI", 12, "bold"),
                  foreground=TH.PRIMARY).pack(anchor="w", pady=(0, 8))

        canvas = tk.Canvas(self, highlightthickness=0, background=TH.BG)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.inner = ttk.Frame(canvas)
        self.inner.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self._win = canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(self._win, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas = canvas
        self.refresh_count([])

    def refresh_count(self, jobs: list):
        lang = self.app.lang
        self.count.set(f"📋 {t('results_for', lang)}: {len(jobs)}")

    def show_jobs(self, jobs: list, lang: str = "es"):
        for w in self.inner.winfo_children():
            w.destroy()
        self.refresh_count(jobs)
        if not jobs:
            ttk.Label(self.inner, text="🔍 " + t("no_results", lang),
                      style="Muted.TLabel").pack(pady=24)
        for job in jobs:
            JobCard(self.inner, job, lang=lang).pack(fill="x", padx=2, pady=6)
        self.canvas.yview_moveto(0)
