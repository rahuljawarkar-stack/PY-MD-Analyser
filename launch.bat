@echo off
setlocal

echo =========================================
echo Starting PocketOccupancy Analyzer...
echo =========================================

:: Check if the portable Python directory exists
set PORTABLE_PYTHON="D:\Portable_python_3.10_new\App\Python\python.exe"
set PYTHON_CMD=python

if exist %PORTABLE_PYTHON% (
    echo Found portable Python at D:\Portable_python_3.10_new...
    set PYTHON_CMD=%PORTABLE_PYTHON%
) else (
    echo Portable Python not found. Falling back to system Python...
)

:: Install requirements automatically
echo Checking dependencies...
%PYTHON_CMD% -m pip install -r requirements.txt > nul 2>&1

:: Run the application
echo Launching GUI...
%PYTHON_CMD% main.py

if %errorlevel% neq 0 (
    echo.
    echo An error occurred while running the application.
    pause
)

endlocal
