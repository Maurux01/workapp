@echo off
REM Workapp one-click installer for Windows
python --version || (echo Instala Python 3.10+ desde https://www.python.org/downloads/ && pause && exit /b 1)
python install_wizard.py
pause
