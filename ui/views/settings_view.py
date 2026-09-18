"""Settings: language + cache management + sources info."""
import tkinter as tk
from tkinter import ttk, messagebox
from scrapers.scraper_manager import ScraperManager
from utils.i18n import t


class SettingsView(ttk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, padding=12, **kwargs)
        self.app = app
        lang = app.lang
        ttk.Label(self, text=t("nav_settings", lang),
                  font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 8))

        ttk.Label(self, text=t("language", lang)).pack(anchor="w")
        self.lang_var = tk.StringVar(value=lang)
        ttk.Combobox(self, textvariable=self.lang_var, values=["es", "en"],
                     state="readonly", width=8).pack(anchor="w", pady=4)
        ttk.Button(self, text=t("apply", lang),
                   command=self._apply).pack(anchor="w", pady=4)

        ttk.Separator(self).pack(fill="x", pady=10)
        ttk.Button(self, text=t("clear_cache", lang),
                   command=self._clear).pack(anchor="w")

        ttk.Separator(self).pack(fill="x", pady=10)
        ttk.Label(self, text=f"{t('sources', lang)}: "
                             + ", ".join(ScraperManager.SOURCES),
                  wraplength=600, justify="left",
                  foreground="#475569").pack(anchor="w")

    def _apply(self):
        self.app.set_lang(self.lang_var.get())
        messagebox.showinfo("Workapp", t("lang_updated", self.app.lang))

    def _clear(self):
        try:
            from storage.local_cache import LocalCache
            n = LocalCache().clear()
            messagebox.showinfo("Workapp",
                                f"{t('cache_cleared', self.app.lang)}: {n}")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Workapp", str(exc))
