#!/usr/bin/env bash
set -euo pipefail

# Build Digitizer.app on macOS and zip it for a release.
#
# The macOS twin of build_windows.ps1: the same steps from the same pinned inputs, so the
# .app and the .exe contain the same things.
#   1. a clean build environment (.build-venv) on the Python in ../.python-version,
#      with exactly the packages in ../constraints.txt
#   2. the OCR engine pinned in tesseract-lock.json   (vendor_tesseract_macos.sh)
#   3. PyInstaller with digitizer_macos.spec           (settings shared via tools/build_common.py)
#   4. an inventory of what went in                    (tools/bundle_inventory.py)
#   then the macOS-only steps: minimum macOS in Info.plist, ad-hoc signature, zip.
#
#   bash Digitizer/build_macos.sh                  (needs Homebrew)
#   SKIP_INSTALL=1 bash Digitizer/build_macos.sh   reuse the existing build environment
#   PYTHON=/path/to/python3.12 bash ...            use that Python instead of python3.12
#
# The app runs on the chip it is built on (Apple Silicon or Intel) and on the macOS version
# of the build machine or newer - see tools/macho_minos.py for why. The GitHub Actions
# workflow builds one of each chip on the oldest supported runner.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$ROOT/.." && pwd)"
cd "$ROOT"
PY_VERSION="$(tr -d '[:space:]' < "$REPO/.python-version")"
PYTHON="${PYTHON:-python$PY_VERSION}"
VENV="$ROOT/.build-venv"
VPY="$VENV/bin/python"

case "$(uname -m)" in
  arm64) ARCH_LABEL="AppleSilicon" ;;
  x86_64) ARCH_LABEL="Intel" ;;
  *) ARCH_LABEL="$(uname -m)" ;;
esac

# 1. Clean build environment with the pinned packages.
if [[ "${SKIP_INSTALL:-0}" != "1" || ! -x "$VPY" ]]; then
  if ! command -v "$PYTHON" >/dev/null 2>&1; then
    echo "Python $PY_VERSION not found ('$PYTHON'). Install it (brew install python@$PY_VERSION) or set PYTHON=/path/to/python3." >&2
    exit 1
  fi
  rm -rf "$VENV"
  "$PYTHON" -m venv "$VENV"
  "$VPY" -m pip install --disable-pip-version-check --only-binary=:all: -r requirements.txt -c ../constraints.txt
fi
got="$("$VPY" -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
if [[ "$got" != "$PY_VERSION" && -z "${ALLOW_ANY_PYTHON:-}" ]]; then
  echo "The build environment uses Python $got, but LinePilot is built with $PY_VERSION (.python-version) so macOS and Windows bundle the same thing. Install Python $PY_VERSION, or set ALLOW_ANY_PYTHON=1 to build anyway." >&2
  exit 1
fi
VERSION="$("$VPY" -c 'import json; print(json.load(open("version.json"))["version"])')"

# 2. The pinned OCR engine (and the app icon, made from the same .ico Windows uses).
"$VPY" make_macos_icons.py
PYTHON="$VPY" bash vendor_tesseract_macos.sh

# 3. PyInstaller.
rm -rf build dist
"$VPY" -m PyInstaller --clean --noconfirm digitizer_macos.spec
APP="dist/Digitizer.app"

# macOS only: stamp the real minimum macOS (highest of any bundled binary) so an older Mac
# is told "requires macOS X" up front instead of opening an app whose OCR cannot load.
MINOS="$("$VPY" ../tools/macho_minos.py "$APP" --report)"
/usr/bin/plutil -replace LSMinimumSystemVersion -string "$MINOS" "$APP/Contents/Info.plist"

# Ad-hoc sign (no Apple Developer ID). Editing Info.plist above invalidates PyInstaller's
# signature, and Apple Silicon will not launch an app whose signature is broken.
codesign --force --deep --sign - "$APP"
codesign --verify --deep --strict "$APP"

# 4. What went in (compared against the Windows build in CI). Taken after signing,
# because it runs the bundled tesseract, which Apple Silicon only runs when signed.
"$VPY" ../tools/bundle_inventory.py "$APP" -o "dist/Digitizer-inventory-macOS-${ARCH_LABEL}.json"

ZIP="dist/Digitizer-macOS-${ARCH_LABEL}.zip"
ditto -c -k --sequesterRsrc --keepParent "$APP" "$ZIP"

echo ""
echo "Built: $ROOT/$APP  (LinePilot Digitizer $VERSION, Python $got, $(uname -m), macOS $MINOS or newer)"
echo "Zip:   $ROOT/$ZIP"
