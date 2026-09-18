@echo off
REM Workapp — doble clic y abre la app de escritorio SIN ventana de consola.
REM Double-click to open the desktop app with NO console window.
cd /d "%~dp0"
python --version >nul 2>&1 || (echo Instala Python 3.10+ desde https://www.python.org/downloads/ && pause && exit /b 1)
REM Solo la primera vez (o si faltan deps) veras la consola instalando.
python -c "import flask, requests, bs4, lxml, pypdf, dotenv" >nul 2>&1 || (echo Instalando dependencias, espera... && pip install -r requirements.txt && echo Listo, abriendo Workapp...)
REM pythonw = Python sin consola. Errores quedan en Workapp-error.log
start "" pythonw main_desktop.py
