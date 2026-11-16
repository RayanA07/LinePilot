# -*- mode: python ; coding: utf-8 -*-

import json
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules


block_cipher = None
root = Path(SPECPATH)

# Version for Finder's Get Info, read from version.json (was hardcoded to 2.12).
VERSION = json.loads((root / "version.json").read_text(encoding="utf-8"))["version"]

datas = [(str(root / "version.json"), ".")]
datas += collect_data_files("matplotlib")
datas += collect_data_files("tkinterdnd2")

hiddenimports = collect_submodules("tkinterdnd2")

# Icon is optional: if assets/accuracytester.icns is missing, build without one.
icon_path = root / "assets" / "accuracytester.icns"
icon = str(icon_path) if icon_path.is_file() else None

a = Analysis(
    [str(root / "accuracytester_desktop.py")],
    pathex=[str(root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="AccuracyTester",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="AccuracyTester",
)

app = BUNDLE(
    coll,
    name="AccuracyTester.app",
    icon=icon,
    bundle_identifier="com.rayana07.datadigitizer.accuracytester",
    version=VERSION,
    info_plist={
        "CFBundleName": "AccuracyTester",
        "CFBundleDisplayName": "LinePilot Accuracy Tester",
        "CFBundleShortVersionString": VERSION,
        "CFBundleVersion": VERSION,
        "NSHumanReadableCopyright": "LinePilot Digitizer - Apache License 2.0",
        "NSHighResolutionCapable": True,
    },
)
