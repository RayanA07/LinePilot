# -*- mode: python ; coding: utf-8 -*-
#
# macOS build: dist/Digitizer.app (a folder bundle, which is what macOS expects). The
# Windows twin is digitizer.spec; both take their excludes, version and names from
# tools/build_common.py so they bundle the same things. Run through build_macos.sh, which
# makes a clean build environment from constraints.txt, vendors the pinned Tesseract first,
# and afterwards stamps LSMinimumSystemVersion and signs the result.

import sys
from pathlib import Path

block_cipher = None
root = Path(SPECPATH)
sys.path.insert(0, str(root.parent / "tools"))
import build_common  # noqa: E402

APP = "Digitizer"
VERSION = build_common.version_of(root)

datas = [(str(root / "version.json"), ".")]

# Tesseract OCR runtime bundled from Digitizer/vendor/tesseract (self-contained OCR).
# vendor/ is gitignored, so a fresh clone does not have it - run vendor_tesseract_macos.sh
# (build_macos.sh does). Without it the app has no OCR on anyone else's Mac, so say so loudly.
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

# make_macos_icons.py writes assets/digitizer.icns from the same digitizer.ico Windows uses.
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
    excludes=build_common.excludes(APP),
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP,
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
    name=APP,
)

app = BUNDLE(
    coll,
    name=f"{APP}.app",
    icon=icon,
    bundle_identifier=build_common.APPS[APP]["bundle_id"],
    version=VERSION,
    info_plist=build_common.mac_info_plist(APP, VERSION),
)
