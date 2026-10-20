# LinePilot Digitizer <!-- vX.Y --> (Windows)


Turn a picture of a line plot into numbers — a CSV plus an overlay image showing the detected points. No install, no Python: the Tesseract OCR engine is bundled inside the app.

Three calibration modes, one curve-recovery workflow:
- **Standard** — click four axis ticks.
- **Enhanced** — the same four clicks, snapped to tick centers at sub-pixel precision (`Tools → Calibration → Enhanced Human Click`).
- **OCR** — fully automatic axis reading (`Advanced → Axis Scale Detection`), also used by the command line and batch mode.

## New in this release
<!-- bullets -->

## Install (Windows 10 / 11)
1. Under **Assets** below, download `Digitizer.exe`.
2. Double-click it. On the very first run Windows SmartScreen may show *"Windows protected your PC"* — click **More info**, then **Run anyway**. This is expected; the app simply isn't code-signed.
3. That's it. Optional: `AccuracyTester.exe` compares a digitized CSV against a reference CSV.

If double-clicking does **nothing at all** (no window, no warning), Smart App Control is silently blocking unsigned programs. Run from source instead — see the [README](https://github.com/RayanA07/LinePilot#install). Turning Smart App Control off is a one-way door, so prefer running from source.

Full guide: [README](https://github.com/RayanA07/LinePilot#readme) · Project site: https://rayana07.github.io/LinePilot/

## Known limitations
- OCR can drop minus signs on negative tick labels and misread superscript / power-of-ten axes. Pass `--axis` or type the values in by hand in the app.
- Curves drawn in black or grey on charts with black axes are not reliably separable by the color-based extractor.
- Low-resolution figures are the main cause of wrong numbers; the app warns below 700 px.

---

## If you find LinePilot useful, please cite our paper

> Fengbo Ma, Rayan Akhtar, Aakash H. Joshi, Xiaoting Li, Haijian Sun, Zhen Xiang, Xianyan Chen, Yiping Zhao.
> **LinePilot Digitizer: Line-Plot Recovery with Manual and Automatic Calibration.** arXiv:2609.19377, 2026.
> https://arxiv.org/abs/2609.19377

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

⭐ Star or fork the repo, and [let us know how we did](https://github.com/RayanA07/LinePilot/issues) — bug reports, feature requests and example figures that trip it up are all welcome.

## Acknowledgment
This work was supported by the National Science Foundation through the Pathways to Open-Source Ecosystems (POSE) program, award No. 2518273. The authors gratefully acknowledge the support, guidance and collaboration of all members of the SpectraGuru™ development and stakeholder teams.

Full changelog: https://github.com/RayanA07/LinePilot/blob/main/CHANGELOG.md
