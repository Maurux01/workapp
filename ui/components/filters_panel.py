"""Search filters: keyword, location, job-type + modality checkboxes, anti-scam."""
import tkinter as tk
from tkinter import ttk
from config import DEFAULT_LOCATION
from utils.i18n import t, JOB_TYPE_KEYS, MODALITY_KEYS


class FiltersPanel(ttk.Frame):
    def __init__(self, parent, on_search=None, lang: str = "es", **kwargs):
        super().__init__(parent, **kwargs)
        self.on_search = on_search
        self.lang = lang
        self.keyword = tk.StringVar(value="python")
        self.location = tk.StringVar(value=DEFAULT_LOCATION)
        self.hide_spam = tk.BooleanVar(value=True)
        self.type_vars = {k: tk.BooleanVar(value=False) for k in JOB_TYPE_KEYS}
        self.mod_vars = {k: tk.BooleanVar(value=False) for k in MODALITY_KEYS}
        self._build()

    def _build(self):
        top = ttk.Frame(self)
        top.pack(fill="x", pady=4)
        ttk.Label(top, text=t("keyword", self.lang) + ":").grid(row=0, column=0, sticky="w")
        ttk.Entry(top, textvariable=self.keyword, width=28).grid(row=0, column=1, padx=6)
        ttk.Label(top, text=t("location", self.lang) + ":").grid(row=0, column=2, sticky="w")
        ttk.Entry(top, textvariable=self.location, width=22).grid(row=0, column=3, padx=6)

        jf = ttk.LabelFrame(self, text=t("job_type", self.lang))
        jf.pack(fill="x", pady=4)
        for i, key in enumerate(JOB_TYPE_KEYS):
            ttk.Checkbutton(jf, text=t(key, self.lang),
                            variable=self.type_vars[key]).grid(row=0, column=i, padx=8, sticky="w")

        mf = ttk.LabelFrame(self, text=t("modality", self.lang))
        mf.pack(fill="x", pady=4)
        for i, key in enumerate(MODALITY_KEYS):
            ttk.Checkbutton(mf, text=t(key, self.lang),
                            variable=self.mod_vars[key]).grid(row=0, column=i, padx=8, sticky="w")

        bottom = ttk.Frame(self)
        bottom.pack(fill="x", pady=4)
        ttk.Checkbutton(bottom, text=t("hide_spam", self.lang),
                        variable=self.hide_spam).pack(side="left")
        ttk.Button(bottom, text=t("search", self.lang),
                   command=self._go).pack(side="right", ipadx=16, ipady=2)

    def _go(self):
        if self.on_search:
            self.on_search(
                self.keyword.get().strip(),
                self.location.get().strip(),
                self.hide_spam.get(),
                [k for k, v in self.type_vars.items() if v.get()],
                [k for k, v in self.mod_vars.items() if v.get()],
            )
