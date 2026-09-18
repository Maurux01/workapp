"""PDF upload + CV analysis widget."""
import tkinter as tk
from tkinter import filedialog, messagebox
from core.cv_analyzer import CVAnalyzer

_analyzer = CVAnalyzer()


class PdfUploader(tk.Frame):
    def __init__(self, parent, on_analyzed=None, lang: str = "es", **kwargs):
        super().__init__(parent, **kwargs)
        self.on_analyzed = on_analyzed
        self.lang = lang
        self.status = tk.StringVar(value="Sin CV / No CV yet")
        btn_text = "Subir CV (PDF) / Upload CV" 
        tk.Button(self, text=btn_text, command=self._pick).pack(side="left")
        tk.Label(self, textvariable=self.status, fg="gray").pack(side="left", padx=8)

    def _pick(self):
        path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if not path:
            return
        data = _analyzer.analyze(path)
        if "error" in data:
            messagebox.showerror("Workapp", data["error"])
            return
        skills = ", ".join(data.get("skills", [])[:12]) or "—"
        self.status.set(f"CV: {data.get('email','')} | {data.get('experience_years','')} | {skills[:80]}")
        if self.on_analyzed:
            self.on_analyzed(data)
