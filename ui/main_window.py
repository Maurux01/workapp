"""Main window: splash, indigo header, theme toggle, threaded search + progress."""
import queue
import threading
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


class Splash(tk.Toplevel):
    def __init__(self, parent, lang: str):
        super().__init__(parent)
        self.overrideredirect(True)
        self.configure(background=TH.PRIMARY_DARK)
        w, h = 380, 200
        x = parent.winfo_screenwidth() // 2 - w // 2
        y = parent.winfo_screenheight() // 2 - h // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
        tk.Label(self, text="💼", font=("Segoe UI", 44),
                 background=TH.PRIMARY_DARK, foreground="white").pack(pady=(24, 0))
        tk.Label(self, text=APP_NAME, font=("Segoe UI", 18, "bold"),
                 background=TH.PRIMARY_DARK, foreground="white").pack()
        tk.Label(self, text=t("tagline", lang), font=("Segoe UI", 10),
                 background=TH.PRIMARY_DARK, foreground="#c7d2fe").pack(pady=(4, 0))
        self.after(1300, self.destroy)


class MainWindow(tk.Tk):
    def __init__(self, lang: str = DEFAULT_LANG):
        super().__init__()
        self.lang = lang if lang in ("es", "en") else "es"
        self.cv_data: dict | None = None
        self.jobs: list = []
        self.matcher = JobMatcher()
        self.spam = SpamDetector()
        self.scrapers = ScraperManager()
        self._searching = False
        self._result_queue: queue.Queue = queue.Queue()
        TH.apply(self)
        self.geometry("860x720")
        self.minsize(720, 600)
        self.withdraw()
        Splash(self, self.lang)
        self.after(1350, self.deiconify)
        self._build_chrome()
        self._build_views()
        self._apply_title()

    # --- chrome ---
    def _app_icon(self, size: int = 28):
        """Load the devicon (cached). None if missing."""
        key = f"_icon_{size}"
        if hasattr(self, key):
            return getattr(self, key)
        img = None
        try:
            from pathlib import Path
            png = Path(__file__).resolve().parent.parent / "assets" / "icon-64.png"
            if png.is_file():
                img = tk.PhotoImage(file=str(png)).subsample(max(1, 64 // size), max(1, 64 // size))
                setattr(self, key, img)
        except Exception:  # noqa: BLE001
            img = None
        return img

    def _apply_window_icon(self):
        try:
            from pathlib import Path
            ico = Path(__file__).resolve().parent.parent / "assets" / "icon.ico"
            if ico.is_file() and hasattr(self, "iconbitmap"):
                self.iconbitmap(default=str(ico))
        except Exception:  # noqa: BLE001
            pass
        img = self._app_icon(32)
        if img:
            try:
                self.iconphoto(True, img)
            except Exception:  # noqa: BLE001
                pass

    def _build_chrome(self):
        self._apply_window_icon()
        header = ttk.Frame(self, style="Header.TFrame", padding=(16, 14))
        header.pack(fill="x")
        logo = ttk.Frame(header, style="Header.TFrame")
        logo.pack(side="left")
        icon = self._app_icon(30)
        if icon:
            ttk.Label(logo, image=icon, style="Header.TLabel").pack(side="left", padx=(0, 10))
        txt = ttk.Frame(header, style="Header.TFrame")
        txt.pack(side="left")
        self.title_lbl = ttk.Label(txt, text=APP_NAME, style="HeaderTitle.TLabel")
        self.title_lbl.pack(anchor="w")
        self.tag_lbl = ttk.Label(txt, text="", style="HeaderSub.TLabel")
        self.tag_lbl.pack(anchor="w")
        right = ttk.Frame(header, style="Header.TFrame")
        right.pack(side="right", anchor="e")
        self.theme_btn = ttk.Button(right, text=self._theme_icon(),
                                    style="Header.TButton",
                                    command=self.toggle_theme, width=4)
        self.theme_btn.pack(side="left", padx=3)
        ttk.Button(right, text="ES", style="Header.TButton",
                   command=lambda: self.set_lang("es")).pack(side="left", padx=3)
        ttk.Button(right, text="EN", style="Header.TButton",
                   command=lambda: self.set_lang("en")).pack(side="left", padx=3)

        self.nav = ttk.Frame(self, padding=(12, 10, 12, 0))
        self.nav.pack(fill="x")
        self.nav_btns = {}
        for key in ("nav_home", "nav_results", "nav_settings"):
            btn = ttk.Button(self.nav, text="", style="Ghost.TButton",
                             command=lambda k=key: self.show(k))
            btn.pack(side="left", padx=4)
            self.nav_btns[key] = btn

        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=8)
        self.status = tk.StringVar(value="")
        bar = ttk.Label(self, textvariable=self.status, relief="flat",
                        anchor="w", padding=6, background=TH.PRIMARY_SOFT,
                        foreground=TH.PRIMARY, font=("Segoe UI", 9))
        bar.pack(fill="x", side="bottom")

    def _theme_icon(self) -> str:
        return "☀️" if TH.MODE == "dark" else "🌙"

    def toggle_theme(self):
        TH.set_mode("dark" if TH.MODE == "light" else "light")
        TH.apply(self)
        cv, jobs = self.cv_data, self.jobs
        for w in self.winfo_children():
            w.destroy()
        self._build_chrome()
        self._build_views()
        self.cv_data = cv
        if jobs:
            self.jobs = jobs
            self.views["nav_results"].show_jobs(jobs, lang=self.lang)

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

    # --- behavior ---
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
        if self._searching:
            return
        if not keyword:
            messagebox.showwarning("Workapp", t("type_keyword", self.lang))
            return
        self._searching = True
        location = location or DEFAULT_LOCATION
        self.views["nav_home"].set_info(
            f"🔎 {t('searching', self.lang)} '{keyword}' {t('in', self.lang)} {location}…")
        self.status.set(f"🔎 {t('searching', self.lang)}…")
        self.progress.pack(fill="x", padx=12)
        self.progress.start(12)
        threading.Thread(
            target=self._search_worker,
            args=("keyword", keyword, location, hide_spam,
                  job_types or [], modalities or []),
            daemon=True).start()
        self.after(150, self._poll_search)

    def search_for_cv(self, location: str = "", hide_spam: bool = True,
                      job_types: list | None = None, modalities: list | None = None):
        """One search per top CV skill → merged, ranked jobs."""
        if self._searching:
            return
        if not self.cv_data:
            messagebox.showwarning("Workapp", t("no_cv", self.lang))
            return
        self._searching = True
        location = location or DEFAULT_LOCATION
        self.views["nav_home"].set_info(
            f"✨ {t('match_cv', self.lang)}… 🔎 {t('searching', self.lang)}…")
        self.status.set(f"✨ {t('searching', self.lang)}…")
        self.progress.pack(fill="x", padx=12)
        self.progress.start(12)
        threading.Thread(
            target=self._search_worker,
            args=("cv", None, location, hide_spam,
                  job_types or [], modalities or []),
            daemon=True).start()
        self.after(150, self._poll_search)

    def _search_worker(self, mode, keyword, location, hide_spam, job_types, modalities):
        # NOTE: never touch tkinter widgets here — results go via queue.
        try:
            queries: list = []
            if mode == "cv":
                jobs, queries = self.scrapers.search_for_cv(
                    self.cv_data, location,
                    job_types=job_types, modalities=modalities)
            else:
                jobs = self.scrapers.search_all(keyword, location,
                                                job_types=job_types, modalities=modalities)
            for j in jobs:
                j["spam"] = self.spam.detect(j)
            if hide_spam:
                jobs = [j for j in jobs if not j["spam"].get("is_spam")]
            if self.cv_data:
                jobs = self.matcher.rank(self.cv_data, jobs)
            self._result_queue.put((jobs, location, queries, None))
        except Exception as exc:  # noqa: BLE001
            self._result_queue.put(([], location, [], str(exc)))

    def _poll_search(self):
        # Runs in the main thread: safe to touch the UI here.
        try:
            jobs, location, queries, error = self._result_queue.get_nowait()
        except queue.Empty:
            if self._searching:
                self.after(150, self._poll_search)
            return
        self._search_done(jobs, location, queries, error)

    def _search_done(self, jobs: list, location: str, queries: list, error: str | None):
        self._searching = False
        self.progress.stop()
        self.progress.pack_forget()
        if error:
            messagebox.showerror("Workapp", error)
            self.status.set("⚠ " + error[:100])
            return
        self.jobs = jobs
        self.views["nav_results"].show_jobs(jobs, lang=self.lang)
        extra = f" 🔎 [{', '.join(queries[:6])}]" if queries else ""
        self.views["nav_home"].set_info(f"🎉 {len(jobs)} {t('found', self.lang)}{extra}")
        self.status.set(f"🎉 {len(jobs)} {t('found', self.lang)} · {location}")
        self.show("nav_results")


def run():
    app = MainWindow()
    app.mainloop()
