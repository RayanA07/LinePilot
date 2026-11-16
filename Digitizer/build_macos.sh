#!/usr/bin/env bash
set -euo pipefail

# Build Digitizer.app on macOS and zip it for a release.
# Run on a Mac with Homebrew, from anywhere:
#   bash Digitizer/build_macos.sh
#
# The app runs on the architecture it is built on (Apple Silicon or Intel) and on the
# macOS version of the build machine or newer - see tools/macho_minos.py for why. The
# GitHub Actions workflow builds one of each architecture on the oldest supported runner.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
PYTHON="${PYTHON:-python3}"

VERSION="$("$PYTHON" -c 'import json; print(json.load(open("version.json"))["version"])')"
case "$(uname -m)" in
  arm64) ARCH_LABEL="AppleSilicon" ;;
  x86_64) ARCH_LABEL="Intel" ;;
  *) ARCH_LABEL="$(uname -m)" ;;
esac

if [[ "${SKIP_INSTALL:-0}" != "1" ]]; then
  "$PYTHON" -m pip install -r requirements.txt
fi
"$PYTHON" make_macos_icons.py
bash vendor_tesseract_macos.sh

rm -rf build dist
"$PYTHON" -m PyInstaller --clean --noconfirm digitizer_macos.spec

APP="dist/Digitizer.app"

# Stamp the real minimum macOS (highest of any bundled binary) so an older Mac is told
# "requires macOS X" up front instead of opening an app whose OCR cannot load.
MINOS="$("$PYTHON" ../tools/macho_minos.py "$APP" --report)"
/usr/bin/plutil -replace LSMinimumSystemVersion -string "$MINOS" "$APP/Contents/Info.plist"

# Ad-hoc sign (no Apple Developer ID). Editing Info.plist above invalidates PyInstaller's
# signature, and Apple Silicon will not launch an app whose signature is broken.
codesign --force --deep --sign - "$APP"
codesign --verify --deep --strict "$APP"

ZIP="dist/Digitizer-macOS-${ARCH_LABEL}.zip"
ditto -c -k --sequesterRsrc --keepParent "$APP" "$ZIP"

echo ""
echo "Built: $ROOT/$APP  (LinePilot Digitizer $VERSION, $(uname -m), macOS $MINOS or newer)"
echo "Zip:   $ROOT/$ZIP"
