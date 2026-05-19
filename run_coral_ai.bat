@echo off
title CoralAI - Smart Coral Health Assessment
echo ======================================================
echo    Starting CoralAI Web Application...
echo ======================================================
echo.

:: 1. Navigate to Project Root (Relative to this script)
cd /d "%~dp0"

:: 2. Pre-flight checks
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found at .venv\
    echo Please run 'python -m venv .venv' and 'pip install -r 04_Web_Application\requirements.txt'
    pause
    exit /b 1
)

set "MODEL_PATH=02_Modelling\efficientnetb0_coral\models"
if not exist "%MODEL_PATH%" (
    echo [ERROR] Model directory not found: %MODEL_PATH%
    echo Please check the path in app.py and ensure models are downloaded.
    pause
    exit /b 1
)

:: 3. Launch using virtual environment Python
echo [OK] Starting server with virtual environment Python...
echo [OK] Model: EfficientNet-V4 Robust (ENSEMBLE)
echo [OK] Template: Premium Dashboard (design9.html)
echo.

:: 4. Run the application in the background
start /B .venv\Scripts\python.exe "04_Web_Application\app.py"

:: 5. Wait for models to load and server to start
echo [INFO] Waiting for server to start (loading ensemble)...
timeout /t 15 /nobreak >nul

:: 6. Open Browser to Home (defaults to design9)
echo [INFO] Opening browser...
start "" "http://localhost:5000/"

:: 7. Keep window open so server keeps running
echo.
echo [OK] Server is running at http://localhost:5000/
echo [OK] Use CTRL+C in this window to stop.
pause >nul

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Server crashed or closed unexpectedly.
    echo Common fixes:
    echo  - Ensure Python is installed and on PATH
    echo  - Run 'pip install -r 04_Web_Application\requirements.txt' if modules are missing
    echo  - Check that model files exist in %MODEL_PATH%
    pause
)
