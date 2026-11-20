#!/usr/bin/env bash
set -euo pipefail

# Vendor a self-contained Tesseract OCR runtime into Digitizer/vendor/tesseract.
#
# The macOS twin of vendor_tesseract_windows.ps1. Both read tesseract-lock.json and produce
# the same layout, so Digitizer.app and Digitizer.exe carry the same OCR engine:
#
#   vendor/tesseract/tesseract              the pinned Tesseract version
#   vendor/tesseract/lib/*.dylib            exactly the libraries it loads (dylibbundler)
#   vendor/tesseract/tessdata/eng.traineddata, osd.traineddata   (SHA-256 checked)
#   vendor/tesseract/tessdata/configs/, tessconfigs/
#   vendor/tesseract/doc/AUTHORS, LICENSE, README.md
#
# There is no official macOS build and Homebrew only offers its latest version (with no
# Intel bottles), so the pinned release is compiled from its git tag - checked against the
# commit in the lock file - against Homebrew's leptonica and libarchive. The result is
# cached in .tesseract-build/<version>/ and reused on the next run.
#
#   bash vendor_tesseract_macos.sh            (needs Homebrew; build_macos.sh runs this)

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PYTHON:-python3}"
LOCK="$ROOT/tesseract-lock.json"
VENDOR_DIR="$ROOT/vendor/tesseract"
TESSDATA_DIR="$VENDOR_DIR/tessdata"

lock() { "$PY" -c 'import json,sys
d = json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."):
    d = d[k]
print("\n".join(d) if isinstance(d, list) else d)' "$LOCK" "$1"; }

VERSION="$(lock version)"
REPO="$(lock source.repository)"
TAG="$(lock source.tag)"
COMMIT="$(lock source.commit)"
WORK="$ROOT/.tesseract-build/$VERSION"
PREFIX="$WORK/install"

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is required to vendor Tesseract on macOS (https://brew.sh)." >&2
  exit 1
fi
for formula in leptonica libarchive pkgconf dylibbundler; do
  brew list --formula "$formula" >/dev/null 2>&1 || brew install "$formula"
done
command -v cmake >/dev/null 2>&1 || brew install cmake

pinned() { [[ -x "$1" ]] && "$1" --version 2>/dev/null | head -1 | grep -Eq "^tesseract v?${VERSION//./\\.}([. ]|$)"; }

# 1. The pinned Tesseract build.
if pinned "$PREFIX/bin/tesseract"; then
  echo "Using Tesseract $VERSION already built in $WORK"
else
  echo "Building Tesseract $VERSION from $REPO ($TAG)"
  rm -rf "$WORK"
  git clone --quiet --depth 1 --branch "$TAG" "$REPO" "$WORK/src"
  got="$(git -C "$WORK/src" rev-parse HEAD)"
  if [[ "$got" != "$COMMIT" ]]; then
    echo "Tesseract tag $TAG is at $got, expected $COMMIT (tesseract-lock.json)." >&2
    exit 1
  fi
  cmake -S "$WORK/src" -B "$WORK/build" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$PREFIX" \
    -DCMAKE_INSTALL_RPATH="$PREFIX/lib" \
    -DCMAKE_OSX_DEPLOYMENT_TARGET="$(sw_vers -productVersion | cut -d. -f1).0" \
    -DCMAKE_PREFIX_PATH="$(brew --prefix libarchive);$(brew --prefix leptonica)" \
    -DBUILD_SHARED_LIBS=ON \
    -DBUILD_TRAINING_TOOLS=OFF \
    -DBUILD_TESTS=OFF \
    -DGRAPHICS_DISABLED=ON \
    -DOPENMP_BUILD=OFF \
    -DSW_BUILD=OFF \
    -DDISABLE_ARCHIVE=OFF \
    -DDISABLE_CURL=OFF
  cmake --build "$WORK/build" --parallel "$(sysctl -n hw.ncpu)"
  cmake --install "$WORK/build"
  pinned "$PREFIX/bin/tesseract" || { echo "Built tesseract is not version $VERSION." >&2; exit 1; }
fi

# 2. Copy the program and exactly the libraries it loads.
rm -rf "$VENDOR_DIR"
mkdir -p "$TESSDATA_DIR"
cp "$PREFIX/bin/tesseract" "$VENDOR_DIR/tesseract"
chmod +x "$VENDOR_DIR/tesseract"
dylibbundler -od -b -cd \
  -x "$VENDOR_DIR/tesseract" \
  -d "$VENDOR_DIR/lib" \
  -p "@executable_path/lib" \
  -s "$PREFIX/lib"

# dylibbundler rewrites load paths with install_name_tool, which breaks each file's code
# signature. Apple Silicon kills a binary with a broken signature on launch ("Killed: 9"),
# which shows up in the app as OCR silently failing - so re-sign every piece ad hoc.
codesign --force --sign - "$VENDOR_DIR/tesseract"
for lib in "$VENDOR_DIR"/lib/*.dylib; do
  codesign --force --sign - "$lib"
done

# 3. Configs and the license / authors / readme, from the same release.
cp -R "$PREFIX/share/tessdata/configs" "$TESSDATA_DIR/configs"
cp -R "$PREFIX/share/tessdata/tessconfigs" "$TESSDATA_DIR/tessconfigs"
# The official Windows installer leaves out configs/bazaar (an unused language-model
# setting); leave it out here too so the two bundles match file for file.
rm -f "$TESSDATA_DIR/configs/bazaar"
mkdir -p "$VENDOR_DIR/doc"
cp "$WORK/src/AUTHORS" "$WORK/src/LICENSE" "$WORK/src/README.md" "$VENDOR_DIR/doc/"

# 4. The language models, from the pinned URLs, checksum-verified.
"$PY" -c 'import json,sys
for name, spec in json.load(open(sys.argv[1]))["tessdata"].items():
    print(name, spec["url"], spec["sha256"])' "$LOCK" |
while read -r name url sha; do
  curl -fsSL --retry 3 -o "$TESSDATA_DIR/$name" "$url"
  got="$(shasum -a 256 "$TESSDATA_DIR/$name" | cut -d' ' -f1)"
  if [[ "$got" != "$sha" ]]; then
    echo "$name checksum mismatch: got $got, expected $sha (tesseract-lock.json)." >&2
    exit 1
  fi
done

# 5. Prove the vendored copy runs on its own, is the pinned version, has the same optional
#    features as the Windows build, and finds its own language data.
info="$(TESSDATA_PREFIX="$TESSDATA_DIR" "$VENDOR_DIR/tesseract" --version 2>&1)"
pinned "$VENDOR_DIR/tesseract" || { echo "Vendored tesseract is not version $VERSION:" >&2; echo "$info" >&2; exit 1; }
for feature in $(lock required_features); do
  grep -q "Found $feature" <<<"$info" || { echo "Vendored tesseract was built without $feature:" >&2; echo "$info" >&2; exit 1; }
done
langs="$(TESSDATA_PREFIX="$TESSDATA_DIR" "$VENDOR_DIR/tesseract" --list-langs 2>&1)"
for lang in eng osd; do
  grep -qx "$lang" <<<"$langs" || { echo "Vendored tesseract cannot list '$lang':" >&2; echo "$langs" >&2; exit 1; }
done

echo "Vendored Tesseract $VERSION at $VENDOR_DIR ($(ls "$VENDOR_DIR/lib" | wc -l | tr -d ' ') libraries, $(find "$VENDOR_DIR" -type f | wc -l | tr -d ' ') files)"
