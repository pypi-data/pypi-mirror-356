@echo off
setlocal enabledelayedexpansion

echo Removing pdf2gif "Send to" integration...
echo.

REM Get the Send to folder path
for /f "tokens=2*" %%a in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v "SendTo" 2^>nul') do set "SEND_TO_FOLDER=%%b"

REM If registry query fails, use default path
if not defined SEND_TO_FOLDER (
    set "SEND_TO_FOLDER=%APPDATA%\Microsoft\Windows\SendTo"
)

echo Found Send to folder: %SEND_TO_FOLDER%
echo.

REM Check if the shortcut exists
set "SHORTCUT_PATH=%SEND_TO_FOLDER%\Convert to GIF.lnk"
if exist "%SHORTCUT_PATH%" (
    echo Found shortcut: %SHORTCUT_PATH%
    echo.
    
    REM Delete the shortcut
    echo Removing shortcut...
    del "%SHORTCUT_PATH%"
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo SUCCESS: pdf2gif "Send to" integration has been removed!
        echo.
        echo The "Convert to GIF" option will no longer appear in the Send to menu.
    ) else (
        echo.
        echo ERROR: Failed to remove shortcut. Please try running as Administrator.
    )
) else (
    echo.
    echo No pdf2gif shortcut found in the Send to folder.
    echo The integration may have already been removed or was never set up.
)

echo.
pause 