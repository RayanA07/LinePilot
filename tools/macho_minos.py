"""Report the oldest macOS a built .app can actually run on.

Every Mach-O binary records the minimum macOS it was built for (LC_BUILD_VERSION, or the
older LC_VERSION_MIN_MACOSX). A bundle runs only where *all* of its binaries run, so its
real minimum is the highest of those values. That matters here because the app bundles
Homebrew's Tesseract, and Homebrew compiles for the macOS of the machine that built it: a
build made on macOS 26 carries an OCR engine that will not load on macOS 15, even though
Python and Qt themselves run on much older systems.

build_macos.sh stamps the result into Info.plist as LSMinimumSystemVersion, so a Mac that
is too old gets a clear "requires macOS X" message from Finder instead of an app that opens
and then fails at OCR.

Usage:
  python3 tools/macho_minos.py dist/Digitizer.app            -> prints e.g. 15.0
  python3 tools/macho_minos.py dist/Digitizer.app --report   -> also lists the binaries
                                                                that set that minimum
Pure Python (no otool/vtool), so it also runs in tests on any OS.
"""

from __future__ import annotations

import argparse
import os
import struct
import sys
from pathlib import Path
from typing import Iterator, Optional, Tuple

LC_VERSION_MIN_MACOSX = 0x24
LC_BUILD_VERSION = 0x32
PLATFORM_MACOS = 1

MH_MAGIC = 0xFEEDFACE
MH_MAGIC_64 = 0xFEEDFACF
FAT_MAGIC = 0xCAFEBABE
FAT_MAGIC_64 = 0xCAFEBABF

Version = Tuple[int, int, int]


def _decode(v: int) -> Version:
    return (v >> 16, (v >> 8) & 0xFF, v & 0xFF)


def _thin_minos(data: bytes, base: int) -> Optional[Version]:
    """Minimum macOS of one thin (single-architecture) Mach-O image starting at `base`."""
    if len(data) < base + 28:
        return None
    magic = struct.unpack_from("<I", data, base)[0]
    if magic == MH_MAGIC_64:
        header = 32
    elif magic == MH_MAGIC:
        header = 28
    else:
        return None
    ncmds = struct.unpack_from("<I", data, base + 16)[0]
    offset = base + header
    found: Optional[Version] = None
    for _ in range(ncmds):
        if offset + 8 > len(data):
            break
        cmd, size = struct.unpack_from("<II", data, offset)
        if size < 8:
            break
        if cmd == LC_BUILD_VERSION and offset + 16 <= len(data):
            platform, minos = struct.unpack_from("<II", data, offset + 8)
            if platform == PLATFORM_MACOS:
                found = _decode(minos)
        elif cmd == LC_VERSION_MIN_MACOSX and offset + 12 <= len(data):
            found = _decode(struct.unpack_from("<I", data, offset + 8)[0])
        offset += size
    return found


def file_minos(path: Path) -> Optional[Version]:
    """Highest minimum macOS across all architecture slices of a Mach-O file, or None."""
    try:
        with open(path, "rb") as fh:
            head = fh.read(8)
            if len(head) < 4:
                return None
            magic_be = struct.unpack(">I", head[:4])[0]
            magic_le = struct.unpack("<I", head[:4])[0]
            if magic_be not in (FAT_MAGIC, FAT_MAGIC_64) and magic_le not in (MH_MAGIC, MH_MAGIC_64):
                return None
            fh.seek(0)
            data = fh.read()
    except OSError:
        return None

    if magic_le in (MH_MAGIC, MH_MAGIC_64):
        return _thin_minos(data, 0)

    # Universal binary: big-endian header, then one fat_arch entry per slice.
    nfat = struct.unpack_from(">I", data, 4)[0]
    if nfat > 32:  # Java .class files share the 0xCAFEBABE magic; real fat headers are tiny
        return None
    entry = 32 if magic_be == FAT_MAGIC_64 else 20
    best: Optional[Version] = None
    for i in range(nfat):
        at = 8 + i * entry
        if magic_be == FAT_MAGIC_64:
            offset = struct.unpack_from(">Q", data, at + 8)[0]
        else:
            offset = struct.unpack_from(">I", data, at + 8)[0]
        v = _thin_minos(data, offset)
        if v is not None and (best is None or v > best):
            best = v
    return best


def scan(bundle: Path) -> Iterator[Tuple[Version, Path]]:
    for dirpath, _dirs, files in os.walk(bundle):
        for name in files:
            path = Path(dirpath) / name
            if path.is_symlink():
                continue
            v = file_minos(path)
            if v is not None:
                yield v, path


def fmt(v: Version) -> str:
    major, minor, patch = v
    return f"{major}.{minor}" + (f".{patch}" if patch else "")


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--report", action="store_true",
                        help="also list the binaries with the highest minimums (to stderr)")
    args = parser.parse_args(argv)

    results = sorted(scan(args.bundle), reverse=True)
    if not results:
        print(f"error: no Mach-O binaries found under {args.bundle}", file=sys.stderr)
        return 2
    top = results[0][0]
    if args.report:
        print(f"{len(results)} Mach-O binaries scanned; highest minimum macOS = {fmt(top)}",
              file=sys.stderr)
        for v, path in results[:12]:
            print(f"  {fmt(v):>7}  {path.relative_to(args.bundle)}", file=sys.stderr)
    print(fmt(top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
