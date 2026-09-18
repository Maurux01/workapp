"""Search filters: keyword, location, hide-spam toggle."""
import tkinter as tk
from config import DEFAULT_LOCATION


class FiltersPanel(tk.Frame):
    def __init__(self, parent, on_search=None, lang: str = "es", **kwargs):
        super().__init__(parent, **kwargs)
        self.on_search = on_search
        self.keyword = tk.StringVar(value="python")
        self.location = tk.StringVar(value=DEFAULT_LOCATION)
        self.hide_spam = tk.BooleanVar(value=True)

        tk.Label(self, text="Palabra clave / Keyword:").grid(row=0, column=0, sticky="w")
        tk.Entry(self, textvariable=self.keyword, width=30).grid(row=0, column=1, padx=6)
        tk.Label(self, text="Ubicación / Location:").grid(row=1, column=0, sticky="w")
        tk.Entry(self, textvariable=self.location, width=30).grid(row=1, column=1, padx=6)
        tk.Checkbutton(self, text="Ocultar posible fraude / Hide scams", variable=self.hide_spam).grid(row=2, column=0, columnspan=2, sticky="w")
        tk.Button(self, text="Buscar / Search", command=self._go, bg="#1d4ed8", fg="white").grid(row=0, column=2, rowspan=3, padx=10, ipadx=10, ipady=6)

    def _go(self):
        if self.on_search:
            self.on_search(self.keyword.get().strip(), self.location.get().strip(), self.hide_spam.get())
