"""PDF upload + CV analysis widget."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from core.cv_analyzer import CVAnalyzer
from utils.i18n import t

_analyzer = CVAnalyzer()


class PdfUploader(ttk.Frame):
    def __init__(self, parent, on_analyzed=None, lang: str = "es", **kwargs):
        super().__init__(parent, **kwargs)
        self.on_analyzed = on_analyzed
        self.lang = lang
        self.status = tk.StringVar(value=t("no_cv", lang))
        ttk.Button(self, text=t("upload_cv", lang), command=self._pick).pack(side="left")
        ttk.Label(self, textvariable=self.status, foreground="#64748b",
                  wraplength=480, justify="left").pack(side="left", padx=10)

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
            f"{t('cv_ready', self.lang)}: {data.get('email', '')} · "
            f"{t('experience', self.lang)}: {data.get('experience_years', '')} · {skills[:90]}"
        )
        if self.on_analyzed:
            self.on_analyzed(data)
