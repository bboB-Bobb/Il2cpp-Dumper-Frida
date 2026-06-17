@echo off
setlocal
color 0F

echo ===================================================
echo     Il2Cpp Dumper - Environment Setup
echo ===================================================
echo Checking system requirements...
echo.

set NEEDS_RESTART=0

:: Check Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [INFO] Python not found. Installing Python 3.12 via Winget...
    winget install --id Python.Python.3.12 -e --silent --accept-package-agreements --accept-source-agreements
    IF %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Python automatic installation failed.
        echo Please install Python manually from https://www.python.org/
        pause
        exit /b
    )
    echo [OK] Python installed successfully.
    set NEEDS_RESTART=1
) ELSE (
    echo [OK] Python is installed.
)

:: Check Node.js
npm --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [INFO] Node.js not found. Installing Node.js via Winget...
    winget install --id OpenJS.NodeJS -e --silent --accept-package-agreements --accept-source-agreements
    IF %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Node.js automatic installation failed.
        echo Please install Node.js manually from https://nodejs.org/
        pause
        exit /b
    )
    echo [OK] Node.js installed successfully.
    set NEEDS_RESTART=1
) ELSE (
    echo [OK] Node.js is installed.
)

IF "%NEEDS_RESTART%"=="1" (
    echo.
    echo ============================================================
    echo   RESTART REQUIRED
    echo   Core dependencies were installed. You must close this
    echo   window and run setup.bat again to update the system PATH.
    echo ============================================================
    pause
    exit /b
)

echo.
echo Installing global Python dependency: frida-tools...
pip install frida-tools --quiet

echo.
echo Installing local Node.js dependencies...
npm install --silent

echo.
echo ===================================================
echo   Setup Complete. You can now execute run.bat.
echo ===================================================
pause
