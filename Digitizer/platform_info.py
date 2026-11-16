"""Everything that differs between Windows, macOS and Linux, in one place.

The rest of the code is platform-neutral. Help text is written once, in its Windows form
(the platform the app started on), and `for_this_os` rewrites it on macOS / Linux at print
time: `py script.py` -> `python3 script.py`, `C:\\...` example paths -> home-folder paths,
`Digitizer.exe` -> `Digitizer.app`. On Windows the text is returned unchanged, byte for
byte. tools/check_help_text.sh runs in the macOS CI and fails if any Windows-only text
survives the rewrite, so a new example added later cannot leak through unnoticed.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path
from typing import Iterable, Optional

IS_WINDOWS = sys.platform == "win32"
IS_MAC = sys.platform == "darwin"

# Qt maps ControlModifier to the Command key on macOS, so a Ctrl+Z shortcut already *works*
# there as Cmd+Z; only the label shown to the user has to change.
UNDO_HINT = "⌘Z" if IS_MAC else "Ctrl+Z"

TESSERACT_BINARY = "tesseract.exe" if IS_WINDOWS else "tesseract"

if IS_WINDOWS:
    _SYSTEM_TESSERACT = (
        Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
        Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
    )
else:
    _SYSTEM_TESSERACT = (
        Path("/opt/homebrew/bin/tesseract"),  # Homebrew, Apple Silicon
        Path("/usr/local/bin/tesseract"),     # Homebrew, Intel Mac
        Path("/opt/local/bin/tesseract"),     # MacPorts
        Path("/usr/bin/tesseract"),           # Linux packages
    )


def tesseract_candidates(env_cmd: str, vendor_roots: Iterable[Path]) -> list[Path]:
    """Search order shared by AxisReader, Masking and digitizer_2_11: the TESSERACT_CMD
    override, then a vendored copy next to the code / inside the app bundle, then the
    standard install locations for this OS. Callers fall back to PATH afterwards."""
    out: list[Path] = []
    if env_cmd:
        out.append(Path(env_cmd))
    out.extend(Path(root) / "vendor" / "tesseract" / TESSERACT_BINARY for root in vendor_roots)
    out.extend(_SYSTEM_TESSERACT)
    return out


def find_tesseract(env_cmd: str, vendor_roots: Iterable[Path]) -> Optional[Path]:
    for candidate in tesseract_candidates(env_cmd, vendor_roots):
        if candidate.is_file():
            return candidate
    on_path = shutil.which("tesseract")
    return Path(on_path) if on_path else None


def missing_tesseract_message() -> str:
    if IS_WINDOWS:
        how = "Install Tesseract and add it to PATH"
    elif IS_MAC:
        how = "Install it with `brew install tesseract`"
    else:
        how = "Install it with your package manager (e.g. `sudo apt install tesseract-ocr`)"
    return (
        f"Tesseract OCR executable not found. {how}, "
        f"or set TESSERACT_CMD, or place it at vendor/tesseract/{TESSERACT_BINARY}."
    )


# ---- help text -----------------------------------------------------------------------------
# Ordered: the specific example paths first, then the generic drive-letter fallbacks.
# Paths inside a quoted digitizer_cli(...) call are not expanded by the shell, so they use a
# literal /Users/you/...; paths given straight to the shell use ~ or $HOME.
_PATH_REWRITES: tuple[tuple[str, str], ...] = (
    (r"C:\Users\User\Pictures\Screenshots\Example 2.png", "/Users/you/Pictures/Example 2.png"),
    (r"C:\Users\User\Downloads\testcli", "/Users/you/Downloads/testcli"),
    ("C:/Users/User/Downloads/out", "/Users/you/Downloads/out"),
    (r"C:\Users\User\Desktop\graph.png", "$HOME/Desktop/graph.png"),
    (r"C:\Users\User\Desktop\out", "$HOME/Desktop/out"),
    (r"C:\\charts", "~/Downloads/charts"),
    (r"C:\charts", "~/Downloads/charts"),
    (r"D:\\results", "~/Desktop/results"),
    (r"D:\results", "~/Desktop/results"),
    (r"C:\\out", "~/Desktop/out"),
    (r"C:\out", "~/Desktop/out"),
    ("C:/out", "~/Desktop/out"),
    ("Digitizer.exe", "Digitizer.app"),
    ("AccuracyTester.exe", "AccuracyTester.app"),
    ("%LOCALAPPDATA%", "~/Library/Application Support" if IS_MAC else "~/.local/share"),
)

# `py script.py` / `py -m ...` is the Windows Python launcher; elsewhere it is python3.
_PY_LAUNCHER = re.compile(r"(?<![\w.-])py (?=[\w-]+\.pyw?\b|-m\b)")


def for_this_os(text: str) -> str:
    """Return help/usage text with Windows-only commands and paths rewritten for this OS."""
    if IS_WINDOWS:
        return text
    for windows, other in _PATH_REWRITES:
        text = text.replace(windows, other)
    return _PY_LAUNCHER.sub("python3 ", text)
