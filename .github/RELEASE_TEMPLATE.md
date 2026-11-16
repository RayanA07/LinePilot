# LinePilot Digitizer <!-- vX.Y -->

Turn a picture of a line plot into numbers — a CSV plus an overlay image showing the detected points. **No install, no Python:** the Tesseract OCR engine is bundled inside every app.

Three calibration modes, one curve-recovery workflow:
- **Standard** — click four axis ticks.
- **Enhanced** — the same four clicks, snapped to tick centers at sub-pixel precision (`Tools → Calibration → Enhanced Human Click`).
- **OCR** — fully automatic axis reading (`Advanced → Axis Scale Detection`), also used by the command line and batch mode.

## Download

| Your computer | Download from **Assets** below | Then |
| --- | --- | --- |
| **Windows 10 / 11** (64-bit) | `Digitizer.exe` | double-click it |
| **Mac with Apple Silicon** (M1, M2, M3, M4…) | `Digitizer-macOS-AppleSilicon.zip` | double-click the zip, then open `Digitizer.app` |
| **Mac with an Intel processor** | `Digitizer-macOS-Intel.zip` | double-click the zip, then open `Digitizer.app` |

Not sure which Mac you have? Apple menu → **About This Mac**: *Chip: Apple M…* means Apple Silicon; *Processor: …Intel…* means Intel.

Optional: the **Accuracy Tester** (`AccuracyTester.exe`, `AccuracyTester-macOS-AppleSilicon.zip`, `AccuracyTester-macOS-Intel.zip`) compares a digitized CSV against a reference CSV.

Windows and macOS are built from the same code, and every file below was tested before release on a clean machine: the built app read the axes of a real Raman spectrum with its own bundled OCR and matched the true data, and both apps opened.

## New in this release
<!-- bullets -->

## Install

### Windows
1. Download `Digitizer.exe` and double-click it.
2. First run only: Windows SmartScreen may say *"Windows protected your PC"* — click **More info**, then **Run anyway**. The app simply isn't code-signed.
3. That's it — nothing is installed; the `.exe` is the program.

If double-clicking does **nothing at all**, Smart App Control is silently blocking unsigned programs; run from source instead (see the guide).

### macOS
**Requires** <!-- macos-min -->. On Sequoia, install the latest updates first (System Settings → General → Software Update).
1. Download the zip for your Mac's chip and double-click it to unpack **`Digitizer.app`**. Drag it into **Applications** if you like.
2. First launch only: macOS says it *"cannot verify"* the app — click **Done**, then open **System Settings → Privacy & Security**, scroll down and click **Open Anyway**. The app simply isn't notarized with a paid Apple Developer ID.
3. That's it. If macOS ever calls the app *"damaged"*, run `xattr -dr com.apple.quarantine /Applications/Digitizer.app` once in Terminal.

Step-by-step guide with screenshots: [Install on Windows](https://github.com/RayanA07/LinePilot/blob/main/Digitizer/README.md#on-windows) · [Install on macOS](https://github.com/RayanA07/LinePilot/blob/main/Digitizer/README.md#on-a-mac) · [README](https://github.com/RayanA07/LinePilot#readme) · Project site: https://rayana07.github.io/LinePilot/

## Known limitations
- OCR can drop minus signs on negative tick labels and misread superscript / power-of-ten axes. Pass `--axis` or type the values in by hand in the app.
- Curves drawn in black or grey on charts with black axes are not reliably separable by the color-based extractor.
- Low-resolution figures are the main cause of wrong numbers; the app warns below 700 px.

---

## If you find LinePilot useful, please cite our paper

> Fengbo Ma, Rayan Akhtar, Aakash Joshi, Xiaoting Li, Haijian Sun, Zhen Xiang, Xianyan Chen, Yiping Zhao.
> **LinePilot Digitizer: Line-Plot Recovery with Manual and Automatic Calibration.** arXiv:2609.19377, 2026.
> https://arxiv.org/abs/2609.19377

```bibtex
@article{ma2026linepilot,
  title   = {LinePilot Digitizer: Line-Plot Recovery with Manual and Automatic Calibration},
  author  = {Ma, Fengbo and Akhtar, Rayan and Joshi, Aakash and Li, Xiaoting and
             Sun, Haijian and Xiang, Zhen and Chen, Xianyan and Zhao, Yiping},
  journal = {arXiv preprint arXiv:2609.19377},
  year    = {2026},
  doi     = {10.48550/arXiv.2609.19377}
}
```

The benchmark from the paper, **DigitizerBench**, is on Hugging Face: https://huggingface.co/datasets/LinePilot/DigitizerBench

⭐ Star or fork the repo, and [let us know how we did](https://github.com/RayanA07/LinePilot/issues/new/choose) — installation reports, bug reports, feature requests and example figures that trip it up are all welcome. Questions and collaborations: Fengbo.Ma@uga.edu.

## Acknowledgment
This work was supported by the National Science Foundation through the Pathways to Open-Source Ecosystems (POSE) program, award No. 2518273. The authors gratefully acknowledge the support, guidance and collaboration of all members of the SpectraGuru™ development and stakeholder teams.

Full changelog: https://github.com/RayanA07/LinePilot/blob/main/CHANGELOG.md
