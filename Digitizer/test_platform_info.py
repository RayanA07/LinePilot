"""Pins the per-OS behaviour in platform_info.py.

The important guarantee is the first test: on Windows the help text is returned untouched,
so making the code cross-platform cannot change a single character of what Windows users
see. The rest checks the macOS / Linux rewrite and the Tesseract search order.
"""

from pathlib import Path

import platform_info
from platform_info import for_this_os

WINDOWS_SAMPLE = (
    "  py digitizer.py plot2.png --out C:\\out\n"
    "  py digitizer.py C:\\charts\n"
    "  py digitizer_batch_cli.py --input-dir C:\\charts --output-dir D:\\results\n"
    "  double-click Digitizer.exe   (or from source: py digitizer_2_11.py)\n"
    "  py digitizer.py 'digitizer_cli(pic_dir=\"C:\\Users\\User\\Pictures\\Screenshots\\Example 2.png\", "
    "output_dir=\"C:\\Users\\User\\Downloads\\testcli\")'\n"
    "  py -m pytest -q\n"
)


def test_windows_text_is_returned_unchanged(monkeypatch):
    monkeypatch.setattr(platform_info, "IS_WINDOWS", True)
    assert for_this_os(WINDOWS_SAMPLE) == WINDOWS_SAMPLE


def test_mac_rewrite_removes_every_windows_only_token(monkeypatch):
    monkeypatch.setattr(platform_info, "IS_WINDOWS", False)
    out = for_this_os(WINDOWS_SAMPLE)
    for bad in ("C:\\", "D:\\", ".exe", "py digitizer", "py -m"):
        assert bad not in out, (bad, out)
    assert "python3 digitizer.py ~/Downloads/charts" in out
    assert "--output-dir ~/Desktop/results" in out
    assert "double-click Digitizer.app" in out
    assert 'pic_dir="/Users/you/Pictures/Example 2.png"' in out
    assert "python3 -m pytest" in out


def test_rewrite_leaves_words_ending_in_py_alone(monkeypatch):
    monkeypatch.setattr(platform_info, "IS_WINDOWS", False)
    text = "copy digitizer.py here; numpy -m stays; happy digitizer.py"
    assert for_this_os(text) == text


def test_tesseract_env_override_wins(tmp_path, monkeypatch):
    fake = tmp_path / "my-tesseract"
    fake.write_text("")
    found = platform_info.find_tesseract(str(fake), [tmp_path / "nowhere"])
    assert found == fake


def test_vendored_tesseract_uses_this_os_binary_name(tmp_path):
    vendored = tmp_path / "vendor" / "tesseract" / platform_info.TESSERACT_BINARY
    vendored.parent.mkdir(parents=True)
    vendored.write_text("")
    assert platform_info.find_tesseract("", [Path("/definitely/not/here"), tmp_path]) == vendored


def test_undo_hint_matches_the_key_qt_actually_binds():
    expected = "⌘Z" if platform_info.IS_MAC else "Ctrl+Z"
    assert platform_info.UNDO_HINT == expected
