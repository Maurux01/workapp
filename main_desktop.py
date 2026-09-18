# Workapp — the smart way to get a job!
"""Desktop entry point."""
from ui.main_window import MainWindow


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
