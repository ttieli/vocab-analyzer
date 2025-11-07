@echo off
REM Vocab Analyzer Web Server Startup Script for Windows
REM This script activates the virtual environment and starts the Flask web server

echo ======================================================================
echo   📚 Vocabulary Analyzer - Web Interface
echo ======================================================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\" (
    echo ❌ Error: Virtual environment not found!
    echo    Please run: python -m venv venv
    echo    Then install dependencies: pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ❌ Error: Flask not installed!
    echo    Please run: pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ Environment ready
echo.
echo 🚀 Starting web server...
echo    Server will be available at: http://127.0.0.1:5000
echo.
echo    Press CTRL+C to stop the server
echo ======================================================================
echo.

REM Start the Flask application
python -m vocab_analyzer.web.app

pause
