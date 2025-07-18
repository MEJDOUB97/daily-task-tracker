@echo off
REM Daily Task Tracker Pro - Windows Launcher
set "APP_DIR=%~dp0"
cd /d "%APP_DIR%"

echo Starting Daily Task Tracker Pro...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

if not exist "task_tracker.py" (
    echo task_tracker.py not found
    pause
    exit /b 1
)

python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing CustomTkinter...
    pip install customtkinter
)

python task_tracker.py

if %errorlevel% neq 0 (
    echo Error occurred. Press any key to exit.
    pause >nul
)
