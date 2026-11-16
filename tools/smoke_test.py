"""End-to-end smoke test: chart image -> batch digitize -> batch accuracy score.

Nothing here is mocked. It renders real charts with matplotlib (so the true x,y are
known exactly), runs the batch digitizer over the folder, then runs the batch accuracy
CLI against the ground truth and asserts every figure came back within tolerance.

This is what proves the CLI actually works on each platform it ships for (it runs on
Windows and on both Mac chips in .github/workflows/release.yml): the unit tests cover the
statistics, but only this exercises OCR axis detection, colour auto-pick, calibration,
point extraction, file pairing and scoring together.

Run:  python3 tools/smoke_test.py            (from the repo root)
      python3 tools/smoke_test.py --keep     (leave the generated files for inspection)

Exit code 0 = everything passed; 1 = something regressed (details printed).
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Each figure is drawn with a distinct colour and axis range so the smoke test covers
# auto colour-pick and OCR on more than one layout. nrmse_range_pct is RMSE as a percent
# of the figure's own y-range, so one tolerance is meaningful across all of them.
MAX_NRMSE_PCT = 2.0

FIGURES = [
    # name,          colour,      x range,     y = f(x)
    ("smoke_sine", "#1f77b4", (0.0, 10.0), lambda x: 0.5 + 0.4 * __import__("math").sin(x)),
    ("smoke_line", "#d62728", (0.0, 100.0), lambda x: 2.0 * x + 10.0),
    ("smoke_decay", "#2ca02c", (0.0, 5.0), lambda x: 100.0 * __import__("math").exp(-0.5 * x)),
]


def build_figures(images_dir: Path, truth_dir: Path) -> None:
    """Render each chart as a PNG and write its exact x,y as the ground truth CSV."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    images_dir.mkdir(parents=True, exist_ok=True)
    truth_dir.mkdir(parents=True, exist_ok=True)

    for name, colour, (x0, x1), fn in FIGURES:
        n = 400
        xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
        ys = [fn(x) for x in xs]

        # dpi matters: at ~110 the axis labels are only a few pixels tall and OCR misreads
        # them (the digitizer warns about exactly this). 200 is the resolution its own
        # warning recommends, and is what a real figure exported for print would be.
        fig, ax = plt.subplots(figsize=(8, 6), dpi=200)
        ax.plot(xs, ys, color=colour, linewidth=2.0)
        ax.set_xlim(x0, x1)
        ax.margins(y=0.05)
        fig.tight_layout()
        fig.savefig(images_dir / f"{name}.png")
        plt.close(fig)

        # The header row matters: the batch scorer pairs on x/y column names.
        with open(truth_dir / f"{name}.csv", "w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["x", "y"])
            writer.writerows(zip(xs, ys))

    print(f"built {len(FIGURES)} figures in {images_dir}")


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    print(f"\n$ {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    sys.stdout.write(proc.stdout)
    if proc.stderr.strip():
        sys.stderr.write(proc.stderr)
    return proc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--keep", action="store_true",
                        help="Keep the generated files instead of using a temp folder.")
    args = parser.parse_args()

    workdir = (REPO_ROOT / "smoke_out") if args.keep else Path(tempfile.mkdtemp(prefix="dd_smoke_"))
    images = workdir / "images"
    truth = workdir / "truth"
    out = workdir / "run"

    build_figures(images, truth)

    # 1. Batch digitize the whole folder.
    proc = run([sys.executable, "digitizer_batch_cli.py", str(images), "--output-dir", str(out)],
               cwd=REPO_ROOT / "Digitizer")
    if proc.returncode != 0:
        print(f"\nFAIL: batch digitizer exited {proc.returncode}")
        return 1

    report = json.loads((out / "batch_report.json").read_text(encoding="utf-8"))
    if report["failed"] or report["succeeded"] != len(FIGURES):
        print(f"\nFAIL: expected {len(FIGURES)} images digitized, got "
              f"{report['succeeded']} ok / {report['failed']} failed")
        for row in report["images"]:
            if row["status"] != "ok":
                print(f"  {row['image']}: {row['status']} - {row['reason']}")
        return 1

    # 2. Score them against the ground truth.
    proc = run([sys.executable, "accuracy_batch_cli.py",
                "--digitized-dir", str(out / "digitized_csvs"),
                "--ground-truth-dir", str(truth),
                "--output-dir", str(out / "accuracy_report")],
               cwd=REPO_ROOT / "AccuracyTester")
    if proc.returncode != 0:
        print(f"\nFAIL: accuracy batch CLI exited {proc.returncode}")
        return 1

    # 3. Every figure must be scored, and scored well.
    rows = list(csv.DictReader(open(out / "accuracy_report" / "accuracy_report.csv",
                                    encoding="utf-8")))
    scored = {r["image"]: r for r in rows if r["status"] == "ok"}

    print("\n--- accuracy ---")
    failures = []
    for name, *_ in FIGURES:
        row = scored.get(name)
        if row is None:
            status = next((r["status"] for r in rows if r["image"] == name), "missing")
            failures.append(f"{name}: not scored ({status})")
            continue
        nrmse = float(row["nrmse_range_pct"])
        verdict = "ok" if nrmse <= MAX_NRMSE_PCT else "TOO HIGH"
        print(f"  {name:<14} nrmse={nrmse:6.3f}%  r2={float(row['r2']):.5f}  "
              f"points={row['points_compared']}  {verdict}")
        if nrmse > MAX_NRMSE_PCT:
            failures.append(f"{name}: nrmse {nrmse:.3f}% exceeds {MAX_NRMSE_PCT}%")

    if failures:
        print("\nFAIL:")
        for line in failures:
            print(f"  {line}")
        return 1

    print(f"\nPASS: {len(FIGURES)} figures digitized and scored within {MAX_NRMSE_PCT}% of range")
    if args.keep:
        print(f"files kept in {workdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
