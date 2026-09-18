"""Reusable job card widget."""
import tkinter as tk


class JobCard(tk.Frame):
    def __init__(self, parent, job: dict, lang: str = "es", **kwargs):
        super().__init__(parent, relief="groove", borderwidth=1, padx=8, pady=6, **kwargs)
        self.job = job
        self.lang = lang
        self._build()

    def _build(self):
        title = self.job.get("title", "—")
        company = self.job.get("company_name", "")
        loc = self.job.get("location", "")
        score = self.job.get("score")
        spam = self.job.get("spam", {})
        url = self.job.get("url", "")

        header = f"{title}"
        if score is not None:
            header += f"  —  {score}% match"
        tk.Label(self, text=header, font=("Arial", 10, "bold"), wraplength=550, justify="left").pack(anchor="w")
        tk.Label(self, text=f"{company}  ·  {loc}  ·  {self.job.get('source','')}", fg="gray").pack(anchor="w")

        if isinstance(spam, dict) and spam:
            if spam.get("is_spam"):
                msg = "⚠️ Posible fraude / Possible scam" if True else ""
                tk.Label(self, text=f"{msg} (riesgo {spam.get('risk_score')})", fg="red").pack(anchor="w")
            else:
                tk.Label(self, text="✓ Verificada / Verified", fg="green").pack(anchor="w")

        matched = self.job.get("matched_skills") or []
        if matched:
            tk.Label(self, text="Skills: " + ", ".join(matched[:10]), fg="#333").pack(anchor="w")

        desc = (self.job.get("description") or "")[:400]
        if desc:
            tk.Label(self, text=desc, wraplength=550, justify="left").pack(anchor="w", pady=(4, 0))

        if url:
            link = tk.Label(self, text=url[:90], fg="blue", cursor="hand2")
            link.pack(anchor="w")
            link.bind("<Button-1>", lambda e: __import__("webbrowser").open(url))
