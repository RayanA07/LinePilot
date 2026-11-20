"""Settings shared by the Windows and macOS PyInstaller specs.

The four .spec files (digitizer.spec, digitizer_macos.spec, accuracytester.spec,
accuracytester_macos.spec) import their exclude lists, version metadata and display names
from here, so a Windows build and a macOS build of the same app can never be configured
differently. tools/bundle_inventory.py then checks the finished apps really match.
"""

from __future__ import annotations

import json
from pathlib import Path

COPYRIGHT = "LinePilot Digitizer - Apache License 2.0"

# Never bundled into either app: test tools, the build tool itself, and certifi (only used
# by matplotlib to download images from URLs, which the Accuracy Tester never does).
_COMMON_EXCLUDES = [
    "PyInstaller", "pytest", "_pytest", "pluggy", "iniconfig", "pygments",
    "scipy", "sklearn", "IPython", "certifi",
]

APPS = {
    "Digitizer": {
        "display_name": "LinePilot Digitizer",
        "bundle_id": "com.rayana07.datadigitizer.digitizer",
        # The Digitizer is a Qt app: it never imports the Accuracy Tester's plotting stack.
        "excludes": _COMMON_EXCLUDES + [
            "matplotlib", "pandas", "tkinter", "_tkinter", "tkinterdnd2",
        ],
    },
    "AccuracyTester": {
        "display_name": "LinePilot Accuracy Tester",
        "bundle_id": "com.rayana07.datadigitizer.accuracytester",
        # The Accuracy Tester is a Tk app: keep matplotlib from pulling in a Qt backend.
        "excludes": _COMMON_EXCLUDES + [
            "PyQt6", "PyQt5", "PySide6", "PySide2", "pytesseract", "openpyxl",
        ],
    },
}


# Tcl/Tk files that the Python distributions on Windows and macOS package differently and
# that Tk never uses: Tcl's own timezone database (only for `clock -timezone`), its C
# example sources, its test framework and its SQLite database driver. Both Accuracy Tester
# specs drop them, so the .exe and the .app carry the same Tcl/Tk library.
_UNUSED_TCL = ("_tcl_data/tzdata/", "AppInit.c", "/tcltest-", "/tdbc/")


def drop_unused_tcl_files(datas):
    """Filter a PyInstaller TOC (Analysis.datas) with the rule above."""
    out = []
    for entry in datas:
        dest = str(entry[0]).replace("\\", "/")
        if dest.startswith(("_tcl_data/", "_tk_data/", "tcl8/")) and any(p in dest for p in _UNUSED_TCL):
            continue
        out.append(entry)
    return type(datas)(out) if not isinstance(datas, list) else out


def version_of(app_dir: Path) -> str:
    return json.loads((Path(app_dir) / "version.json").read_text(encoding="utf-8"))["version"]


def excludes(app: str) -> list[str]:
    return list(APPS[app]["excludes"])


def mac_info_plist(app: str, version: str) -> dict:
    """Info.plist entries for the .app (the macOS counterpart of windows_version_info)."""
    return {
        "CFBundleName": app,
        "CFBundleDisplayName": APPS[app]["display_name"],
        "CFBundleShortVersionString": version,
        "CFBundleVersion": version,
        "NSHumanReadableCopyright": COPYRIGHT,
        "NSHighResolutionCapable": True,
    }


def windows_version_info(app: str, version: str):
    """The version resource of the .exe (Properties -> Details), the Windows counterpart of
    the Info.plist above: same display name, version and copyright."""
    from PyInstaller.utils.win32.versioninfo import (
        FixedFileInfo, StringFileInfo, StringStruct, StringTable, VarFileInfo, VarStruct,
        VSVersionInfo,
    )

    parts = [int(p) for p in version.split(".") if p.isdigit()][:4]
    nums = tuple(parts + [0] * (4 - len(parts)))
    return VSVersionInfo(
        ffi=FixedFileInfo(filevers=nums, prodvers=nums, mask=0x3F, flags=0x0, OS=0x40004,
                          fileType=0x1, subtype=0x0, date=(0, 0)),
        kids=[
            StringFileInfo([StringTable("040904B0", [
                StringStruct("FileDescription", APPS[app]["display_name"]),
                StringStruct("FileVersion", version),
                StringStruct("InternalName", app),
                StringStruct("LegalCopyright", COPYRIGHT),
                StringStruct("OriginalFilename", f"{app}.exe"),
                StringStruct("ProductName", APPS[app]["display_name"]),
                StringStruct("ProductVersion", version),
            ])]),
            VarFileInfo([VarStruct("Translation", [1033, 1200])]),
        ],
    )
