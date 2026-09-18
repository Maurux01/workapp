"""Scrollable results list."""
import tkinter as tk
from tkinter import ttk
from ui.components.job_card import JobCard
from utils.i18n import t


class ResultView(ttk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, padding=8, **kwargs)
        self.app = app
        self.count = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.count,
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 6))

        canvas = tk.Canvas(self, highlightthickness=0, background="#f8fafc")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.inner = ttk.Frame(canvas)
        self.inner.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas = canvas
        self.refresh_count([])

    def refresh_count(self, jobs: list):
        lang = self.app.lang
        self.count.set(f"{t('results_for', lang)}: {len(jobs)}")

    def show_jobs(self, jobs: list, lang: str = "es"):
        for w in self.inner.winfo_children():
            w.destroy()
        self.refresh_count(jobs)
        if not jobs:
            ttk.Label(self.inner, text=t("no_results", lang),
                      foreground="#64748b").pack(pady=20)
        for job in jobs:
            JobCard(self.inner, job, lang=lang).pack(fill="x", padx=4, pady=5)
        self.canvas.yview_moveto(0)
