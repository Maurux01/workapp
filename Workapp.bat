@echo off
REM Workapp — doble clic y abre la app de escritorio / double-click to open desktop app
cd /d "%~dp0"
python --version >nul 2>&1 || (echo Instala Python 3.10+ desde https://www.python.org/downloads/ && pause && exit /b 1)
python -c "import flask" >nul 2>&1 || (echo Instalando dependencias... && pip install -r requirements.txt)
python main_desktop.py
if errorlevel 1 (echo. && echo La app se cerro con un error. && pause)
