# Workapp — the smart way to get a job!
"""Desktop entry point."""
import sys
import traceback


def _log_crash(text: str) -> None:
    # pythonw.exe has no console: persist errors so they are not lost.
    try:
        with open("Workapp-error.log", "a", encoding="utf-8") as fh:
            fh.write(text + "\n")
    except OSError:
        pass


def main():
    from ui.main_window import MainWindow
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception:  # noqa: BLE001
        _log_crash(traceback.format_exc())
        raise
