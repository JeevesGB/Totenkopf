@echo off
setlocal 

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found in PATH.
    echo.
    echo To add Python to PATH:
    echo.
    echo   OPTION 1 - Install Python:
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
    echo        C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\
    echo        C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\Scripts\
    echo     6. Click OK on all windows, then restart this terminal
    echo.
    echo   TIP: To find where Python is installed, search for "python.exe"
    echo        in File Explore
    pause
    exit /b 1
)

echo Running aiedit.py 
python "%~dp0aiedit.py"

if %errorlevel% neq 0 (
    echo Script exited with error code %errorlevel%.
) else (
    echo Done.
)

pause 
endlocal