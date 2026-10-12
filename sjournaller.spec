# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for SJournaller.

Build:  pyinstaller sjournaller.spec
"""

import os
import sys

block_cipher = None

# Determine if icon exists
icon_path = 'assets/icon.ico'
if not os.path.isfile(icon_path):
    icon_path = None

a = Analysis(
    ['sjournaller/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'sjournaller',
        'sjournaller.main',
        'sjournaller.constants',
        'sjournaller.config',
        'sjournaller.crypto',
        'sjournaller.database',
        'sjournaller.ui',
        'sjournaller.ui.styles',
        'sjournaller.ui.login_dialog',
        'sjournaller.ui.setup_dialog',
        'sjournaller.ui.main_window',
        'sjournaller.ui.template_dialog',
        'sjournaller.ui.export_dialog',
        'sjournaller.ui.settings_dialog',
        'sjournaller.resources',
        'sjournaller.resources.icons',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter', 'matplotlib', 'numpy', 'scipy',
        'PIL', 'pytest', 'ruff',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SJournaller',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # GUI app, no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
    version='version_info.txt',   # Windows version resource
)