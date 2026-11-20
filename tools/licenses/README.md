# Bundled license texts

The Accuracy Tester's window is drawn with Tcl/Tk, which is bundled into both
`AccuracyTester.exe` and `AccuracyTester.app`. The Python distributions for Windows and
macOS do not ship the same Tcl/Tk license files (Windows had Tk's but not Tcl's; macOS had
neither), so both PyInstaller specs add these two files through
`tools/build_common.py`, and every build carries them as `_tcl_data/license.terms` and
`_tk_data/license.terms`.

| File | Source |
| --- | --- |
| `tcl-license.terms` | https://github.com/tcltk/tcl/blob/core-8-6-branch/license.terms |
| `tk-license.terms` | https://github.com/tcltk/tk/blob/core-8-6-branch/license.terms |
