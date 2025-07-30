@echo off
setlocal enabledelayedexpansion

REM Check if any files were provided
if "%~1"=="" (
    echo Error: No PDF files selected.
    echo.
    echo Usage: Drag and drop PDF files onto this script, or use "Send to" menu.
    pause
    exit /b 1
)

REM Activate conda environment (replace 'bio11' with your actual environment name)
call conda activate bio11

REM Initialize counters
set "total_files=0"
set "successful_conversions=0"
set "failed_conversions=0"

echo Starting PDF to GIF conversion...
echo.

REM Process each file passed as an argument
:process_files
set "pdf_file=%~1"

REM Check if we've processed all files
if "%pdf_file%"=="" goto :end

REM Increment total file counter
set /a "total_files+=1"

REM Check if the file exists
if not exist "%pdf_file%" (
    echo [%total_files%] ERROR: File does not exist: %pdf_file%
    set /a "failed_conversions+=1"
    goto :next_file
)

REM Check if it's a PDF file
if /i not "%pdf_file:~-4%"==".pdf" (
    echo [%total_files%] ERROR: File is not a PDF: %pdf_file%
    set /a "failed_conversions+=1"
    goto :next_file
)

REM Convert the PDF to GIF
echo [%total_files%] Converting: %pdf_file%
pdf2gif "%pdf_file%"

REM Check if the conversion was successful
if %errorlevel% equ 0 (
    echo [%total_files%] SUCCESS: %pdf_file%
    set /a "successful_conversions+=1"
) else (
    echo [%total_files%] ERROR: Failed to convert %pdf_file%
    set /a "failed_conversions+=1"
)

:next_file
REM Move to next argument
shift
goto :process_files

:end
echo.
echo ========================================
echo Conversion Summary:
echo Total files processed: %total_files%
echo Successful conversions: %successful_conversions%
echo Failed conversions: %failed_conversions%
echo ========================================

if %failed_conversions% gtr 0 (
    echo.
    echo Some conversions failed. Check the error messages above.
) else if %successful_conversions% gtr 0 (
    echo.
    echo All conversions completed successfully!
    echo Output files saved in the same directories as the input files.
)

echo.
pause 