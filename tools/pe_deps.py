#!/usr/bin/env python3
"""Print the DLLs a Windows program loads from its own folder, one per line.

vendor_tesseract_windows.ps1 uses this to copy tesseract.exe with exactly the libraries it
needs - the Windows counterpart of dylibbundler on macOS - instead of the whole Tesseract
install folder (which also holds the training tools, their manuals, Java jars and an
uninstaller, none of which the app uses).

    python tools/pe_deps.py "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

Follows imports and delay-loaded imports recursively; DLLs that are not in the program's
folder (Windows system DLLs such as kernel32.dll) are left out. Needs pefile, which
PyInstaller installs on Windows.
"""

from __future__ import annotations

import sys
from pathlib import Path


def local_dependencies(exe: Path) -> list[str]:
    import pefile

    folder = exe.parent
    local = {p.name.lower(): p.name for p in folder.iterdir() if p.suffix.lower() == ".dll"}
    seen: set[str] = set()
    todo = [exe]
    while todo:
        current = todo.pop()
        pe = pefile.PE(str(current), fast_load=True)
        pe.parse_data_directories(directories=[
            pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"],
            pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT"],
        ])
        for attr in ("DIRECTORY_ENTRY_IMPORT", "DIRECTORY_ENTRY_DELAY_IMPORT"):
            for entry in getattr(pe, attr, []):
                name = entry.dll.decode("ascii", "replace").lower()
                if name in local and name not in seen:
                    seen.add(name)
                    todo.append(folder / local[name])
        pe.close()
    return sorted(local[n] for n in seen)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    exe = Path(argv[1])
    if not exe.is_file():
        print(f"not found: {exe}", file=sys.stderr)
        return 1
    for name in local_dependencies(exe):
        print(name)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
