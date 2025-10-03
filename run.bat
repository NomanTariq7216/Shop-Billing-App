@echo off
REM Launcher script for Shop Billing System (Windows)

echo Starting Shop Billing System...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed!
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Run the application
python main.py

pause
