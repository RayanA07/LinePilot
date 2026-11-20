@echo off
REM ===========================================================================
REM  LinePilot Digitizer - one-click Windows build  (code  ->  Digitizer.exe)
REM
REM  Double-click this file, or run it in a terminal:   build.cmd
REM  It makes a clean build environment with the pinned packages, vendors the
REM  pinned Tesseract OCR engine and runs PyInstaller via digitizer.spec
REM  (see build_windows.ps1).
REM
REM  Output:  dist\Digitizer.exe
REM  Reuse the existing build environment with:   build.cmd -SkipInstall
REM
REM  Requires Python 3.12 (the "py" launcher). Get it from https://python.org
REM ===========================================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build_windows.ps1" %*
echo.
echo Done. If it succeeded, your app is at:  %~dp0dist\Digitizer.exe
echo.
pause
