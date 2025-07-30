@echo off
setlocal enabledelayedexpansion

echo Setting up pdf2gif "Send to" integration...
echo.

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
set "BATCH_FILE=%SCRIPT_DIR%pdf2gif-converter.bat"

REM Check if the batch file exists
if not exist "%BATCH_FILE%" (
    echo ERROR: pdf2gif-converter.bat not found in %SCRIPT_DIR%
    echo Please make sure this script is in the same directory as pdf2gif-converter.bat
    pause
    exit /b 1
)

REM Get the Send to folder path
for /f "tokens=2*" %%a in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v "SendTo" 2^>nul') do set "SEND_TO_FOLDER=%%b"

REM If registry query fails, use default path
if not defined SEND_TO_FOLDER (
    set "SEND_TO_FOLDER=%APPDATA%\Microsoft\Windows\SendTo"
)

echo Found Send to folder: %SEND_TO_FOLDER%
echo.

REM Create the shortcut
echo Creating shortcut in Send to folder...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SEND_TO_FOLDER%\Convert PDF to GIF.lnk'); $Shortcut.TargetPath = '%BATCH_FILE%'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.Description = 'Convert PDF to GIF using pdf2gif'; $Shortcut.Save()}"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo SUCCESS: pdf2gif "Send to" integration has been set up!
    echo.
    echo You can now:
    echo 1. Right-click on any PDF file
    echo 2. Hover over "Send to"
    echo 3. Click "Convert PDF to GIF"
    echo.
    echo To remove this integration, run remove-send-to-menu.bat
) else (
    echo.
    echo ERROR: Failed to create shortcut. Please try running as Administrator.
)

echo.
pause 