@echo off
REM ===========================================================================
REM  LinePilot Accuracy Tester - one-click Windows build  (code  ->  AccuracyTester.exe)
REM
REM  Double-click this file, or run it in a terminal:   build.cmd
REM  It makes a clean build environment with the pinned packages and runs
REM  PyInstaller via accuracytester.spec (see build_windows.ps1).
REM
REM  Output:  dist\AccuracyTester.exe
REM  Reuse the existing build environment with:   build.cmd -SkipInstall
REM
REM  Requires Python 3.12 (the "py" launcher). Get it from https://python.org
REM ===========================================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build_windows.ps1" %*
echo.
echo Done. If it succeeded, your app is at:  %~dp0dist\AccuracyTester.exe
echo.
pause
