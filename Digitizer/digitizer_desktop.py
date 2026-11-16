from __future__ import annotations

import os

from digitizer_2_11 import configure_runtime_paths, launch_digitizer_gui


def _bundle_self_test(image: str) -> int:
    """Release-pipeline check: digitize one image with the OCR runtime *inside the built
    app* and exit without opening a window.

    The CLI cannot test this - it runs from source, against whatever Tesseract the build
    machine has installed. Only the frozen app resolves vendor/tesseract from inside its
    own bundle, so CI launches it with LINEPILOT_SELFTEST=<image> (after removing the
    machine's own Tesseract) to prove the shipped app can read axes on a clean computer.
    Ordinary launches never set the variable and go straight to the GUI.

    The result is printed and, if LINEPILOT_SELFTEST_REPORT names a file, also written
    there - a windowed Windows .exe has no console, so CI reads the file instead.
    """
    import json

    from digitizer_api import digitize_image

    out_dir = os.environ.get("LINEPILOT_SELFTEST_OUT") or None

    def report(payload: dict) -> None:
        line = json.dumps(payload)
        print(line)
        path = os.environ.get("LINEPILOT_SELFTEST_REPORT")
        if path:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(line + "\n")

    try:
        result = digitize_image(image, output_dir=out_dir)
    except Exception as exc:  # report, don't crash: CI reads the JSON
        report({"ok": False, "error": f"{type(exc).__name__}: {exc}",
                "tesseract": os.environ.get("TESSERACT_CMD")})
        return 1
    report({"ok": True, "points": result.point_count, "used_ocr": result.used_ocr,
            "ocr_confidence": result.ocr_confidence,
            "axis_values": list(result.axis_values),
            "csv": result.csv_path,
            "tesseract": os.environ.get("TESSERACT_CMD")})
    return 0


if __name__ == "__main__":
    configure_runtime_paths()
    _self_test_image = os.environ.get("LINEPILOT_SELFTEST")
    if _self_test_image:
        raise SystemExit(_bundle_self_test(_self_test_image))
    raise SystemExit(launch_digitizer_gui())
