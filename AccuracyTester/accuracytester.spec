# -*- mode: python ; coding: utf-8 -*-
#
# Windows build: dist/AccuracyTester.exe, one file. The macOS twin is
# accuracytester_macos.spec; both take their excludes, version and names from
# tools/build_common.py so they bundle the same things. Run through build_windows.ps1.

import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None
root = Path(SPECPATH)
sys.path.insert(0, str(root.parent / "tools"))
import build_common  # noqa: E402

APP = "AccuracyTester"
VERSION = build_common.version_of(root)

datas = [(str(root / "version.json"), ".")]
datas += collect_data_files("matplotlib")
datas += collect_data_files("tkinterdnd2")

# tkinterdnd2 ships its own PyInstaller hook in tkinterdnd2/__pyinstaller; collecting that
# too would bundle PyInstaller itself into the app.
hiddenimports = collect_submodules("tkinterdnd2", filter=lambda name: "__pyinstaller" not in name)
# pandas needs the tzdata package on Windows (no system timezone database there); bundle it
# on macOS too so both apps carry the same timezone data instead of one using the OS copy.
hiddenimports += ["tzdata"]
datas += collect_data_files("tzdata")

a = Analysis(
    [str(root / "accuracytester_desktop.py")],
    pathex=[str(root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=build_common.excludes(APP),
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

a.datas = build_common.drop_unused_tcl_files(a.datas)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=APP,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # as on macOS; UPX-packed exes also trip antivirus scanners
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(root / "assets" / "accuracytester.ico"),
    version=build_common.windows_version_info(APP, VERSION),
)
