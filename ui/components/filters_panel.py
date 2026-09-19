"""Modern search filters: keyword/location + pills for type/modality + big CTA."""
import tkinter as tk
from tkinter import ttk
from config import DEFAULT_LOCATION
from ui import theme as TH
from utils.i18n import t, JOB_TYPE_KEYS, MODALITY_KEYS

TYPE_ICONS = {"full_time": "💼", "part_time": "🕐", "freelance": "🚀", "internship": "🎓"}
MOD_ICONS = {"remote": "🌍", "onsite": "🏢", "hybrid": "🔀"}


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
        search = ttk.Frame(self, style="Card.TFrame", padding=14)
        search.pack(fill="x")
        ttk.Label(search, text="🔎 " + t("search", self.lang),
                  style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))

        row = ttk.Frame(search, style="Card.TFrame")
        row.pack(fill="x")
        ttk.Label(row, text=t("keyword", self.lang),
                  style="CardBody.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Entry(row, textvariable=self.keyword, width=26).grid(row=1, column=0,
                                                                 padx=(0, 10), sticky="ew")
        ttk.Label(row, text=t("location", self.lang),
                  style="CardBody.TLabel").grid(row=0, column=1, sticky="w")
        ttk.Entry(row, textvariable=self.location, width=20).grid(row=1, column=1,
                                                                  padx=(0, 10), sticky="ew")
        go = ttk.Button(row, text="✨ " + t("search", self.lang),
                        style="Accent.TButton", command=self._go)
        go.grid(row=0, column=2, rowspan=2, padx=(6, 0), sticky="ns")
        row.columnconfigure(0, weight=1)
        row.columnconfigure(1, weight=1)

        jf = ttk.LabelFrame(self, text="💼 " + t("job_type", self.lang))
        jf.pack(fill="x", pady=(10, 0))
        for i, key in enumerate(JOB_TYPE_KEYS):
            ttk.Checkbutton(jf, text=f"{TYPE_ICONS.get(key, '')} {t(key, self.lang)}",
                            variable=self.type_vars[key]).grid(row=0, column=i,
                                                               padx=10, pady=4, sticky="w")

        mf = ttk.LabelFrame(self, text="📍 " + t("modality", self.lang))
        mf.pack(fill="x", pady=(6, 0))
        for i, key in enumerate(MODALITY_KEYS):
            ttk.Checkbutton(mf, text=f"{MOD_ICONS.get(key, '')} {t(key, self.lang)}",
                            variable=self.mod_vars[key]).grid(row=0, column=i,
                                                              padx=10, pady=4, sticky="w")

        bottom = ttk.Frame(self)
        bottom.pack(fill="x", pady=(8, 0))
        ttk.Checkbutton(bottom, text="🛡 " + t("hide_spam", self.lang),
                        variable=self.hide_spam).pack(side="left")

    def _go(self):
        if self.on_search:
            self.on_search(
                self.keyword.get().strip(),
                self.location.get().strip(),
                self.hide_spam.get(),
                [k for k, v in self.type_vars.items() if v.get()],
                [k for k, v in self.mod_vars.items() if v.get()],
            )
