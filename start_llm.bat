@echo off
setlocal enabledelayedexpansion

echo.
echo =======================================
echo  HireLens
echo =======================================
echo.

REM Check if Ollama is installed
where ollama >nul 2>nul
if !errorlevel! neq 0 (
    echo ERROR: Ollama not found
    echo.
    echo STEPS TO FIX:
    echo 1. Go to https://ollama.ai
    echo 2. Download and install
    echo 3. Restart computer
    echo 4. Run this file again
    echo.
    pause
    exit /b 1
)

echo Starting Ollama server...
start ollama serve
timeout /t 4

echo.
echo Starting app at http://localhost:8501
echo.
streamlit run app_llm.py

pause
