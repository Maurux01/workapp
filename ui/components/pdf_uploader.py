"""PDF upload + CV analysis widget."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from core.cv_analyzer import CVAnalyzer
from utils.i18n import t

_analyzer = CVAnalyzer()


class PdfUploader(ttk.Frame):
    def __init__(self, parent, on_analyzed=None, lang: str = "es", **kwargs):
        super().__init__(parent, style="Card.TFrame", padding=14, **kwargs)
        self.on_analyzed = on_analyzed
        self.lang = lang
        self.status = tk.StringVar(value=t("no_cv", lang))
        ttk.Label(self, text="📄 " + t("upload_cv", lang),
                  style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))
        row = ttk.Frame(self, style="Card.TFrame")
        row.pack(fill="x")
        ttk.Button(row, text="⬆ " + t("upload_cv", lang), style="Ghost.TButton",
                   command=self._pick).pack(side="left")
        ttk.Label(row, textvariable=self.status, style="CardMuted.TLabel",
                  wraplength=420, justify="left").pack(side="left", padx=12)

    def _pick(self):
        path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if not path:
            return
        data = _analyzer.analyze(path)
        if "error" in data:
            messagebox.showerror("Workapp", t("could_not_read_cv", self.lang))
            return
        skills = ", ".join(data.get("skills", [])[:12]) or "—"
        self.status.set(
            f"✅ {t('cv_ready', self.lang)}: {data.get('email', '')} · "
            f"{t('experience', self.lang)}: {data.get('experience_years', '')}\n{skills[:100]}"
        )
        if self.on_analyzed:
            self.on_analyzed(data)
