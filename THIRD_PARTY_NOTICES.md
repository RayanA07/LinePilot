# Third-party notices

LinePilot Digitizer is released under the [Apache License 2.0](LICENSE). It depends on the
open-source components below, each under its own license. License identifiers were read
from the packages' own metadata (`importlib.metadata`) on 2026-10-29; versions are those
resolved by `pip` at that date and are not pinned.

## Bundled into `Digitizer.exe`

| Component | License | Used for |
| --- | --- | --- |
| [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) | GPL-3.0-only (commercial license also available from Riverbank) | Desktop window and widgets |
| [PyQt6-Qt6](https://www.qt.io) (the Qt 6 runtime) | LGPL v3 | Qt libraries PyQt6 binds to |
| PyQt6-sip | BSD-2-Clause | PyQt6 bindings support |
| [NumPy](https://numpy.org) | BSD-3-Clause (and 0BSD / MIT / Zlib / CC0 for vendored parts) | Array math |
| [Pillow](https://python-pillow.org) | MIT-CMU | Image loading and overlay drawing |
| [pytesseract](https://github.com/madmaze/pytesseract) | Apache-2.0 | Python wrapper around Tesseract |
| [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and `tessdata` | Apache-2.0 | Reading axis tick labels (vendored at build time) |
| [RapidOCR](https://github.com/RapidAI/RapidOCR) *(optional, if installed)* | Apache-2.0 | Secondary OCR engine |
| [openpyxl](https://openpyxl.readthedocs.io) | MIT | Excel export |

## Bundled into `AccuracyTester.exe`

| Component | License | Used for |
| --- | --- | --- |
| [pandas](https://pandas.pydata.org) | BSD-3-Clause | Tabular data handling |
| [matplotlib](https://matplotlib.org) | PSF-based matplotlib license (BSD-compatible) | Comparison plots |
| [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2) | MIT | Drag-and-drop in the Tk window |
| NumPy | BSD-3-Clause | Metrics |

## Build only (not shipped inside the executables' Python code)

| Component | License | Used for |
| --- | --- | --- |
| [PyInstaller](https://pyinstaller.org) | GPL-2.0-or-later **with the bootloader exception** that allows building closed- or open-source applications of any license | Producing the one-file `.exe`s |

## What this means for the executables

- The Python source of LinePilot is Apache-2.0.
- The prebuilt `Digitizer.exe` combines that source with PyQt6, which is **GPL-3.0**. The
  Apache-2.0 license is compatible with GPL-3.0, so the *combined* executable is distributed
  on GPL-3.0 terms: anyone receiving it is entitled to the corresponding source, which is
  this repository. Anyone who wants to ship a LinePilot-derived program without GPL
  obligations must either obtain a commercial PyQt6 license from Riverbank or replace PyQt6.
- Tesseract, its language data, NumPy, Pillow, pytesseract and openpyxl impose only
  attribution-style requirements, satisfied by this file and the About → Licenses tab in
  the app.
- No component here restricts academic or commercial *use* of the tool.
