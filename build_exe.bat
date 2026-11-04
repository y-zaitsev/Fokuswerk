@echo off
title Fokuswerk Builder

echo ==================================
echo        Building Fokuswerk
echo ==================================

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --windowed --onefile --noupx --name Fokuswerk main.py

if errorlevel 1 (
    echo.
    echo BUILD FAILED!
    pause
    exit /b 1
)

echo.
echo BUILD SUCCESSFUL!
echo Your application is in dist\Fokuswerk.exe
pause
