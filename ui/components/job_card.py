"""Modern job card: accent bar, match meter, skill pills, modal on double-click."""
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
        self.bind("<Double-Button-1>", lambda e: self._open_detail())
        for child in self.winfo_children():
            child.bind("<Double-Button-1>", lambda e: self._open_detail())

    def _pill(self, parent, text, bg, fg):
        lbl = tk.Label(parent, text=text, background=bg, foreground=fg,
                       font=("Segoe UI", 8, "bold"), padx=10, pady=2,
                       borderwidth=0, highlightthickness=0)
        lbl.pack(side="left", padx=(0, 6), pady=2)
        return lbl

    def _build(self):
        score = self.job.get("score")
        accent = TH.PRIMARY
        if isinstance(score, (int, float)):
            accent = TH.PRIMARY if score >= 60 else ("#f59e0b" if score >= 30 else TH.MUTED)
        bar = tk.Frame(self, background=accent, width=5)
        bar.pack(side="left", fill="y")
        body = ttk.Frame(self, style="Card.TFrame", padding=12)
        body.pack(side="left", fill="both", expand=True)

        top = ttk.Frame(body, style="Card.TFrame")
        top.pack(fill="x")
        ttk.Label(top, text=self.job.get("title", "—"), style="CardTitle.TLabel",
                  wraplength=520, justify="left").pack(side="left", fill="x", expand=True)

        if isinstance(score, (int, float)):
            meter = ttk.Frame(top, style="Card.TFrame")
            meter.pack(side="right", padx=(12, 0), pady=(2, 0), anchor="n")
            ttk.Label(meter, text=f"{score}%", style="CardTitle.TLabel",
                      foreground=TH.PRIMARY).pack(anchor="e")
            bar_w = ttk.Progressbar(meter, style="Match.Horizontal.TProgressbar",
                                    length=110, mode="determinate", value=score)
            bar_w.pack(anchor="e", pady=(2, 0))

        sub = "  ·  ".join(p for p in (
            self.job.get("company_name", ""), self.job.get("location", ""),
            self.job.get("source", "")) if p)
        if sub:
            ttk.Label(body, text=sub, style="CardMuted.TLabel").pack(anchor="w", pady=(2, 0))

        pills = tk.Frame(body, background=TH.CARD)
        pills.pack(anchor="w", pady=(6, 0))
        jtype = self.job.get("job_type", "unknown")
        if jtype and jtype != "unknown":
            self._pill(pills, "💼 " + t(jtype, self.lang), TH.PRIMARY_SOFT, TH.PRIMARY)
        mod = self.job.get("modality", "unknown")
        if mod and mod != "unknown":
            icon = {"remote": "🌍", "onsite": "🏢", "hybrid": "🔀"}.get(mod, "📍")
            self._pill(pills, f"{icon} " + t(mod, self.lang), TH.PRIMARY_SOFT, TH.PRIMARY)
        spam = self.job.get("spam") or {}
        if spam:
            if spam.get("is_spam"):
                self._pill(pills, f"⚠ {t('possible_scam', self.lang)} "
                                  f"({t('risk', self.lang)} {spam.get('risk_score')})",
                           TH.DANGER_BG, TH.DANGER_FG)
            else:
                self._pill(pills, f"✓ {t('verified', self.lang)}",
                           TH.SUCCESS_BG, TH.SUCCESS_FG)

        for skill in (self.job.get("matched_skills") or [])[:8]:
            self._pill(pills, "✨ " + skill, TH.PRIMARY_SOFT, TH.PRIMARY)

        desc = (self.job.get("description") or "")[:320]
        if desc:
            ttk.Label(body, text=desc, style="CardBody.TLabel",
                      wraplength=580, justify="left").pack(anchor="w", pady=(6, 0))

        row = ttk.Frame(body, style="Card.TFrame")
        row.pack(fill="x", pady=(8, 0))
        url = self.job.get("url", "")
        if url:
            link = tk.Label(row, text=f"{t('view_offer', self.lang)}  →",
                            foreground=TH.PRIMARY, background=TH.CARD,
                            font=("Segoe UI", 10, "bold"), cursor="hand2")
            link.pack(side="left")
            link.bind("<Button-1>", lambda e: webbrowser.open(url))
        hint = tk.Label(row, text="🖱×2", background=TH.CARD, foreground=TH.MUTED,
                        font=("Segoe UI", 8))
        hint.pack(side="right")

    def _open_detail(self):
        win = tk.Toplevel(self)
        win.title(self.job.get("title", "Workapp")[:80])
        win.geometry("620x560")
        win.configure(background=TH.BG)
        try:
            win.transient(self.winfo_toplevel())
        except tk.TclError:
            pass
        frame = ttk.Frame(win, style="Card.TFrame", padding=16)
        frame.pack(fill="both", expand=True, padx=12, pady=12)
        ttk.Label(frame, text=self.job.get("title", "—"), style="CardTitle.TLabel",
                  font=("Segoe UI", 13, "bold"), wraplength=560,
                  justify="left").pack(anchor="w")
        sub = "  ·  ".join(p for p in (
            self.job.get("company_name", ""), self.job.get("location", ""),
            self.job.get("source", "")) if p)
        ttk.Label(frame, text=sub, style="CardMuted.TLabel").pack(anchor="w", pady=(2, 8))
        txt = tk.Text(frame, wrap="word", background=TH.CARD, foreground=TH.INK,
                      relief="flat", font=("Segoe UI", 10), padx=4, pady=4)
        scroll = ttk.Scrollbar(frame, command=txt.yview)
        txt.configure(yscrollcommand=scroll.set)
        txt.insert("1.0", self.job.get("description") or "")
        txt.configure(state="disabled")
        txt.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        bottom = ttk.Frame(win, padding=(12, 0, 12, 12))
        bottom.pack(fill="x")
        url = self.job.get("url", "")
        if url:
            ttk.Button(bottom, text=f"{t('view_offer', self.lang)}  →",
                       style="Accent.TButton",
                       command=lambda: webbrowser.open(url)).pack(side="right")
