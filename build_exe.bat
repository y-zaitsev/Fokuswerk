@echo off
title Mindrift Builder

echo ==================================
echo        Building Mindrift
echo ==================================

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --windowed --onefile --name Mindrift main.py

if errorlevel 1 (
    echo.
    echo BUILD FAILED!
    pause
    exit /b 1
)

echo.
echo BUILD SUCCESSFUL!
echo Your application is in dist\Mindrift.exe
pause
