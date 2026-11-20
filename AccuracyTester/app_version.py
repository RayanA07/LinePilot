"""Name and version of the Accuracy Tester, read from version.json.

The same approach as Digitizer/app_version.py: version.json is bundled into the .exe and
the .app by both PyInstaller specs, so the window title always matches the release.
test_app_version.py fails if version.json and the fallback below disagree.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

# Used only if version.json is unreadable. Kept in step with version.json by the tests.
_FALLBACK_VERSION = "2.17"


def _version_json_path() -> Optional[Path]:
    roots = []
    bundle = getattr(sys, "_MEIPASS", None)  # set inside the PyInstaller .exe / .app
    if bundle:
        roots.append(Path(bundle))
    roots.append(Path(__file__).resolve().parent)
    for root in roots:
        candidate = root / "version.json"
        if candidate.is_file():
            return candidate
    return None


def _load() -> str:
    path = _version_json_path()
    if path is None:
        return _FALLBACK_VERSION
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return _FALLBACK_VERSION
    if not isinstance(data, dict):
        return _FALLBACK_VERSION
    return str(data.get("version") or _FALLBACK_VERSION)


APP_VERSION = _load()

# The window title, matching the Digitizer's "LinePilot Digitizer <version>".
APP_TITLE = f"LinePilot Accuracy Tester {APP_VERSION}"
