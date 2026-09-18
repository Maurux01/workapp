"""Main Tk window: navigation + orchestration (search, match, spam)."""
import tkinter as tk
from tkinter import messagebox
from config import APP_NAME, DEFAULT_LANG, t
from core.job_matcher import JobMatcher
from core.spam_detector import SpamDetector
from scrapers.scraper_manager import ScraperManager
from ui.views.home_view import HomeView
from ui.views.result_view import ResultView
from ui.views.settings_view import SettingsView


class MainWindow(tk.Tk):
    def __init__(self, lang: str = DEFAULT_LANG):
        super().__init__()
        self.lang = lang
        self.title(f"{APP_NAME} — {t('app_tagline', lang)}")
        self.geometry("720x640")
        self.cv_data: dict | None = None
        self.jobs: list = []
        self.matcher = JobMatcher()
        self.spam = SpamDetector()
        self.scrapers = ScraperManager()

        nav = tk.Frame(self)
        nav.pack(fill="x")
        tk.Button(nav, text="Inicio / Home", command=lambda: self.show("home")).pack(side="left", padx=4, pady=4)
        tk.Button(nav, text="Resultados / Results", command=lambda: self.show("results")).pack(side="left", padx=4, pady=4)
        tk.Button(nav, text="Ajustes / Settings", command=lambda: self.show("settings")).pack(side="left", padx=4, pady=4)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=8, pady=4)
        self.views = {
            "home": HomeView(self.container, self),
            "results": ResultView(self.container, self),
            "settings": SettingsView(self.container, self),
        }
        self.show("home")

    def show(self, name: str):
        for v in self.views.values():
            v.pack_forget()
        self.views[name].pack(fill="both", expand=True)

    def set_cv(self, cv_data: dict):
        self.cv_data = cv_data
        n = len(cv_data.get("skills", []))
        self.views["home"].set_info(f"CV analizado: {n} skills — {', '.join(cv_data.get('skills', [])[:10])}")

    def set_lang(self, lang: str):
        self.lang = lang
        self.title(f"{APP_NAME} — {t('app_tagline', lang)}")

    def search_jobs(self, keyword: str, location: str, hide_spam: bool = True):
        if not keyword:
            messagebox.showwarning("Workapp", "Escribe una palabra clave / Type a keyword")
            return
        self.views["home"].set_info(f"Buscando '{keyword}' en {location}… / Searching…")
        self.update_idletasks()
        try:
            jobs = self.scrapers.search_all(keyword, location)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Workapp", str(exc))
            return
        # spam check
        for j in jobs:
            j["spam"] = self.spam.detect(j)
        if hide_spam:
            jobs = [j for j in jobs if not j["spam"].get("is_spam")]
        # match with CV if available
        if self.cv_data:
            jobs = self.matcher.rank(self.cv_data, jobs)
        self.jobs = jobs
        self.views["results"].show_jobs(jobs, lang=self.lang)
        self.views["home"].set_info(f"Encontradas {len(jobs)} ofertas / Found {len(jobs)} jobs")
        self.show("results")


def run():
    app = MainWindow()
    app.mainloop()
