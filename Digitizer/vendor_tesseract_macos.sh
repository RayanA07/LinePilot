#!/usr/bin/env bash
set -euo pipefail

# Vendor a self-contained Tesseract OCR runtime into Digitizer/vendor/tesseract:
#   - the tesseract binary
#   - tessdata/eng.traineddata + osd.traineddata
#   - the dependent dylibs (bundled with dylibbundler, rewritten to @executable_path/lib)
#
# Run from a Mac with Homebrew installed. The PyInstaller spec then copies
# vendor/tesseract into Digitizer.app so OCR works without any system Tesseract.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENDOR_DIR="$ROOT/vendor/tesseract"
TESSDATA_DIR="$VENDOR_DIR/tessdata"

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is required to vendor Tesseract on macOS." >&2
  exit 1
fi

if ! command -v tesseract >/dev/null 2>&1; then
  brew install tesseract
fi

if ! command -v dylibbundler >/dev/null 2>&1; then
  brew install dylibbundler
fi

rm -rf "$VENDOR_DIR"
mkdir -p "$TESSDATA_DIR"

TESSERACT_BIN="$(command -v tesseract)"
cp "$TESSERACT_BIN" "$VENDOR_DIR/tesseract"
chmod +x "$VENDOR_DIR/tesseract"

BREW_TESS_PREFIX="$(brew --prefix tesseract)"
if [[ -f "$BREW_TESS_PREFIX/share/tessdata/eng.traineddata" ]]; then
  cp "$BREW_TESS_PREFIX/share/tessdata/eng.traineddata" "$TESSDATA_DIR/"
fi
if [[ -f "$BREW_TESS_PREFIX/share/tessdata/osd.traineddata" ]]; then
  cp "$BREW_TESS_PREFIX/share/tessdata/osd.traineddata" "$TESSDATA_DIR/"
fi

if [[ ! -f "$TESSDATA_DIR/eng.traineddata" ]]; then
  echo "Missing eng.traineddata after Tesseract install." >&2
  exit 1
fi

dylibbundler \
  -od \
  -b \
  -x "$VENDOR_DIR/tesseract" \
  -d "$VENDOR_DIR/lib" \
  -p "@executable_path/lib"

# dylibbundler rewrites load paths with install_name_tool, which breaks each file's code
# signature. Apple Silicon kills a binary with a broken signature on launch ("Killed: 9"),
# which shows up in the app as OCR silently failing - so re-sign every piece ad hoc.
codesign --force --sign - "$VENDOR_DIR/tesseract"
for lib in "$VENDOR_DIR"/lib/*.dylib; do
  codesign --force --sign - "$lib"
done

# Prove the vendored copy launches and finds its own bundled tessdata before PyInstaller
# copies it into the app. (The CI workflow goes further: it uninstalls Homebrew's
# Tesseract and runs OCR through the built app's copy.)
TESSDATA_PREFIX="$TESSDATA_DIR" "$VENDOR_DIR/tesseract" --list-langs 2>&1 | grep -qx eng \
  || { echo "Vendored tesseract cannot list the 'eng' language - bundle is broken." >&2; exit 1; }

echo "Vendored Tesseract runtime at $VENDOR_DIR ($(TESSDATA_PREFIX="$TESSDATA_DIR" "$VENDOR_DIR/tesseract" --version 2>&1 | head -1))"
