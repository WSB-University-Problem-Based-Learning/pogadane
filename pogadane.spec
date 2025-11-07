# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Pogadane
Creates a single-file executable (.exe) for Windows

Usage:
    pyinstaller pogadane.spec

Output:
    dist/Pogadane.exe - Single file application (~100-200 MB)
"""

import sys
from pathlib import Path

# Project paths
project_root = Path.cwd()
src_path = project_root / 'src'

block_cipher = None

# Collect all data files
datas = [
    # Configuration files (optional - will be created if missing)
    ('.config/config.py', '.config'),
]

# Collect hidden imports (libraries not auto-detected)
hiddenimports = [
    # Flet and dependencies
    'flet',
    'flet.core',
    'flet.auth',
    
    # Pogadane modules
    'pogadane',
    'pogadane.gui_flet',
    'pogadane.backend',
    'pogadane.config_loader',
    'pogadane.constants',
    'pogadane.file_utils',
    'pogadane.text_utils',
    'pogadane.llm_providers',
    'pogadane.transcription_providers',
    'pogadane.types',
    'pogadane.gui_utils',
    'pogadane.gui_utils.results_manager',
    
    # Google AI
    'google.generativeai',
    'google.ai',
    
    # Transcription libraries (optional - only if installed)
    # Uncomment if you want to bundle these:
    # 'faster_whisper',
    # 'whisper',
    # 'transformers',
    # 'torch',
    
    # Other dependencies
    'yt_dlp',
    'py7zr',
]

# Analysis: scan the entry point
a = Analysis(
    ['run_gui_flet.py'],
    pathex=[str(src_path)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary packages to reduce size
        'matplotlib',
        'PIL',
        'tkinter',
        '_tkinter',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'notebook',
        'IPython',
        'sphinx',
        'pytest',
        'setuptools',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ: Create the archive
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

# EXE: Create the executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Pogadane',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress with UPX (if available)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path if you have one: 'res/icon.ico'
    # Single file bundle
    onefile=True,
)

# Optional: Create installer (requires NSIS or similar)
# Uncomment to create an installer instead of single file
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='Pogadane',
# )
