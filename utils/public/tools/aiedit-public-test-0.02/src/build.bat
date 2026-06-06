@echo off
echo ============================================
echo  RTCW AI Editor - Build to .exe
echo ============================================
echo.

REM Install dependencies if not already installed
echo Installing dependencies...
pip install PyQt5 pyinstaller

echo.
echo Building .exe...
pyinstaller --onefile --windowed --name "AIEdit" aiedit.py

echo.
echo Done! Your .exe is in the dist\ folder.
pause