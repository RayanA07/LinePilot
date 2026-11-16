"""Release-pipeline checks on the BUILT apps (used by .github/workflows/release.yml).

  check_selftest.py REPORT --app-marker M [--forbid F]
      REPORT is the JSON the frozen Digitizer writes when launched with LINEPILOT_SELFTEST
      (see Digitizer/digitizer_desktop.py). Passes only if the app digitized the demo Raman
      spectrum with OCR, read its axes exactly, found a full curve, and used a Tesseract whose
      path contains M (i.e. the copy bundled inside the app) and not F.

  check_selftest.py --score ACCURACY_CSV
      Reads the Accuracy Tester's report for the same run and requires the recovered curve to
      be within 2 % of the true data's range (NRMSE).

Same script on Windows and macOS, so both platforms are held to the same bar.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys

EXPECTED_AXES = [400.0, 1800.0, 2000.0, 14000.0]  # x min, x max, y min, y max of the demo
MIN_POINTS = 500
MAX_NRMSE_PCT = 2.0


def check_report(path: str, marker: str, forbid: str | None) -> list[str]:
    with open(path, encoding="utf-8-sig") as fh:
        r = json.loads(fh.read().strip().splitlines()[-1])
    print(json.dumps(r))
    problems = []
    if not r.get("ok"):
        return [f"self-test failed: {r.get('error')}"]
    if not r.get("used_ocr"):
        problems.append("the axes were not read by OCR")
    tesseract = r.get("tesseract") or ""
    if marker.lower() not in tesseract.lower():
        problems.append(f"used a Tesseract outside the app: {tesseract!r}")
    if forbid and forbid.lower() in tesseract.lower():
        problems.append(f"used the machine's own Tesseract: {tesseract!r}")
    if r.get("axis_values") != EXPECTED_AXES:
        problems.append(f"OCR misread the axes: {r.get('axis_values')} (expected {EXPECTED_AXES})")
    if (r.get("points") or 0) <= MIN_POINTS:
        problems.append(f"only {r.get('points')} points recovered")
    if not problems:
        print(f"bundled OCR OK: {tesseract}")
    return problems


def check_score(path: str) -> list[str]:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = [row for row in csv.DictReader(fh) if row.get("image") == "example_raman"]
    if not rows:
        return ["example_raman is missing from the accuracy report"]
    row = rows[0]
    if row.get("status") != "ok":
        return [f"accuracy scoring failed: {row}"]
    nrmse = float(row["nrmse_range_pct"])
    print(f"example_raman: NRMSE {nrmse:.3f}% of range, R^2 {float(row['r2']):.5f}")
    return [] if nrmse < MAX_NRMSE_PCT else [f"NRMSE {nrmse:.3f}% is not below {MAX_NRMSE_PCT}%"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("report", nargs="?")
    parser.add_argument("--app-marker", default="")
    parser.add_argument("--forbid")
    parser.add_argument("--score")
    args = parser.parse_args(argv)
    if args.score:
        problems = check_score(args.score)
    elif args.report and args.app_marker:
        problems = check_report(args.report, args.app_marker, args.forbid)
    else:
        parser.error("give REPORT with --app-marker, or --score ACCURACY_CSV")
    for p in problems:
        print(f"::error::{p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
