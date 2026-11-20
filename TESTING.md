# Testing LinePilot

LinePilot is tested two ways before a release is announced: **automatically** on clean build machines for every change, and **by hand** on independent computers that have never had LinePilot, Python or Tesseract installed.

## 1. Automatic checks — every push, every release

[`.github/workflows/release.yml`](.github/workflows/release.yml) runs on three kinds of machine at once. A release only gets its download files if every check passes.

| Check | Windows | Mac, Apple Silicon | Mac, Intel |
| --- | :---: | :---: | :---: |
| Unit tests — Digitizer, Accuracy Tester, build tools | ✓ | ✓ | ✓ |
| End-to-end smoke test — render charts with known data → batch-digitize with OCR → score against the truth | ✓ | ✓ | ✓ |
| Command-line help prints only Mac-appropriate commands and paths | — | ✓ | ✓ |
| Build both apps (`Digitizer`, `AccuracyTester`) with the same build scripts a developer runs, from the same pins: Python 3.12 (`.python-version`), every package's exact version (`constraints.txt`), Tesseract 5.5.3 and its model checksums (`Digitizer/tesseract-lock.json`) | ✓ | ✓ | ✓ |
| App reports the same version as `version.json` (the `.exe`'s version resource / the `.app`'s `Info.plist`) | ✓ | ✓ | ✓ |
| **Clean-machine check:** the build machine's own Tesseract is removed, then the **built app** digitizes the lab's Raman spectrum with the OCR engine bundled inside it — axes must read 400 / 1800 / 2000 / 14000 and the curve must be within 2 % of the true data | ✓ | ✓ | ✓ |
| Both apps open their window (on Windows: the app's own window title, so a crash dialog can't pass for a running app) | ✓ | ✓ | ✓ |
| **Parity check:** the inventories of all three builds (`tools/bundle_inventory.py`) list the same Python version, third-party packages, data files, PyInstaller hooks, Tesseract version and features, OCR bundle files and model checksums | ✓ | ✓ | ✓ |

The unit tests and the smoke test run against the Tesseract the build just bundled, not a separately installed one. The clean-machine check uses the app's built-in self-test (`LINEPILOT_SELFTEST`, see `Digitizer/digitizer_desktop.py`), judged by `tools/check_selftest.py`. Results for every run are on the [Actions page](https://github.com/RayanA07/LinePilot/actions/workflows/release.yml).

Run the same tests locally from the repository folder:

```bash
cd Digitizer && python -m pytest -q && cd ..        # Digitizer unit tests
cd AccuracyTester && python -m pytest -q && cd ..   # Accuracy Tester unit tests
python tools/smoke_test.py                          # end to end (needs Tesseract installed)
python tools/bundle_inventory.py --compare Digitizer/dist/*-inventory-*.json   # after builds on two platforms
```

## 2. Hands-on installation test — independent computers

Build machines are clean, but they are not real users' computers: those have antivirus software, SmartScreen / Smart App Control, Gatekeeper, other Python installs, different display scaling, and people who have never seen the app. So before announcing a release, run this checklist on **at least one Windows PC and one Mac that have never had LinePilot, Python or Tesseract installed** (a lab or library computer, or a colleague's laptop). Record each run with the **[Installation report](https://github.com/RayanA07/LinePilot/issues/new?template=install_report.yml)** form so the result is public and dated.

You need the demo image and its true data: [`example_raman.png`](docs/assets/demo/example_raman.png) and [`example_raman_ground_truth.csv`](docs/assets/demo/example_raman_ground_truth.csv) (open each link, then **Download raw file**).

| # | Do this | Expected result |
| --- | --- | --- |
| 1 | Open [rayana07.github.io/LinePilot](https://rayana07.github.io/LinePilot/) and click the download button for your computer. | The right file downloads: `Digitizer.exe` on Windows; `Digitizer-macOS-AppleSilicon.zip` or `-Intel.zip` on a Mac. |
| 2 | Open it, following the [user guide](Digitizer/README.md#download--install-no-python-needed) for the first-run warning. | The warning matches the guide; after the documented clicks the app opens. The title bar reads **LinePilot Digitizer 2.17** (or the version being tested). |
| 3 | **Import ▾ → Import Image** → `example_raman.png`, then **Advanced ▾ → Axis Scale Detection → Run Axis Detection**. | The Min-Max boxes read **400, 1800, 2000, 14000**. |
| 4 | **Tools ▾ → Calibration → Coordinate-Mediated Calibration**, then **Tools ▾ → Place Points → Run**. | A dashed calibration box and points along the whole spectrum. |
| 5 | **Export ▾ → Export CSV → Raw values**, save it, and open the file. | It opens in Excel / Numbers with `x`, `y` columns. |
| 6 | Calibrate by hand with **Enhanced Human Click** on; click a tick, then undo (Ctrl+Z on Windows, ⌘Z on a Mac). | The click snaps to the tick; undo removes it. |
| 7 | **About ▾** → click Project website, Paper on arXiv, DigitizerBench on Hugging Face and Report an issue. | Each opens the right page in the browser. |
| 8 | Install the **Accuracy Tester** the same way; compare the exported CSV with `example_raman_ground_truth.csv`. | It opens after the same first-run step; the title bar reads **LinePilot Accuracy Tester 2.17**; R² is above 0.99. |
| 9 | Quit and reopen Digitizer. | It opens straight away, with no security warning. |

Anything that doesn't match: file a **[bug report](https://github.com/RayanA07/LinePilot/issues/new?template=bug_report.yml)** with the OS version and a screenshot, and fix the guide or the app before announcing.

### Results log

| Date | Tester | Computer | OS and version | App version | Result | Report |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |
