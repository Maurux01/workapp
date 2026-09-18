"""Settings: language + cache management."""
import tkinter as tk
from tkinter import messagebox


class SettingsView(tk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        tk.Label(self, text="Ajustes / Settings", font=("Arial", 11, "bold")).pack(anchor="w", pady=8)

        tk.Label(self, text="Idioma / Language:").pack(anchor="w")
        self.lang_var = tk.StringVar(value=app.lang)
        tk.OptionMenu(self, self.lang_var, "es", "en").pack(anchor="w")
        tk.Button(self, text="Aplicar / Apply", command=self._apply).pack(anchor="w", pady=6)

        tk.Button(self, text="Limpiar caché / Clear cache", command=self._clear).pack(anchor="w", pady=6)

    def _apply(self):
        self.app.set_lang(self.lang_var.get())
        messagebox.showinfo("Workapp", "Idioma actualizado / Language updated")

    def _clear(self):
        try:
            from storage.local_cache import LocalCache
            n = LocalCache().clear()
            messagebox.showinfo("Workapp", f"Caché limpiada: {n} archivos / Cache cleared: {n} files")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Workapp", str(exc))
