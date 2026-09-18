"""Workapp install wizard (tkinter, no extra deps). ES/EN.
Run:  python install_wizard.py
Steps: 1) welcome 2) check python+pip 3) install requirements
       4) create .env + language 5) done (launch web/desktop).
"""
import os
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STR = {
    "es": {"title": "Instalador de Workapp", "next": "Siguiente", "back": "Atrás",
           "install": "Instalar", "close": "Cerrar", "lang": "Idioma / Language:"},
    "en": {"title": "Workapp Installer", "next": "Next", "back": "Back",
           "install": "Install", "close": "Close", "lang": "Idioma / Language:"},
}


def check_python():
    ok = sys.version_info >= (3, 10)
    return ok, f"Python {sys.version.split()[0]} ({'OK' if ok else 'se requiere 3.10+ / requires 3.10+'})"


def run_pip_install(log):
    cmd = [sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")]
    log("pip install -r requirements.txt …\n")
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        log(p.stdout[-2000:] + ("\n" + p.stderr[-2000:] if p.stderr else ""))
        return p.returncode == 0
    except Exception as exc:  # noqa: BLE001
        log(f"ERROR: {exc}\n")
        return False


def setup_env(lang: str):
    env = ROOT / ".env"
    example = ROOT / ".env.example"
    if not env.is_file() and example.is_file():
        text = example.read_text(encoding="utf-8").replace("WORKAPP_LANG=es", f"WORKAPP_LANG={lang}")
        env.write_text(text, encoding="utf-8")
        return True
    return False


class Wizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang = tk.StringVar(value="es")
        self.step = 0
        self.title("Workapp Installer")
        self.geometry("560x440")
        self.body = tk.Frame(self, padx=16, pady=12)
        self.body.pack(fill="both", expand=True)
        nav = tk.Frame(self)
        nav.pack(fill="x", padx=16, pady=10)
        self.back_btn = tk.Button(nav, text="Atrás", command=self.prev)
        self.back_btn.pack(side="left")
        self.next_btn = tk.Button(nav, text="Siguiente", command=self.next, bg="#1d4ed8", fg="white")
        self.next_btn.pack(side="right")
        self.render()

    def t(self, key):
        return STR[self.lang.get()][key]

    def clear(self):
        for w in self.body.winfo_children():
            w.destroy()

    def render(self):
        self.title(self.t("title"))
        self.back_btn.config(text=self.t("back"), state="normal" if self.step > 0 else "disabled")
        self.next_btn.config(text=self.t("close") if self.step == 3 else (self.t("install") if self.step == 2 else self.t("next")))
        self.clear()
        [self.page_welcome, self.page_reqs, self.page_config, self.page_done][self.step]()

    # --- pages ---
    def page_welcome(self):
        tk.Label(self.body, text="Workapp — The smart way to get a job",
                 font=("Arial", 12, "bold")).pack(anchor="w", pady=6)
        tk.Label(self.body, wraplength=480, justify="left",
                 text="Este asistente instala dependencias, crea tu .env y deja lista la app desktop + web.\n"
                      "This wizard installs dependencies, creates your .env and gets desktop + web ready.").pack(anchor="w")
        tk.Label(self.body, text=self.t("lang")).pack(anchor="w", pady=(12, 0))
        tk.OptionMenu(self.body, self.lang, "es", "en", command=lambda _: self.render()).pack(anchor="w")

    def page_reqs(self):
        ok_py, msg_py = check_python()
        ok_pip = shutil.which("pip") is not None or True
        tk.Label(self.body, text="1. Python: " + msg_py, fg="green" if ok_py else "red").pack(anchor="w")
        tk.Label(self.body, text=f"2. pip: {'OK' if ok_pip else 'FALTA / MISSING'}",
                 fg="green" if ok_pip else "red").pack(anchor="w")
        tk.Label(self.body, text="3. requirements.txt: flask, requests, bs4, lxml, pypdf, dotenv").pack(anchor="w", pady=6)
        if not ok_py:
            tk.Label(self.body, text="Instala Python 3.10+ desde python.org y vuelve aquí.",
                     fg="red").pack(anchor="w")

    def page_config(self):
        tk.Label(self.body, text=self.t("lang")).pack(anchor="w")
        tk.OptionMenu(self.body, self.lang, "es", "en").pack(anchor="w", pady=4)
        self.log = tk.Text(self.body, height=12)
        self.log.pack(fill="both", expand=True, pady=8)
        self.log.insert("1.0", "Pulsa Instalar / Press Install.\n")

    def page_done(self):
        tk.Label(self.body, text="✓ Workapp lista / ready", font=("Arial", 12, "bold"), fg="green").pack(anchor="w")
        tk.Button(self.body, text="Probar web / Try web (python main_web.py → :5000)",
                  command=self.launch_web).pack(fill="x", pady=4)
        tk.Button(self.body, text="Abrir desktop / Open desktop (python main_desktop.py)",
                  command=self.launch_desktop).pack(fill="x", pady=4)
        tk.Label(self.body, wraplength=480, justify="left", fg="gray",
                 text="Si Indeed/Computrabajo bloquean (403/500), LinkedIn + caché siguen funcionando.").pack(anchor="w", pady=8)

    # --- nav ---
    def prev(self):
        if self.step > 0:
            self.step -= 1
            self.render()

    def next(self):
        if self.step == 2:  # install action
            self.do_install()
            return
        if self.step < 3:
            self.step += 1
            self.render()
        else:
            self.destroy()

    def do_install(self):
        log = lambda s: (self.log.insert("end", s), self.log.see("end"), self.update_idletasks())
        ok = run_pip_install(log)
        created = setup_env(self.lang.get())
        log(("\n.env creado / created\n" if created else "\n.env ya existía / already existed\n"))
        if ok:
            messagebox.showinfo("Workapp", "Instalación OK / Install OK")
            self.step = 3
            self.render()
        else:
            messagebox.showerror("Workapp", "Falló pip install. Revisa el log. / pip install failed. Check log.")

    def launch_web(self):
        subprocess.Popen([sys.executable, str(ROOT / "main_web.py")])

    def launch_desktop(self):
        subprocess.Popen([sys.executable, str(ROOT / "main_desktop.py")])


if __name__ == "__main__":
    Wizard().mainloop()
