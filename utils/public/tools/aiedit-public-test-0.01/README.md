# RTCW AI Editor

A desktop editor for Return to Castle Wolfenstein `.ai` script files.

## Features
- Load multiple `.ai` files at once
- Browse all entities per file with a filter box
- Edit `attributes` (health, aggression, aim_accuracy, fov, etc.) with proper form controls
- Raw script editor with syntax highlighting for advanced edits
- All-entities overview table across all loaded files — double-click to jump
- Find & Replace attribute values across all files at once
- Bulk Set — apply one attribute value to every entity in every file
- Dark theme, saves back in original format preserving comments

## Running from source

1. Install Python 3.9+ from https://python.org
2. Install dependencies:
   ```
   pip install PyQt5
   ```
3. Run:
   ```
   python aiedit.py
   ```

## Compiling to .exe (Windows)

Run `build_exe.bat` — it will install PyInstaller and produce `dist\RTCW_AI_Editor.exe`.
Or manually:
```
pip install pyinstaller
pyinstaller --onefile --windowed --name "RTCW_AI_Editor" rtcw_ai_editor.py
```

## Usage tips
- Drag `.ai` files onto the exe to open them directly
- Use **Edit > Bulk Set Attribute** to e.g. set all `starting_health` to 50 across every entity
- Use **Edit > Find & Replace** to swap one specific value to another
- The **All Entities** tab gives an overview spreadsheet — double-click any row to jump to that entity
- Raw edits take effect when you click "Apply raw changes"