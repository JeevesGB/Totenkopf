# Totenkopf

A Hardmode Mod for **Return To Castle Wolfenstein** that tweaks enemy parameters and weapons to increase difficulty.
> ⚠️ **Work in progress**

---

# Change Notes

**`escape1`** - *`Enemy Health set to 100, Flamethrower added and made more aggressive`*

**`escape2`** - *`Enemy Health set to 100, Venom added and made more aggressive`*

**`tram`** - *`Enemy Health set to 100 and made more aggressive`*

**`village1`** - *`Enemy Health set to 100, Flamethrower added and made more aggressive`*

**`crypt1`** - *`Enemy / Zombie Health set to 100 and made more aggressive`*

**`crypt2`** - *`Enemy / Zombie Health set to 100 and made more aggressive`*

**`church`** - *`Enemy Health set to 100 and made more aggressive`*

**`boss1`** - *`Boss / Zombie Health increased`*

**`forest`** - *`Enemy Health set to 100`*

**`rocket`** - *`Enemy Health set to 100 and made more aggressive`*

**`baseout`** - *`Enemy Health / Accuracy set to 100 and made more aggressive`*

**`assault`** - *`Enemy Health / Accuracy set to 100 and made more aggressive`*

**`sfm`** - *`TBD`*

**`factory`** - *`TBD`*

**`trainyard`** - *`TBD`*

**`swf`** - *`TBD`*

**`norway`** - *`TBD`*

**`xlabs`** - *`TBD`*

**`boss2`** - *`TBD`*

**`dam`** - *`Enemy Health / Accuracy set to 100 and made more aggressive`*

**`village2`** - *`TBD`*

**`chateau`** - *`TBD`*

**`dark`** - *`TBD`*

**`dig`** - *`TBD`*

**`castle`** - *`TBD`*

**`end`** - *`TBD`*

---

# Requirements

- **[iortcw](https://github.com/iortcw/iortcw)** — required to run this mod.
- **Making a backup of your original RTCW installation is strongly recommended.**

---

# Installation

Put **`_totenkopf.pk3`** into your **`RTCW/Main`** directory. Optionally you can copy **`autoexec.cfg`** to **`RTCW/Main`**.

### autoexec.cfg

```
set devdll 1
com_introplayed 1
```

---

# Console Commands

**[Console commands](utils/public/docs/CMDLIST.MD)**

---

# Cvars

***CVars** (Console Variables) are configurable settings built into the Quake III engine that RTCW runs on. They control everything from graphics and sound to gameplay and network behaviour, and can be changed at runtime by typing them directly into the game console. Most are saved to your config file and persist between sessions.*

You can generate a list in the console by typing `/cvarlist`.

You are then able to type `/condump cvar.txt` into the console and this will then save to your `Documents/RTCW/main` directory.

**[CVar Reference](utils/public/docs/CVARS.md)**

---

# Utils

Within the *`utils/public/bat`* folder you will find **`bsp2map.bat`**. This simple batch file will allow you to convert the original map .bsp files located within **`RTCW/Main/pak0.pk3`** back into editable .map files. 

```
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
```
Open **`bsp2map.bat`** in a text editor and put your path's within:

-`set "Q3MAP2="`

-`set "INPUTDIR="`

-`set "OUTPUTDIR="`

Save and then run the file. 

**The process may take some time and some textures/shaders may not convert correctly**
