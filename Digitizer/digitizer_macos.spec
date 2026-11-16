# -*- mode: python ; coding: utf-8 -*-
#
# macOS counterpart of digitizer.spec: builds dist/Digitizer.app (a folder bundle, which is
# what macOS expects) instead of a one-file exe. Run through build_macos.sh, which vendors
# Tesseract first and then stamps LSMinimumSystemVersion and signs the result.

import json
from pathlib import Path


block_cipher = None
root = Path(SPECPATH)

# The version shown in Finder's Get Info comes from version.json, like every other version
# string in the app. It was hardcoded here before and shipped 2.13 / 2.15 builds whose
# Info.plist still said 2.12.
VERSION = json.loads((root / "version.json").read_text(encoding="utf-8"))["version"]

datas = [(str(root / "version.json"), ".")]

# Tesseract OCR runtime bundled from Digitizer/vendor/tesseract (self-contained OCR).
# vendor/ is gitignored, so a fresh clone does not have it - run vendor_tesseract_macos.sh
# (build_macos.sh does). Without it the app silently falls back to a Homebrew Tesseract on
# the build machine and has no OCR on anyone else's Mac, so say so loudly.
vendor_tesseract = root / "vendor" / "tesseract"
if vendor_tesseract.exists() and any(path.is_file() for path in vendor_tesseract.rglob("*")):
    datas.append((str(vendor_tesseract), "vendor/tesseract"))
else:
    import warnings

    warnings.warn(
        "\n"
        "    ****************************************************************\n"
        "    WARNING: vendor/tesseract not found -- building an app with NO OCR.\n"
        "    Axis Scale Detection will not work for anyone you give this app to.\n"
        "    Run 'bash vendor_tesseract_macos.sh' (or build_macos.sh) first.\n"
        "    ****************************************************************\n",
        stacklevel=1,
    )

# Icon is optional: make_macos_icons.py writes assets/digitizer.icns from the Windows .ico.
icon_path = root / "assets" / "digitizer.icns"
icon = str(icon_path) if icon_path.is_file() else None

hiddenimports = [
    "openpyxl",
    "pytesseract",
    "PIL.Image",
    "PIL.ImageEnhance",
    "PIL.ImageFilter",
    "PIL.ImageOps",
]

a = Analysis(
    [str(root / "digitizer_desktop.py")],
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
    name="Digitizer",
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
    name="Digitizer",
)

app = BUNDLE(
    coll,
    name="Digitizer.app",
    icon=icon,
    bundle_identifier="com.rayana07.datadigitizer.digitizer",
    version=VERSION,
    info_plist={
        "CFBundleName": "Digitizer",
        "CFBundleDisplayName": "LinePilot Digitizer",
        "CFBundleShortVersionString": VERSION,
        "CFBundleVersion": VERSION,
        "NSHumanReadableCopyright": "LinePilot Digitizer - Apache License 2.0",
        "NSHighResolutionCapable": True,
    },
)
