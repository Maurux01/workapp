"""Modern job card: accent bar, title, pills, hover lift effect."""
import tkinter as tk
from tkinter import ttk
import webbrowser
from ui import theme as TH
from utils.i18n import t


class JobCard(ttk.Frame):
    def __init__(self, parent, job: dict, lang: str = "es", **kwargs):
        super().__init__(parent, style="Card.TFrame", padding=0, **kwargs)
        self.job = job
        self.lang = lang
        self._build()
        self._hover(False)
        self.bind("<Enter>", lambda e: self._hover(True))
        self.bind("<Leave>", lambda e: self._hover(False))

    def _hover(self, on: bool):
        try:
            self.configure(cursor="hand2" if on else "")
        except tk.TclError:
            pass

    def _pill(self, parent, text, bg, fg):
        lbl = tk.Label(parent, text=text, background=bg, foreground=fg,
                       font=("Segoe UI", 8, "bold"), padx=10, pady=2,
                       borderwidth=0, highlightthickness=0)
        lbl.pack(side="left", padx=(0, 6), pady=2)
        return lbl

    def _build(self):
        score = self.job.get("score") or 0
        accent = TH.PRIMARY if score >= 60 else ("#f59e0b" if score >= 30 else TH.LINE)
        if score is None:
            accent = TH.PRIMARY
        bar = tk.Frame(self, background=accent, width=5)
        bar.pack(side="left", fill="y")
        body = ttk.Frame(self, style="Card.TFrame", padding=12)
        body.pack(side="left", fill="both", expand=True)

        top = ttk.Frame(body, style="Card.TFrame")
        top.pack(fill="x")
        ttk.Label(top, text=self.job.get("title", "—"), style="CardTitle.TLabel",
                  wraplength=560, justify="left").pack(side="left", fill="x", expand=True)
        if score:
            self._pill(top, f"{score}%", TH.PRIMARY_SOFT, TH.PRIMARY)

        sub = "  ·  ".join(p for p in (
            self.job.get("company_name", ""), self.job.get("location", ""),
            self.job.get("source", "")) if p)
        if sub:
            ttk.Label(body, text=sub, style="CardMuted.TLabel").pack(anchor="w", pady=(2, 0))

        pills = tk.Frame(body, background=TH.CARD)
        pills.pack(anchor="w", pady=(6, 0))
        jtype = self.job.get("job_type", "unknown")
        if jtype and jtype != "unknown":
            self._pill(pills, "💼 " + t(jtype, self.lang), "#f4f4f5", "#52525b")
        mod = self.job.get("modality", "unknown")
        if mod and mod != "unknown":
            icon = {"remote": "🌍", "onsite": "🏢", "hybrid": "🔀"}.get(mod, "📍")
            self._pill(pills, f"{icon} " + t(mod, self.lang), "#f4f4f5", "#52525b")
        spam = self.job.get("spam") or {}
        if spam:
            if spam.get("is_spam"):
                self._pill(pills, f"⚠ {t('possible_scam', self.lang)} "
                                  f"({t('risk', self.lang)} {spam.get('risk_score')})",
                           TH.DANGER_BG, TH.DANGER_FG)
            else:
                self._pill(pills, f"✓ {t('verified', self.lang)}",
                           TH.SUCCESS_BG, TH.SUCCESS_FG)

        matched = self.job.get("matched_skills") or []
        if matched:
            ttk.Label(body, text="✨ " + ", ".join(matched[:10]),
                      style="CardBody.TLabel").pack(anchor="w", pady=(6, 0))

        desc = (self.job.get("description") or "")[:380]
        if desc:
            ttk.Label(body, text=desc, style="CardBody.TLabel",
                      wraplength=580, justify="left").pack(anchor="w", pady=(6, 0))

        url = self.job.get("url", "")
        if url:
            link = tk.Label(body, text=f"{t('view_offer', self.lang)}  →",
                            foreground=TH.PRIMARY, background=TH.CARD,
                            font=("Segoe UI", 10, "bold"), cursor="hand2")
            link.pack(anchor="w", pady=(8, 0))
            link.bind("<Button-1>", lambda e: webbrowser.open(url))
