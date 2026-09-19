"""Settings: language + cache + sources (themed)."""
import tkinter as tk
from tkinter import ttk, messagebox
from scrapers.scraper_manager import ScraperManager
from utils.i18n import t


class SettingsView(ttk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, padding=14, **kwargs)
        self.app = app
        lang = app.lang
        card = ttk.Frame(self, style="Card.TFrame", padding=16)
        card.pack(fill="x")
        ttk.Label(card, text="⚙ " + t("nav_settings", lang),
                  style="CardTitle.TLabel").pack(anchor="w", pady=(0, 10))

        ttk.Label(card, text="🌐 " + t("language", lang),
                  style="CardBody.TLabel").pack(anchor="w")
        self.lang_var = tk.StringVar(value=lang)
        ttk.Combobox(card, textvariable=self.lang_var, values=["es", "en"],
                     state="readonly", width=8).pack(anchor="w", pady=6)
        ttk.Button(card, text=t("apply", lang), style="Accent.TButton",
                   command=self._apply).pack(anchor="w", pady=4)
        ttk.Button(card, text="🧹 " + t("clear_cache", lang), style="Ghost.TButton",
                   command=self._clear).pack(anchor="w", pady=4)

        src = ttk.Frame(self, style="Card.TFrame", padding=16)
        src.pack(fill="x", pady=(12, 0))
        ttk.Label(src, text="📡 " + t("sources", lang),
                  style="CardTitle.TLabel").pack(anchor="w", pady=(0, 6))
        ttk.Label(src, text=", ".join(ScraperManager.SOURCES),
                  style="CardMuted.TLabel",
                  wraplength=600, justify="left").pack(anchor="w")

    def _apply(self):
        self.app.set_lang(self.lang_var.get())
        messagebox.showinfo("Workapp", "✅ " + t("lang_updated", self.app.lang))

    def _clear(self):
        try:
            from storage.local_cache import LocalCache
            n = LocalCache().clear()
            messagebox.showinfo("Workapp",
                                f"🧹 {t('cache_cleared', self.app.lang)}: {n}")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Workapp", str(exc))
