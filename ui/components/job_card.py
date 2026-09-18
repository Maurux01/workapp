"""Job card widget: title, company, badges (match/type/modality/spam), link."""
import tkinter as tk
from tkinter import ttk
import webbrowser
from utils.i18n import t


class JobCard(ttk.Frame):
    def __init__(self, parent, job: dict, lang: str = "es", **kwargs):
        super().__init__(parent, relief="solid", borderwidth=1, padding=10, **kwargs)
        self.job = job
        self.lang = lang
        self._build()

    def _build(self):
        title = self.job.get("title", "—")
        ttk.Label(self, text=title, font=("Segoe UI", 10, "bold"),
                  wraplength=600, justify="left").pack(anchor="w")

        sub = "  ·  ".join(p for p in (
            self.job.get("company_name", ""),
            self.job.get("location", ""),
            self.job.get("source", "")) if p)
        if sub:
            ttk.Label(self, text=sub, foreground="#64748b").pack(anchor="w")

        badges = ttk.Frame(self)
        badges.pack(anchor="w", pady=(4, 0))
        score = self.job.get("score")
        if score is not None:
            ttk.Label(badges, text=f"{score}% {t('match', self.lang)}",
                      background="#dbeafe", padding=(8, 2)).pack(side="left", padx=(0, 6))
        jtype = self.job.get("job_type", "unknown")
        if jtype and jtype != "unknown":
            ttk.Label(badges, text=t(jtype, self.lang),
                      background="#f1f5f9", padding=(8, 2)).pack(side="left", padx=(0, 6))
        mod = self.job.get("modality", "unknown")
        if mod and mod != "unknown":
            ttk.Label(badges, text=t(mod, self.lang),
                      background="#f1f5f9", padding=(8, 2)).pack(side="left", padx=(0, 6))
        spam = self.job.get("spam") or {}
        if spam:
            if spam.get("is_spam"):
                ttk.Label(badges,
                          text=f"⚠ {t('possible_scam', self.lang)} ({t('risk', self.lang)} {spam.get('risk_score')})",
                          background="#fee2e2", foreground="#991b1b",
                          padding=(8, 2)).pack(side="left")
            else:
                ttk.Label(badges, text=f"✓ {t('verified', self.lang)}",
                          background="#dcfce7", foreground="#166534",
                          padding=(8, 2)).pack(side="left")

        matched = self.job.get("matched_skills") or []
        if matched:
            ttk.Label(self, text=f"{t('skills', self.lang)}: " + ", ".join(matched[:10]),
                      foreground="#334155").pack(anchor="w", pady=(4, 0))

        desc = (self.job.get("description") or "")[:400]
        if desc:
            ttk.Label(self, text=desc, wraplength=600,
                      justify="left").pack(anchor="w", pady=(4, 0))

        url = self.job.get("url", "")
        if url:
            link = ttk.Label(self, text=f"{t('view_offer', self.lang)} →",
                             foreground="#1d4ed8", cursor="hand2")
            link.pack(anchor="w", pady=(4, 0))
            link.bind("<Button-1>", lambda e: webbrowser.open(url))
