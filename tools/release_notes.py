"""Write the release notes for one version (used by .github/workflows/release.yml).

  python3 tools/release_notes.py 2.17 dist > release_body.md

Fills .github/RELEASE_TEMPLATE.md:
  <!-- vX.Y -->         the version
  <!-- bullets -->      that version's section of CHANGELOG.md (plus "Unreleased", if any)
  <!-- macos-min -->    each Mac build's real minimum macOS, read from the Info.plist inside
                        dist/Digitizer-macOS-<chip>.zip (it moves when Homebrew rebuilds
                        Tesseract's libraries, so it is never typed by hand)
  <!-- components -->   what is inside every download, from the pins the build scripts
                        enforce on both platforms: .python-version, constraints.txt and
                        Digitizer/tesseract-lock.json (CI's parity job checks the builds match)
"""

from __future__ import annotations

import json
import plistlib
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHIPS = (("AppleSilicon", "Apple Silicon"), ("Intel", "Intel"))


def changelog_section(log: str, heading: str) -> str:
    m = re.search(rf"(?s)^## {heading}\s*(.*?)(?=^## |\Z)", log, re.M)
    return m.group(1).strip() if m else ""


def macos_minimums(dist: Path) -> str:
    found = []
    for chip, label in CHIPS:
        z = dist / f"Digitizer-macOS-{chip}.zip"
        if not z.is_file():
            continue
        with zipfile.ZipFile(z) as zf:
            plist = plistlib.loads(zf.read("Digitizer.app/Contents/Info.plist"))
        found.append(f"{label}: macOS {plist['LSMinimumSystemVersion']} or newer")
    return " · ".join(found) or "macOS 15 or newer"


def components() -> str:
    pins = {}
    for line in (ROOT / "constraints.txt").read_text(encoding="utf-8").splitlines():
        line = line.split("#")[0].split(";")[0].strip()
        if "==" in line:
            name, ver = line.split("==")
            pins[name.strip().lower()] = ver.strip()
    python = (ROOT / ".python-version").read_text(encoding="utf-8").strip()
    lock = json.loads((ROOT / "Digitizer" / "tesseract-lock.json").read_text(encoding="utf-8"))
    models = re.search(r"tesseract-ocr/(tessdata\w*)/([^/]+)/", lock["tessdata"]["eng.traineddata"]["url"])
    model_src = f"{models.group(1)} {models.group(2)}" if models else "tessdata"
    features = " and ".join(lock.get("required_features", []))
    return (f"Python {python} · Qt {pins['pyqt6-qt6']} (PyQt6 {pins['pyqt6']}) · "
            f"Tesseract OCR {lock['version']}{f' with {features}' if features else ''}, "
            f"English and orientation models from {model_src} · NumPy {pins['numpy']} · "
            f"Pillow {pins['pillow']} · Accuracy Tester: matplotlib {pins['matplotlib']}, "
            f"pandas {pins['pandas']}")


def render(version: str, dist: Path) -> str:
    body = (ROOT / ".github" / "RELEASE_TEMPLATE.md").read_text(encoding="utf-8")
    log = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    pending = changelog_section(log, "Unreleased")
    tagged = changelog_section(log, re.escape(version))
    bullets = "\n\n".join(part for part in (pending, tagged) if part) or "See the changelog."
    return (body.replace("<!-- vX.Y -->", version)
                .replace("<!-- bullets -->", bullets)
                .replace("<!-- macos-min -->", macos_minimums(dist))
                .replace("<!-- components -->", components()))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.stdout.write(render(sys.argv[1], Path(sys.argv[2])))
