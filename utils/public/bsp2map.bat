@echo off
set "Q3MAP2=path\to\q3map2.exe"
set "INPUTDIR=path\to\input\directory"
set "OUTPUTDIR=path\to\output\directory"

if not exist "%OUTPUTDIR%" mkdir "%OUTPUTDIR%"

for %%f in ("%INPUTDIR%\*.bsp") do (
    echo Converting %%~nxf...
    "%Q3MAP2%" -game wolf -convert -format map -v "%%f"
    move "%%~dpnf.map" "%OUTPUTDIR%"
)

echo Done!
pause