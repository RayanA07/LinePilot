<p align="center">
  <img src="docs/assets/banner.png" alt="LinePilot Digitizer" width="820">
</p>

<p align="center">
  <a href="https://arxiv.org/abs/2609.19377"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2609.19377-BA0C2F.svg"></a>
  <a href="https://rayana07.github.io/LinePilot/"><img alt="Project website" src="https://img.shields.io/badge/website-rayana07.github.io%2FLinePilot-000000.svg"></a>
  <a href="https://github.com/aj24by7/DataDigitizer/releases/latest"><img alt="Download" src="https://img.shields.io/badge/download-Windows%20app-00A3AD.svg"></a>
  <a href="#digitizerbench"><img alt="DigitizerBench" src="https://img.shields.io/badge/benchmark-DigitizerBench-9EA2A2.svg"></a>
</p>

**LinePilot Digitizer** turns a *picture* of a line plot — a figure from a paper, a scanned chart, a screenshot — into the *numbers* behind it. It reads the axes, follows each colored curve column by column, and exports a CSV plus an overlay image so you can check its work at a glance.

It offers three calibration modes that share one curve-recovery procedure:

| Mode | How the axes are calibrated | Best for |
| --- | --- | --- |
| **LinePilot (standard)** | You click four axis ticks (X min, X max, Y min, Y max); the clicks are used as is. | Full manual control. |
| **LinePilot (enhanced)** | Same four clicks, each snapped to the nearest tick / axis stroke at sub-pixel precision — only when the image supports it. | Best accuracy with human guidance. Lowest error of every tool we tested on DigitizerBench-Lite. |
| **LinePilot (OCR)** | Axis labels are read with Tesseract (and RapidOCR when available), paired with ticks, and checked for a consistent scale. No clicks. | Batch processing and fully automatic pipelines. Best of the automatic tools on DigitizerBench-Full. |

The paper also introduces **[DigitizerBench](#digitizerbench)**, the first benchmark designed specifically to evaluate plot digitizers end to end.

<p align="center">
  <img src="docs/assets/demo.gif" alt="Animated illustration: LinePilot sweeps across a line plot column by column, placing calibrated points and streaming x,y rows to a CSV" width="560"><br>
  <sub>Column-by-column color matching, linked by dynamic programming into one continuous path per curve.</sub>
</p>

> **Paper:** Fengbo Ma\*, Rayan Akhtar\*, Aakash H. Joshi\*, Xiaoting Li, Haijian Sun, Zhen Xiang†, Xianyan Chen†, Yiping Zhao†.
> *LinePilot Digitizer: Line-Plot Recovery with Manual and Automatic Calibration.* arXiv:2609.19377, 2026.
> [[arXiv](https://arxiv.org/abs/2609.19377)] · [[PDF](https://arxiv.org/pdf/2609.19377)] · [[Online appendix](docs/assets/LinePilot_Online_Appendix.pdf)] · [[Website](https://rayana07.github.io/LinePilot/)] · [[Cite](#citation)]

---

## Contents

- [How it works](#how-it-works)
- [Results](#results)
- [Install](#install)
- [Using the desktop app](#using-the-desktop-app)
- [Command line, batch mode and Python API](#command-line-batch-mode-and-python-api)
- [DigitizerBench](#digitizerbench)
- [Repository layout](#repository-layout)
- [Citation](#citation)
- [Acknowledgment](#acknowledgment)

---

## How it works

<p align="center">
  <img src="docs/assets/workflow.png" alt="LinePilot workflow: import a line plot; calibrate with standard, enhanced or OCR mode; color-based curve extraction; digitized (x, y) data" width="620">
</p>

Digitization is two problems. **Calibration** maps image pixels to data coordinates — a calibration error shifts every recovered point. **Curve recovery** follows the plotted line, which is a continuous path rather than a cloud of independent pixels. LinePilot keeps the recovery stage fixed and lets you choose how calibration happens.

**Calibration.** For either linear axis, two anchors *(p₁, q₁)* and *(p₂, q₂)* define *q = q₁ + (p − p₁)(q₂ − q₁)/(p₂ − p₁)*, applied horizontally to *(u, x)* and vertically to *(v, y)*. The three modes differ only in where the anchors come from: your raw clicks (standard), your clicks refined to the tick center from local image intensity (enhanced), or OCR'd tick labels paired with detected ticks and filtered for a consistent scale (OCR). OCR mode reports failure rather than guessing when the required endpoints can't be established. Log-scale axes are supported in every mode.

**Curve extraction.** Target colors are detected automatically or picked by you. In each image column, pixels within a color tolerance are grouped into vertical runs; each run's midpoint is a candidate center-line position and its thickness is extra stroke evidence. Dynamic programming links candidates across columns, rewarding sustained support and penalizing abrupt vertical jumps and gaps, so isolated color-matched objects lose to the real line. Only image-supported points are exported — missing columns are never filled with synthesized values.

Also in the app: text and legend masking, out-of-plot masking, a color picker with multiple color slots, cursor zoom, Ctrl+Z for calibration clicks, CSV / Excel export, and a batch CLI.

---

## Results

One example from DigitizerBench (`D0001-overlapping-altair`, Fig. 1b in the paper): an overlapping two-line plot digitized by the state-of-the-art automatic tool, the state-of-the-art manual tool, and the three LinePilot modes.

| Original plot | ChartOCR | LinePilot (OCR) |
| :---: | :---: | :---: |
| <img src="docs/assets/example-original.png" width="220"> | <img src="docs/assets/example-chartocr.png" width="220"> | <img src="docs/assets/example-linepilot-ocr.png" width="220"> |
| two noisy series, Altair | **no output** | both series, fully automatic |

| PlotDigitizer Pro | LinePilot (standard) | LinePilot (enhanced) |
| :---: | :---: | :---: |
| <img src="docs/assets/example-plotdigitizer-pro.png" width="220"> | <img src="docs/assets/example-linepilot-standard.png" width="220"> | <img src="docs/assets/example-linepilot-enhanced.png" width="220"> |
| sparse manual points | dense, 4 clicks | dense, 4 snapped clicks |

**Automatic pipelines — DigitizerBench-Full (2,980 images per method)**

| Method | FPC-NRMSE ↓ | Output success ↑ | Trusted usability ↑ | Points per line ↑ |
| --- | ---: | ---: | ---: | ---: |
| ChartOCR | 0.953 | 30.2 % | 5.4 % | 29 |
| LineEX | 0.997 | 36.6 % | 0.4 % | 14 |
| **LinePilot (OCR)** | **0.672** | **55.1 %** | **38.2 %** | **1,180** |

**Human-guided tools — DigitizerBench-Lite (60 images per method)**

| Method | FPC-NRMSE ↓ | Output success ↑ | Trusted usability ↑ | Points per line ↑ |
| --- | ---: | ---: | ---: | ---: |
| PlotDigitizer Pro | 0.097 | 100 % | 91.7 % | 475 |
| WebPlotDigitizer | 0.164 | 98.3 % | 86.7 % | 195 |
| Engauge Digitizer | 0.790 | 55.0 % | 23.3 % | 235 |
| **LinePilot (standard)** | 0.101 | **100 %** | 91.7 % | 1,025 |
| **LinePilot (enhanced)** | **0.081** | **100 %** | **93.3 %** | **1,027** |

*FPC-NRMSE* (failure-penalized capped normalized RMSE) assigns a full unit of error to any image whose output is missing, structurally unusable or catastrophically wrong, so it measures reliability as well as accuracy. *Trusted usability* requires the correct line count, finite error on every match, at least 20 valid points and ≥ 80 % coverage. Values are from Table 3 of the paper; the full comparison with LineEX, WebPlotDigitizer and Engauge Digitizer on the example above is in the [online appendix](docs/assets/LinePilot_Online_Appendix.pdf).

---

## Install

### Windows — no Python needed

1. Open the **[latest release](https://github.com/aj24by7/DataDigitizer/releases/latest)** and download **`Digitizer.exe`** from *Assets*. (Optional: `AccuracyTester.exe`, see below.)
2. Double-click it. Nothing to install — the Tesseract OCR engine is bundled inside.
3. On first run Windows SmartScreen may say *"Windows protected your PC"*. Click **More info → Run anyway**. The app simply isn't code-signed.

> If double-clicking does *nothing at all* — no window, no warning — **Smart App Control** (on by default on new Windows 11 installs) is silently blocking unsigned programs. Run from source instead (below); that path is not blocked. Turning Smart App Control off is a one-way door, so prefer running from source.

### macOS

A `Digitizer.app` bundle is built from the companion **[digitizer_mac](https://github.com/RayanA07/digitizer_mac)** repository (`bash build_macos.sh`), which also builds automatically on GitHub Actions.

### From source (Windows / macOS / Linux)

```bash
git clone https://github.com/RayanA07/LinePilot.git
cd LinePilot/Digitizer
python -m pip install -r requirements.txt     # PyQt6, numpy, pillow, pytesseract, openpyxl, PyInstaller
python digitizer_2_11.py                      # launches the GUI
```

Running from source needs the **Tesseract** program installed for OCR features (`pytesseract` alone is not enough); the prebuilt `.exe` bundles it. On Windows, `build.cmd` rebuilds `dist\Digitizer.exe` with PyInstaller.

---

## Using the desktop app

> The complete, click-by-click user guide — every menu, option and error message, written for people who have never used a terminal — is in **[`Digitizer/README.md`](Digitizer/README.md)**. This is the short version.

Work top to bottom. The status bar along the bottom of the window confirms every step or tells you why something didn't run.

1. **Import** — `Import → Import Image` (PNG, JPG, BMP, TIF) or `Paste Image` from the clipboard. The curve color is guessed and shown in the *Selected color* row; use `Tools → Pick Color` and click the curve to change it, or press the green **+** to add a slot for a second curve.
2. **Calibrate** — pick a mode:
   - *OCR:* `Advanced → Axis Scale Detection → Run Axis Detection`, then `Tools → Calibration → Coordinate-Mediated Calibration`. The four **Min-Max Coordinates** boxes are filled automatically.
   - *Standard:* `Tools → Calibration → Manual Calibration` and follow the banner: click X min, X max, Y min, Y max on the image. Type the four axis values into the Min-Max boxes.
   - *Enhanced:* as standard, with `Tools → Calibration → Enhanced Human Click` turned on. Each click is snapped to the nearest tick center; the status bar reports what moved and by how much. `Enhanced Click Settings…` sets the maximum snap distance (1–10 px, default 3). **Ctrl+Z** undoes a click.
3. **Check the axis values.** OCR is good but not perfect — correct any misread box by hand. Drag an edge of the dashed green calibration box if it doesn't sit on your axes.
4. **Mask what isn't data** *(optional)* — `Advanced → Masking` blanks out text, numbers, legends, or hand-drawn rectangles so they aren't mistaken for the curve.
5. **Place Points** — `Tools → Place Points → Run`. The overlay shows every detected point; the status bar reports the count.
6. **Export** — `Export → Export CSV` or `Export Excel`. Each row carries `color_slot, color_r, color_g, color_b, x, y, x_px, y_px`.

Log-scale axes: toggle the small **log** buttons beside the X or Y Min-Max boxes and enter the axis values as printed (e.g. `1` and `1000`).

---

## Command line, batch mode and Python API

All three run from the source folder (`LinePilot/Digitizer`) with Python installed.

```bash
# one image, everything auto-detected (OCR calibration), output to Downloads
python digitizer.py graph.png

# give the axis values yourself, read Y on a log scale, choose the output folder
python digitizer.py graph.png --axis 0,10,0,100 --log-y --out results/

# force the curve color (R,G,B) and show the OCR confidence + full log
python digitizer.py graph.png --color 130,5,255 --verbose 1

# a whole folder: digitized_csvs/, digitized_overlays/ and a batch_report.csv/.json
python digitizer_batch_cli.py figures/ --out digitized/

# score digitized CSVs against reference CSVs, matched by file name
python ../AccuracyTester/accuracy_batch_cli.py --digitized-dir digitized/digitized_csvs --ground-truth-dir truth/ --out scores/
```

Every run writes `<image>_digitized_points.csv` and `<image>_digitized_overlay.png`; `--verbose 1` adds `<image>_log.txt` with the OCR confidence score — a low score is a hint to pass `--axis` yourself. Run `python digitizer.py --help` for every option (`--ticks`, `--log-x`, `--json`, `--normalize-y`, `--limit-to-calibration`, …).

```python
from digitizer_api import digitize_image

out = digitize_image("graph.png",
                     axis_values=(0, 10, 0, 100),   # None → read by OCR
                     color_rgb=None,                # None → auto-detect
                     output_dir="results")
out.csv_path, out.overlay_path, out.point_count, out.used_ocr, out.ocr_confidence
```

### Accuracy Tester

A separate, optional tool (`AccuracyTester.exe`, or `python accuracytester_desktop.py` from `AccuracyTester/`) that measures how faithfully a digitized curve reproduces a reference curve: MAE, RMSE, R², bias, MAPE / sMAPE / WAPE, with overlay, residual and outlier plots, optional constant X-shift optimization, and CSV export. `accuracy_batch_cli.py` scores whole folders.

---

## DigitizerBench

DigitizerBench evaluates digitizers under **controlled, orthogonally balanced** variation of signal, rendering and plot-structure factors, so you can see *which* factors break a tool — not just how often it breaks.

| | |
| --- | --- |
| **DigitizerBench-Full** | 2,980 images: a 2,500-image orthogonal-array core (four strength-3 OA(625, 19, 5, 3) panels) plus 480 matched *bridge* renderings. For automatic evaluation and main-effects ANOVA. |
| **DigitizerBench-Lite** | 60 outcome-independent core images, each rendered under all nine plot-type × renderer combinations. For human-guided evaluation on identical plots. |
| **Signal factors (8 × 5 levels)** | Baseline family and magnitude; extrema count and prominence; feature width, sharpness and asymmetry; signal noise. |
| **Rendering factors (10 × 5 levels)** | Line thickness and color; DPI; blur; figure width and aspect ratio; tick-label size and tick count; X- and Y-axis ranges. |
| **Structure** | Single, overlapping and stacked plots with 1, 2, 3 or 5 lines; rendered with Matplotlib, Plotly and Altair. |
| **Ground truth** | Exact curve and tick coordinates for every image, plus the master seed, factor levels, orthogonal-array matrices, trace-generation rules, bridge identifiers, software versions and image manifest needed to regenerate it. |

**What it found.** For automatic digitization, image presentation matters far more than signal complexity: figure width has the largest effect, then DPI and renderer; noise and most curve-shape factors are not significant, and width × DPI interact. For human-guided digitization, one-pixel lines are the main failure mode — performance stabilizes at 3–5 px.

**Download:** the benchmark package will be released on Hugging Face — *link coming soon*. <!-- TODO: https://huggingface.co/datasets/… -->

---

## Repository layout

```text
LinePilot/
├── Digitizer/           # desktop app (PyQt6), CLI, batch CLI and Python API
│   ├── digitizer_2_11.py    GUI entry point
│   ├── digitizer.py         CLI launcher
│   ├── digitizer_batch_cli.py
│   ├── digitizer_api.py     digitize_image(...)
│   ├── Calibration.py / EnhancedClick.py / AxisReader.py / PointPlacer.py / Masking.py
│   └── build.cmd            one-click Windows build (PyInstaller)
├── AccuracyTester/      # reference-vs-digitized scoring app and batch CLI
├── docs/                # project website (GitHub Pages) and figures used in this README
├── CHANGELOG.md
└── CITATION.cff
```

This repository carries the full commit history of the project. Earlier releases (2.11 – 2.15, published as *Data Digitizer*) are at [aj24by7/DataDigitizer](https://github.com/aj24by7/DataDigitizer); the [changelog](CHANGELOG.md) covers every version.

---

## Citation

If LinePilot or DigitizerBench is useful in your work, please cite the paper — and star the repo, open an issue, or tell us how it went.

```bibtex
@article{ma2026linepilot,
  title   = {LinePilot Digitizer: Line-Plot Recovery with Manual and Automatic Calibration},
  author  = {Ma, Fengbo and Akhtar, Rayan and Joshi, Aakash H. and Li, Xiaoting and
             Sun, Haijian and Xiang, Zhen and Chen, Xianyan and Zhao, Yiping},
  journal = {arXiv preprint arXiv:2609.19377},
  year    = {2026},
  doi     = {10.48550/arXiv.2609.19377}
}
```

\* Equal contribution. † Corresponding authors: zhaoy@uga.edu, zxiangaa@uga.edu, xychen@uga.edu.

## Acknowledgment

This work was supported by the National Science Foundation through the Pathways to Open-Source Ecosystems (POSE) program, award No. 2518273. The authors gratefully acknowledge the support, guidance and collaboration of all members of the SpectraGuru™ development and stakeholder teams. LinePilot is part of the open-source ecosystem for Raman and SERS spectroscopy developed in the Zhao lab at the University of Georgia and its collaborators at the University of Pennsylvania.
