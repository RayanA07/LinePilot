# Accuracy Tester

Compares a digitized CSV against a reference ("original") CSV and reports accuracy
metrics. Independent of the Digitizer app — you don't need it to get your data out.

Two ways to use it: the **desktop app** (two files at a time, with diagnostic plots) and
the **batch CLI** (a whole folder, scored by file name).

## Download the app (no Python needed)

From the **[latest release](https://github.com/RayanA07/LinePilot/releases/latest)**, under *Assets*:

| Windows 10 / 11 | Mac (macOS 15 or later) |
| --- | --- |
| **`AccuracyTester.exe`** — double-click it. First run: SmartScreen → **More info → Run anyway**. | **`AccuracyTester-macOS-AppleSilicon.zip`** or **`-Intel.zip`** — double-click the zip, open **`AccuracyTester.app`**. First launch: **Done**, then System Settings → Privacy & Security → **Open Anyway**. |

Step-by-step help for both platforms is in the [Digitizer user guide](../Digitizer/README.md#download--install-no-python-needed) — the Accuracy Tester installs exactly the same way.

## Run from source

Python 3.12 is the version the apps are built with; `-c ../constraints.txt` installs exactly the library versions inside them.

**Windows** (PowerShell, in the `AccuracyTester` folder) — needs Python 3.12 from <https://python.org>:

```powershell
py -m pip install -r requirements.txt -c ..\constraints.txt
py accuracytester_desktop.py
```

**Mac** (Terminal, in the `AccuracyTester` folder) — with [Homebrew](https://brew.sh). The window uses Tkinter, which Homebrew's Python leaves out unless you add `python-tk`:

```bash
brew install python@3.12 python-tk@3.12
python3.12 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt -c ../constraints.txt
python3 accuracytester_desktop.py
```

Next time, `cd` into the folder, run `source .venv/bin/activate`, then `python3 accuracytester_desktop.py`.

Load two CSV files (original vs digitized). Drag-and-drop works when `tkinterdnd2`
is installed; otherwise click the panels to browse for files.

## Batch CLI — score a whole folder

**Windows**

```powershell
py accuracy_batch_cli.py --digitized-dir "path\to\digitized_csvs" --ground-truth-dir "path\to\truth"
```

**Mac**

```bash
python3 accuracy_batch_cli.py --digitized-dir path/to/digitized_csvs --ground-truth-dir path/to/truth
```

Writes, next to the digitized CSVs:

- **`accuracy_report/accuracy_report.csv`** — one row per image: RMSE, correlation, MSE,
  R2, MAE, bias, MAPE/sMAPE/WAPE, `nrmse_range_pct`, point count, plus a `status`.
- **`accuracy_report/accuracy_summary.json`** — totals and the overall failure rate.

Pairs are matched by file-name stem after stripping a `_digitized_points` / `_digitized` /
`_points` / `_ground_truth` / `_gt` suffix. Exact matches take priority, and a tie between
several candidates is reported as `ambiguous_match` — never guessed. Every unmatched or
ignored file is reported rather than silently skipped.

| Status | Means |
| --- | --- |
| `ok` | Pair scored; metrics present. |
| `no_method_match` | A reference with no digitized file to compare against. |
| `no_ground_truth_match` | A digitized file whose name matches no reference. |
| `ambiguous_match` | Several files matched one reference equally well. |
| `invalid_data` | Can't be scored as y=f(x) — e.g. a vertical line. |
| `insufficient_overlap` | The curves share too little X range to compare. |
| `parse_error` | A CSV could not be read at all. |

## Reading the numbers honestly

- **Quote `nrmse_range_pct`, not raw RMSE.** RMSE carries the units of the Y axis, so it is
  meaningless across figures with different scales. An RMSE of 63.9 on an axis running to
  30,000 is *better* than 0.03 on an axis running 0–1.
- **Correlation and R2 are undefined against a flat reference.** Both divide by the variance
  of the reference, which is zero for a horizontal line, so the CSV prints a degenerate
  value like `-2.6e+25`. Read that as **N/A**, not as an accuracy.
- **A vertical line is not a function of x**, so `invalid_data` is the correct answer rather
  than a number. This is by design.

## Tests

The tests check the scoring maths against scipy and scikit-learn as independent
references, so they need a few packages the app itself does not:

**Windows**

```powershell
py -m pip install -r requirements-dev.txt -c ..\constraints.txt
py -m pytest -q
```

**Mac** (with the virtual environment active)

```bash
python3 -m pip install -r requirements-dev.txt -c ../constraints.txt
python3 -m pytest -q
```

## Build the apps

| | Windows | macOS |
| --- | --- | --- |
| **Command** | double-click `build.cmd`, or `.\build_windows.ps1` | `bash build_macos.sh` |
| **Needs** | Python 3.12 | Python 3.12 with Tkinter (`brew install python@3.12 python-tk@3.12`) |
| **Output** | `dist\AccuracyTester.exe` — a windowed, one-file app | `dist/AccuracyTester.app` + `dist/AccuracyTester-macOS-<chip>.zip` |

Both scripts make a clean build environment (`.build-venv`) with exactly the packages in [`constraints.txt`](../constraints.txt), use PyInstaller settings shared through [`tools/build_common.py`](../tools/build_common.py), and write an inventory of what went into the app, so the Windows and macOS builds contain the same things. Releases are built, tested and compared automatically for both platforms by `.github/workflows/release.yml`.

## Folder contents

```text
AccuracyTesterPro.py     # The desktop tool (Tkinter + matplotlib + pandas)
accuracytester_desktop.py# GUI entry point
accuracy_core.py         # The scoring maths (alignment, metrics)
batch_scoring.py         # File matching + pair scoring for batch runs
accuracy_batch_cli.py    # Batch CLI entry point
app_version.py           # Name and version (from version.json) for the window title
test_accuracy_core.py    # Tests for the scoring maths
test_batch_scoring.py    # Tests for file matching + pair scoring
requirements-dev.txt     # Test-only deps (pytest, scipy, scikit-learn)
accuracytester.spec      # PyInstaller spec — Windows (AccuracyTester.exe)
build_windows.ps1        # Windows build script
accuracytester_macos.spec# PyInstaller spec — macOS (AccuracyTester.app)
build_macos.sh           # macOS build script
make_macos_icons.py      # Makes the macOS icon from the Windows .ico
requirements.txt         # Python dependencies
version.json             # App name + version (shares the LinePilot release version)
assets/                  # Application icon
```
