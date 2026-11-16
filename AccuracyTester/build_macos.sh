#!/usr/bin/env bash
set -euo pipefail

# Build AccuracyTester.app on macOS and zip it for a release. No Tesseract needed.
#   bash AccuracyTester/build_macos.sh

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

rm -rf build dist
"$PYTHON" -m PyInstaller --clean --noconfirm accuracytester_macos.spec

APP="dist/AccuracyTester.app"
MINOS="$("$PYTHON" ../tools/macho_minos.py "$APP" --report)"
/usr/bin/plutil -replace LSMinimumSystemVersion -string "$MINOS" "$APP/Contents/Info.plist"

codesign --force --deep --sign - "$APP"
codesign --verify --deep --strict "$APP"

ZIP="dist/AccuracyTester-macOS-${ARCH_LABEL}.zip"
ditto -c -k --sequesterRsrc --keepParent "$APP" "$ZIP"

echo ""
echo "Built: $ROOT/$APP  (Accuracy Tester $VERSION, $(uname -m), macOS $MINOS or newer)"
echo "Zip:   $ROOT/$ZIP"
