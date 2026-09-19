"""Main window: indigo header, pill nav, status bar, full ES/EN rebuild."""
import tkinter as tk
from tkinter import ttk, messagebox
from config import APP_NAME, DEFAULT_LANG, DEFAULT_LOCATION
from core.job_matcher import JobMatcher
from core.spam_detector import SpamDetector
from scrapers.scraper_manager import ScraperManager
from ui import theme as TH
from ui.views.home_view import HomeView
from ui.views.result_view import ResultView
from ui.views.settings_view import SettingsView
from utils.i18n import t


class MainWindow(tk.Tk):
    def __init__(self, lang: str = DEFAULT_LANG):
        super().__init__()
        self.lang = lang if lang in ("es", "en") else "es"
        self.cv_data: dict | None = None
        self.jobs: list = []
        self.matcher = JobMatcher()
        self.spam = SpamDetector()
        self.scrapers = ScraperManager()
        TH.apply(self)
        self.geometry("820x700")
        self.minsize(700, 580)
        self._build_chrome()
        self._build_views()
        self._apply_title()

    def _build_chrome(self):
        header = ttk.Frame(self, style="Header.TFrame", padding=(16, 14))
        header.pack(fill="x")
        txt = ttk.Frame(header, style="Header.TFrame")
        txt.pack(side="left")
        self.title_lbl = ttk.Label(txt, text="💼 " + APP_NAME, style="HeaderTitle.TLabel")
        self.title_lbl.pack(anchor="w")
        self.tag_lbl = ttk.Label(txt, text="", style="HeaderSub.TLabel")
        self.tag_lbl.pack(anchor="w")
        lang_box = ttk.Frame(header, style="Header.TFrame")
        lang_box.pack(side="right", anchor="e")
        ttk.Button(lang_box, text="ES",
                   command=lambda: self.set_lang("es")).pack(side="left", padx=3)
        ttk.Button(lang_box, text="EN",
                   command=lambda: self.set_lang("en")).pack(side="left", padx=3)

        self.nav = ttk.Frame(self, padding=(12, 10, 12, 0))
        self.nav.pack(fill="x")
        self.nav_btns = {}
        for key in ("nav_home", "nav_results", "nav_settings"):
            btn = ttk.Button(self.nav, text="", style="Ghost.TButton",
                             command=lambda k=key: self.show(k))
            btn.pack(side="left", padx=4)
            self.nav_btns[key] = btn

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=8)
        self.status = tk.StringVar(value="")
        bar = ttk.Label(self, textvariable=self.status, relief="flat",
                        anchor="w", padding=6, background=TH.PRIMARY_SOFT,
                        foreground=TH.PRIMARY, font=("Segoe UI", 9))
        bar.pack(fill="x", side="bottom")

    def _build_views(self):
        for w in self.container.winfo_children():
            w.destroy()
        self.views = {
            "nav_home": HomeView(self.container, self),
            "nav_results": ResultView(self.container, self),
            "nav_settings": SettingsView(self.container, self),
        }
        for key, btn in self.nav_btns.items():
            btn.config(text=t(key, self.lang))
        self.tag_lbl.config(text=t("tagline", self.lang))
        self._current = "nav_home"
        self.show("nav_home")

    def _apply_title(self):
        self.title(f"{APP_NAME} — {t('tagline', self.lang)}")

    def show(self, name: str):
        self._current = name
        for v in self.views.values():
            v.pack_forget()
        self.views[name].pack(fill="both", expand=True)

    def set_cv(self, cv_data: dict):
        self.cv_data = cv_data
        n = len(cv_data.get("skills", []))
        self.views["nav_home"].set_info(
            f"✅ {t('cv_ready', self.lang)} ({n} {t('skills', self.lang).lower()}): "
            + ", ".join(cv_data.get("skills", [])[:10]))
        self.status.set(f"📄 CV: {cv_data.get('email', '')}")

    def set_lang(self, lang: str):
        if lang not in ("es", "en") or lang == self.lang:
            return
        self.lang = lang
        self._apply_title()
        cv, jobs = self.cv_data, self.jobs
        self._build_views()
        self.cv_data = cv
        if jobs:
            self.jobs = jobs
            self.views["nav_results"].show_jobs(jobs, lang=self.lang)

    def search_jobs(self, keyword: str, location: str, hide_spam: bool = True,
                    job_types: list | None = None, modalities: list | None = None):
        if not keyword:
            messagebox.showwarning("Workapp", t("type_keyword", self.lang))
            return
        location = location or DEFAULT_LOCATION
        self.views["nav_home"].set_info(
            f"🔎 {t('searching', self.lang)} '{keyword}' {t('in', self.lang)} {location}…")
        self.status.set(f"🔎 {t('searching', self.lang)}…")
        self.update_idletasks()
        try:
            jobs = self.scrapers.search_all(keyword, location,
                                            job_types=job_types or [],
                                            modalities=modalities or [])
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Workapp", str(exc))
            return
        for j in jobs:
            j["spam"] = self.spam.detect(j)
        if hide_spam:
            jobs = [j for j in jobs if not j["spam"].get("is_spam")]
        if self.cv_data:
            jobs = self.matcher.rank(self.cv_data, jobs)
        self.jobs = jobs
        self.views["nav_results"].show_jobs(jobs, lang=self.lang)
        self.views["nav_home"].set_info(f"🎉 {len(jobs)} {t('found', self.lang)}")
        self.status.set(f"🎉 {len(jobs)} {t('found', self.lang)} · {location}")
        self.show("nav_results")


def run():
    app = MainWindow()
    app.mainloop()
