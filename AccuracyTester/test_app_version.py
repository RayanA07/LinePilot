import json
from pathlib import Path

import app_version


def test_version_matches_version_json():
    data = json.loads((Path(__file__).parent / "version.json").read_text(encoding="utf-8"))
    assert app_version.APP_VERSION == data["version"]


def test_fallback_matches_version_json():
    data = json.loads((Path(__file__).parent / "version.json").read_text(encoding="utf-8"))
    assert app_version._FALLBACK_VERSION == data["version"]


def test_title_names_the_app_and_version():
    assert app_version.APP_TITLE == f"LinePilot Accuracy Tester {app_version.APP_VERSION}"
