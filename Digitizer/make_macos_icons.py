"""Generate Digitizer/assets/digitizer.icns from a source image in assets/.

Looks for a source image in this folder's ``assets`` directory (a PNG or an ICO,
e.g. the Windows ``digitizer.ico``) and converts it to a macOS ``.icns`` icon.

If no source image is found, this script does nothing and exits cleanly. The
PyInstaller spec treats the icon as optional (icon=None when the .icns is
absent), so the build still succeeds without an icon.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
TARGET = ASSETS / "digitizer.icns"

# Candidate source images, in preference order.
SOURCE_CANDIDATES = [
    ASSETS / "digitizer.png",
    ASSETS / "icon.png",
    ASSETS / "digitizer.ico",
    ASSETS / "icon.ico",
]

ICNS_SIZES = [(1024, 1024), (512, 512), (256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]


def _find_source() -> Path | None:
    for candidate in SOURCE_CANDIDATES:
        if candidate.is_file():
            return candidate
    # Fall back to any PNG or ICO in assets.
    for pattern in ("*.png", "*.ico"):
        for path in sorted(ASSETS.glob(pattern)):
            return path
    return None


def _load_largest(source: Path) -> Image.Image:
    image = Image.open(source)
    # ICO files hold multiple sizes; pick the largest available frame.
    if getattr(image, "format", "") == "ICO":
        sizes = getattr(image, "ico", None)
        try:
            largest = max(image.ico.sizes())  # type: ignore[attr-defined]
            image = image.ico.getimage(largest)  # type: ignore[attr-defined]
        except Exception:
            image.load()
    return image.convert("RGBA")


def main() -> None:
    if not ASSETS.exists():
        print(f"No assets directory at {ASSETS}; skipping icon generation.")
        return

    source = _find_source()
    if source is None:
        print("No source image (PNG/ICO) found in assets/; skipping .icns generation.")
        return

    base = _load_largest(source)
    images = [base.resize((w, h), Image.LANCZOS) for w, h in ICNS_SIZES]
    images[0].save(TARGET, format="ICNS", append_images=images[1:])
    print(f"Wrote {TARGET} from {source.name}")


if __name__ == "__main__":
    main()
