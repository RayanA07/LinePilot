"""Unit tests for tools/macho_minos.py on synthetic Mach-O headers (runs on any OS)."""

import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macho_minos  # noqa: E402


def _thin(minos, cmd=macho_minos.LC_BUILD_VERSION, cputype=0x0100000C):
    if cmd == macho_minos.LC_BUILD_VERSION:
        lc = struct.pack("<IIIIII", cmd, 24, macho_minos.PLATFORM_MACOS, minos, minos, 0)
    else:
        lc = struct.pack("<IIII", cmd, 16, minos, minos)
    header = struct.pack("<IiiIIIII", macho_minos.MH_MAGIC_64, cputype, 0, 6, 1, len(lc), 0, 0)
    return header + lc


def _ver(major, minor, patch=0):
    return (major << 16) | (minor << 8) | patch


def test_thin_build_version(tmp_path):
    f = tmp_path / "lib.dylib"
    f.write_bytes(_thin(_ver(15, 0)))
    assert macho_minos.file_minos(f) == (15, 0, 0)


def test_legacy_version_min_command(tmp_path):
    f = tmp_path / "old.so"
    f.write_bytes(_thin(_ver(10, 13), cmd=macho_minos.LC_VERSION_MIN_MACOSX))
    assert macho_minos.file_minos(f) == (10, 13, 0)


def test_universal_binary_reports_highest_slice(tmp_path):
    a = _thin(_ver(11, 0))
    b = _thin(_ver(10, 13), cputype=0x01000007)
    off_a, off_b = 4096, 8192
    fat = struct.pack(">II", macho_minos.FAT_MAGIC, 2)
    fat += struct.pack(">iiIII", 0x0100000C, 0, off_a, len(a), 12)
    fat += struct.pack(">iiIII", 0x01000007, 0, off_b, len(b), 12)
    data = fat.ljust(off_a, b"\0") + a
    data = data.ljust(off_b, b"\0") + b
    f = tmp_path / "universal"
    f.write_bytes(data)
    assert macho_minos.file_minos(f) == (11, 0, 0)


def test_bundle_minimum_is_the_highest_binary(tmp_path, capsys):
    app = tmp_path / "Digitizer.app" / "Contents"
    (app / "MacOS").mkdir(parents=True)
    (app / "Frameworks" / "vendor").mkdir(parents=True)
    (app / "MacOS" / "Digitizer").write_bytes(_thin(_ver(11, 0)))
    (app / "Frameworks" / "vendor" / "tesseract").write_bytes(_thin(_ver(26, 4)))
    (app / "Info.plist").write_text("<plist/>")
    assert macho_minos.main([str(tmp_path / "Digitizer.app")]) == 0
    assert capsys.readouterr().out.strip() == "26.4"


def test_non_macho_and_java_class_files_are_ignored(tmp_path):
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "A.class").write_bytes(struct.pack(">IHH", 0xCAFEBABE, 0, 52) + b"\0" * 32)
    assert macho_minos.file_minos(tmp_path / "a.txt") is None
    assert macho_minos.file_minos(tmp_path / "A.class") is None
