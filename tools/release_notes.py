"""Write the release notes for one version (used by .github/workflows/release.yml).

  python3 tools/release_notes.py 2.17 dist > release_body.md

Fills .github/RELEASE_TEMPLATE.md:
  <!-- vX.Y -->         the version
  <!-- bullets -->      that version's section of CHANGELOG.md (plus "Unreleased", if any)
  <!-- macos-min -->    each Mac build's real minimum macOS, read from the Info.plist inside
                        dist/Digitizer-macOS-<chip>.zip (it moves when Homebrew rebuilds
                        Tesseract, so it is never typed by hand)
"""

from __future__ import annotations

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


def render(version: str, dist: Path) -> str:
    body = (ROOT / ".github" / "RELEASE_TEMPLATE.md").read_text(encoding="utf-8")
    log = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    pending = changelog_section(log, "Unreleased")
    tagged = changelog_section(log, re.escape(version))
    bullets = "\n\n".join(part for part in (pending, tagged) if part) or "See the changelog."
    return (body.replace("<!-- vX.Y -->", version)
                .replace("<!-- bullets -->", bullets)
                .replace("<!-- macos-min -->", macos_minimums(dist)))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.stdout.write(render(sys.argv[1], Path(sys.argv[2])))
