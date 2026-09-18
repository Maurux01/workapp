"""Scrollable results list."""
import tkinter as tk
from ui.components.job_card import JobCard


class ResultView(tk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self.count = tk.StringVar(value="Resultados / Results: 0")
        tk.Label(self, textvariable=self.count, font=("Arial", 10, "bold")).pack(anchor="w")

        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.inner = tk.Frame(canvas)
        self.inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas = canvas

    def show_jobs(self, jobs: list, lang: str = "es"):
        for w in self.inner.winfo_children():
            w.destroy()
        self.count.set(f"Resultados / Results: {len(jobs)}")
        for job in jobs:
            JobCard(self.inner, job, lang=lang).pack(fill="x", padx=4, pady=4)
        self.canvas.yview_moveto(0)
