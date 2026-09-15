# Code Totally made by
# █   █  ███  █   █ ████  █   █ █   █  ███    █
# ██ ██ █   █ █   █ █   █ █   █  █ █  █   █  ██
# █ █ █ █████ █   █ ████  █   █   █   █   █   █
# █   █ █   █ █   █ █  █  █   █  █ █  █   █   █
# █   █ █   █  ███  █   █  ███  █   █  ███   ███

# Workapp- the smart way to get a job!


# dependcies imported
from token import EQUAL

import flet as ft
from ui.main_window import main_window
from utils.loggers import setup_logger

# Logger config

logger = setup_logger


def main(page: ft.page):
    """
    Main Flet application function

    Args:
        page: Flet page object that controls the window
    """

    # windows config
    Page.title = "Workapp- the smart way to get a job!"
    page.window.width = 1200
    page.window.heigth = 800
    page.window.min_width = 800
    page.window.min_width = 600

    # application theme
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=secondary=background=)
    )
