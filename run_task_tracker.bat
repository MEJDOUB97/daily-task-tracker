@echo off
REM Daily Task Tracker Pro - Windows Launcher
REM This script runs the Task Tracker application

REM Get the directory where this batch file is located
set "APP_DIR=%~dp0"

REM Change to the application directory
cd /d "%APP_DIR%"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if the main application file exists
if not exist "task_tracker.py" (
    echo task_tracker.py not found in current directory
    echo Please make sure you're running this from the correct folder
    pause
    exit /b 1
)

REM Check if CustomTkinter is installed
python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo CustomTkinter is not installed. Installing now...
    pip install customtkinter
    if %errorlevel% neq 0 (
        echo Failed to install CustomTkinter
        echo Please run: pip install customtkinter
        pause
        exit /b 1
    )
)

REM Run the application
echo Starting Daily Task Tracker Pro...
python task_tracker.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo Application exited with error code %errorlevel%
    pause
)