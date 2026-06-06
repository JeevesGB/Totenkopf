@echo off
setlocal

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found in PATH.
    echo.
    echo To add Python to PATH:
    echo.
    echo   OPTION 1 - Reinstall Python ^(easiest^):
    echo     1. Go to https://www.python.org/downloads/
    echo     2. Run the installer
    echo     3. Check "Add python.exe to PATH" on the first screen
    echo     4. Click Install Now
    echo.
    echo   OPTION 2 - Add manually:
    echo     1. Search "environment variables" in the Start menu
    echo     2. Click "Edit the system environment variables"
    echo     3. Click "Environment Variables..." button
    echo     4. Under "User variables", select "Path" and click Edit
    echo     5. Click New and add your Python folder, e.g.:
    echo        C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python314\
    echo        C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python314\Scripts\
    echo     6. Click OK on all windows, then restart this terminal
    echo.
    echo   TIP: To find where Python is installed, search for "python.exe"
    echo        in File Explorer.
    echo.
    pause
    exit /b 1
)

:: Remove any __pycache__ folders left over from previous runs
for /d /r "%~dp0src" %%d in (__pycache__) do rd /s /q "%%d" 2>nul

:: Run the editor
echo Running RTCW AI Editor...
cd /d "%~dp0src"
python main.py %*

if %errorlevel% neq 0 (
    echo.
    echo Script exited with error code %errorlevel%.
) else (
    echo Done.
)

pause
endlocal