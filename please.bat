@echo off
REM ===============================
REM BSOD Command Launcher (Portable)
REM ===============================

REM Get the folder where this CMD file lives
set BASE=C:\BSOD

REM Trim trailing backslash just in case
if "%BASE:~-1%"=="\" set BASE=%BASE:~0,-1%

REM First and second arguments
set CMD=%1
set ARG=%2

REM ===== No command given =====
if "%CMD%"=="" (
    echo.
    echo Please provide a command.
    echo Available commands:
    echo    please bsod
    echo    please bsod editor
    echo    please bsod stock
    echo.
    exit /b
)

REM ===== Command Routing =====
if /i "%CMD%"=="bsod" (
    if /i "%ARG%"=="editor" (
        python "%BASE%\\bsod_editor.py"
        exit /b
    ) else if /i "%ARG%"=="stock" (
        python "%BASE%\\bsod.py" --stock
        exit /b
    ) else (
        python "%BASE%\\bsod.py"
        exit /b
    )
)

REM Unknown command fallback
echo.
echo Unknown command: %1 %2
echo Available commands:
echo    please bsod
echo    please bsod editor
echo    please bsod stock
echo.
exit /b

