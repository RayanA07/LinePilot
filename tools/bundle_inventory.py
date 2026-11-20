#!/usr/bin/env python3
"""List what is inside a built LinePilot app, and compare those lists across platforms.

The Windows apps are one-file .exe programs and the macOS apps are .app bundles, but they
are meant to carry exactly the same things: the same Python version, the same third-party
packages, the same data files and the same OCR engine with the same language data. This
tool makes that checkable.

    # on the machine that built it (needs PyInstaller, i.e. the build environment)
    python tools/bundle_inventory.py Digitizer/dist/Digitizer.exe -o Digitizer-windows.json
    python tools/bundle_inventory.py Digitizer/dist/Digitizer.app -o Digitizer-macos-arm64.json

    # anywhere: fail if the inventories differ in anything but the OS-specific details
    python tools/bundle_inventory.py --compare Digitizer-*.json

What is compared, and what is allowed to differ:

  compared   app name and version, Python major.minor, third-party Python packages,
             data files (everything that is not a native library or Python's own
             standard library), the OCR bundle's files, the SHA-256 of every language
             model, the Tesseract version and its optional features
  ignored    native libraries (.dll / .pyd vs .dylib / .so) and their count, Python's
             standard library (which differs slightly per OS), PyInstaller's own loader,
             macOS bundle plumbing (Info.plist, code signature), the ".exe" suffix
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

NATIVE_SUFFIXES = (".dll", ".pyd", ".so", ".dylib", ".exe", ".lib", ".a", ".tbd")
# A native library name such as libpng16.16.dylib or Qt6Core.dll, or a framework binary.
NATIVE_RE = re.compile(r"(\.(dll|pyd|so|dylib)(\.\d+)*$)|(\.so\.)|(\.dylib\.)")
# PyInstaller's own pieces and OS plumbing: never compared.
IGNORED_TOP = {
    "base_library.zip", "pyimod01_archive", "pyimod02_importers", "pyimod03_ctypes",
    "pyimod04_pywin32", "pyiboot01_bootstrap", "struct", "PYZ.pyz", "PYZ-00.pyz",
    "_CodeSignature", "Info.plist", "PkgInfo", "CodeResources", "python3__dot__12",
    "Python.framework", "Python", "lib-dynload",
}
# Third-party packages that exist only as an OS-specific helper of something we do bundle.
OS_ONLY_PACKAGES = {
    "win32ctypes", "pefile", "ordlookup", "pywintypes", "pythoncom", "win32",  # Windows
    "macholib", "_scproxy",                                                     # macOS
}


def _stdlib_names() -> set[str]:
    names = set(getattr(sys, "stdlib_module_names", ()))
    # Modules that are stdlib on one OS only.
    names |= {"nt", "ntpath", "nturl2path", "msvcrt", "winreg", "winsound", "_winapi",
              "_overlapped", "_msi", "msilib", "_wmi", "posix", "pwd", "grp", "termios",
              "fcntl", "resource", "_posixsubprocess", "_posixshmem", "_scproxy", "syslog",
              "_curses", "curses", "readline", "_dbm", "_gdbm", "_uuid", "tty", "pty",
              "_tkinter", "tkinter", "_osx_support", "_aix_support"}
    return names


STDLIB = _stdlib_names()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_native(path: str) -> bool:
    """A compiled library, or OS packaging around one (macOS frameworks, wheel .libs dirs)."""
    parts = PurePosixPath(path).parts
    if any(p.endswith((".framework", ".libs")) or p in (".dylibs", "_CodeSignature") for p in parts):
        return True
    name = parts[-1] if parts else path
    return bool(NATIVE_RE.search(name)) or name.endswith(NATIVE_SUFFIXES)


# ---------------------------------------------------------------------------------------
# Reading a build
# ---------------------------------------------------------------------------------------

def _pyz_modules(archive_path: str) -> set[str]:
    """Python modules in the app's PYZ archive, plus its startup scripts as 'script:<name>'."""
    from PyInstaller.archive.readers import CArchiveReader, ZlibArchiveReader

    mods: set[str] = set()
    arc = CArchiveReader(archive_path)
    for name, entry in arc.toc.items():
        typecode = entry[-1]
        if typecode == "s":
            mods.add("script:" + name)
        elif typecode == "z":
            with tempfile.NamedTemporaryFile(suffix=".pyz", delete=False) as tmp:
                tmp.write(arc.extract(name))
            try:
                mods.update(ZlibArchiveReader(tmp.name).toc.keys())
            finally:
                os.unlink(tmp.name)
    return mods


def _read_onefile_exe(path: Path, workdir: Path) -> tuple[list[str], set[str], dict[str, bytes], Path | None]:
    """Files, Python modules, small files we need the bytes of, extracted tesseract dir."""
    from PyInstaller.archive.readers import CArchiveReader

    arc = CArchiveReader(str(path))
    files: list[str] = []
    wanted: dict[str, bytes] = {}
    tess_dir = workdir / "tesseract"
    for name, entry in arc.toc.items():
        typecode = entry[-1]
        rel = name.replace("\\", "/")
        if typecode in ("z", "s", "m", "M", "o"):
            continue  # PYZ, scripts, bootstrap modules, options
        files.append(rel)
        if rel.startswith("vendor/tesseract/") or rel == "version.json":
            data = arc.extract(name)
            wanted[rel] = data
            if rel.startswith("vendor/tesseract/"):
                out = tess_dir / rel[len("vendor/tesseract/"):]
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(data)
    exe = tess_dir / "tesseract.exe"
    return files, _pyz_modules(str(path)), wanted, (tess_dir if exe.exists() else None)


def _read_app_bundle(path: Path) -> tuple[list[str], set[str], dict[str, bytes], Path | None]:
    files: set[str] = set()
    wanted: dict[str, bytes] = {}
    contents = path / "Contents"
    for root, _dirs, names in os.walk(contents):
        for n in names:
            full = Path(root) / n
            rel = full.relative_to(contents).as_posix()
            for prefix in ("Resources/", "Frameworks/", "MacOS/"):
                if rel.startswith(prefix):
                    rel = rel[len(prefix):]
                    break
            files.add(rel)
            if rel.startswith("vendor/tesseract/") or rel == "version.json":
                if full.is_file() and rel not in wanted:
                    wanted[rel] = full.read_bytes()
    exes = [p for p in (contents / "MacOS").iterdir() if p.is_file()]
    mods: set[str] = set()
    for exe in exes:
        try:
            mods |= _pyz_modules(str(exe))
        except Exception:
            pass
    tess = contents / "Resources" / "vendor" / "tesseract"
    if not (tess / "tesseract").exists():
        tess = contents / "Frameworks" / "vendor" / "tesseract"
    return sorted(files), mods, wanted, (tess.resolve() if (tess / "tesseract").exists() else None)


def _python_version(files: list[str]) -> str:
    for f in files:
        m = re.search(r"python3(\d+)\.dll$", f) or re.search(r"Python\.framework/Versions/3\.(\d+)/", f) \
            or re.search(r"python3\.(\d+)/", f) or re.search(r"cpython-3(\d+)-", f) or re.search(r"cp3(\d+)-", f)
        if m:
            return f"3.{m.group(1)}"
    return "unknown"


def _tesseract_info(tess_dir: Path | None) -> dict:
    if tess_dir is None:
        return {"version": None, "features": [], "image_formats": []}
    exe = tess_dir / ("tesseract.exe" if (tess_dir / "tesseract.exe").exists() else "tesseract")
    if platform.system() == "Windows" and exe.suffix != ".exe":
        return {"version": "not runnable here", "features": [], "image_formats": []}
    if platform.system() != "Windows" and exe.suffix == ".exe":
        return {"version": "not runnable here", "features": [], "image_formats": []}
    env = dict(os.environ, TESSDATA_PREFIX=str(tess_dir / "tessdata"))
    try:
        out = subprocess.run([str(exe), "--version"], capture_output=True, text=True, env=env,
                             timeout=60, cwd=str(tess_dir)).stdout
    except Exception as exc:  # pragma: no cover - reported, not raised
        return {"version": f"failed to run: {exc}", "features": [], "image_formats": []}
    first = out.splitlines()[0].strip() if out.strip() else ""
    version = first.split()[1].lstrip("v") if len(first.split()) > 1 else first
    version = re.sub(r"\.\d{8}$", "", version)  # 5.5.3.20260724 (Windows build stamp) -> 5.5.3
    features = sorted({m.group(1) for m in re.finditer(r"Found (libarchive|libcurl)", out)})
    formats = sorted({m.group(1) for m in re.finditer(r"\b(libgif|libjpeg|libpng|libtiff|zlib|libwebp|libopenjp2)\b", out)})
    return {"version": version, "features": features, "image_formats": formats}


def inventory(path: Path) -> dict:
    path = Path(path).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        if path.suffix.lower() == ".exe":
            files, mods, wanted, tess_dir = _read_onefile_exe(path, Path(tmp))
            platform_name = "windows"
        elif path.suffix == ".zip":
            with zipfile.ZipFile(path) as z:
                z.extractall(tmp)
            app = next(Path(tmp).glob("*.app"))
            os.chmod(app, 0o755)
            for p in app.rglob("*"):
                if p.is_file() and ("MacOS" in p.parts or p.name == "tesseract"):
                    p.chmod(0o755)
            files, mods, wanted, tess_dir = _read_app_bundle(app)
            platform_name = "macos"
        else:
            files, mods, wanted, tess_dir = _read_app_bundle(path)
            platform_name = "macos"
        tess_info = _tesseract_info(tess_dir)

    version = None
    if "version.json" in wanted:
        version = json.loads(wanted["version.json"].decode("utf-8")).get("version")

    # Third-party Python packages: top-level names from the PYZ archive and from native
    # extension modules / package folders shipped next to it.
    packages: set[str] = set()
    for m in mods:
        if m.startswith("script:"):
            continue
        top = m.split(".")[0]
        if top and top not in STDLIB and not top.startswith(("pyi_", "pyimod", "_pyi", "_sysconfigdata_")):
            packages.add(top)
    data_files: set[str] = set()
    native_count = 0
    for f in files:
        top = f.split("/")[0]
        if top in IGNORED_TOP or f.startswith("vendor/tesseract/") or top.startswith(("pyi_rth", "pyiboot")):
            continue
        if _is_native(f):
            native_count += 1
            # an extension module inside a package folder still names the package
            if "/" in f and top not in STDLIB and not top.endswith((".libs", ".dist-info")):
                packages.add(top)
            continue
        if top.endswith(".dist-info"):
            packages.add(re.sub(r"-[0-9].*$", "", top[: -len(".dist-info")]).replace("-", "_").lower() + " (dist-info)")
            continue
        if "/" in f and top not in STDLIB:
            data_files.add(f)
            packages.add(top)
    packages = {p for p in packages if p.split(" ")[0] not in OS_ONLY_PACKAGES}

    tess_files = set()
    tessdata = {}
    for rel, data in wanted.items():
        if not rel.startswith("vendor/tesseract/"):
            continue
        sub = rel[len("vendor/tesseract/"):]
        if sub.endswith(".traineddata"):
            tessdata[sub] = _sha256(data)
        if _is_native(sub) and sub not in ("tesseract.exe",):
            continue
        tess_files.add(sub[:-4] if sub == "tesseract.exe" else sub)

    runtime_hooks = sorted(m[len("script:"):] for m in mods if m.startswith("script:pyi_rth_"))
    return {
        "app": path.name.split(".")[0].split("-")[0],
        "platform": platform_name,
        "arch": platform.machine().lower(),
        "version": version,
        "python": _python_version(files),
        "packages": sorted(packages),
        "data_files": sorted(data_files),
        "runtime_hooks": runtime_hooks,
        "tesseract": {
            **tess_info,
            "files": sorted(tess_files),
            "tessdata_sha256": dict(sorted(tessdata.items())),
        },
        "info": {"native_libraries": native_count, "python_modules": len(mods)},
    }


# ---------------------------------------------------------------------------------------
# Comparing
# ---------------------------------------------------------------------------------------

COMPARED = ("app", "version", "python", "packages", "data_files", "runtime_hooks")
TESS_COMPARED = ("version", "features", "image_formats", "files", "tessdata_sha256")


def compare(paths: list[Path]) -> int:
    invs = [(p.name, json.loads(p.read_text(encoding="utf-8"))) for p in paths]
    by_app: dict[str, list[tuple[str, dict]]] = {}
    for name, inv in invs:
        by_app.setdefault(inv["app"], []).append((name, inv))
    problems = 0
    for app, group in sorted(by_app.items()):
        ref_name, ref = group[0]
        labels = ", ".join(f"{n} ({i['platform']} {i['arch']})" for n, i in group)
        print(f"== {app}: {labels}")
        for name, inv in group[1:]:
            for key in COMPARED:
                problems += _diff(app, key, ref_name, ref.get(key), name, inv.get(key))
            for key in TESS_COMPARED:
                problems += _diff(app, f"tesseract.{key}", ref_name, ref["tesseract"].get(key),
                                  name, inv["tesseract"].get(key))
        for name, inv in group:
            t = inv["tesseract"]
            print(f"   {name}: version {inv['version']}, Python {inv['python']}, "
                  f"{len(inv['packages'])} packages, {len(inv['data_files'])} data files, "
                  f"Tesseract {t.get('version') or '-'} {'+'.join(t.get('features') or []) or ''}, "
                  f"{inv['info']['native_libraries']} native libraries")
    if problems:
        print(f"::error::{problems} difference(s) between the Windows and macOS builds")
        return 1
    print("Windows and macOS builds contain the same components.")
    return 0


def _diff(app: str, key: str, an: str, a, bn: str, b) -> int:
    if a == b:
        return 0
    if isinstance(a, list) and isinstance(b, list):
        only_a = sorted(set(a) - set(b))
        only_b = sorted(set(b) - set(a))
        print(f"::error::{app} {key} differs")
        if only_a:
            print(f"   only in {an}: {only_a[:40]}{' …' if len(only_a) > 40 else ''}")
        if only_b:
            print(f"   only in {bn}: {only_b[:40]}{' …' if len(only_b) > 40 else ''}")
        return 1
    if isinstance(a, dict) and isinstance(b, dict):
        keys = sorted(set(a) | set(b))
        bad = [k for k in keys if a.get(k) != b.get(k)]
        print(f"::error::{app} {key} differs for {bad}: {an}={ {k: a.get(k) for k in bad} } "
              f"{bn}={ {k: b.get(k) for k in bad} }")
        return 1
    if key == "tesseract.version" and "not runnable here" in (str(a), str(b)):
        return 0
    print(f"::error::{app} {key}: {an}={a!r} vs {bn}={b!r}")
    return 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", type=Path, help="a built app (.exe, .app or .app zip), or inventories with --compare")
    ap.add_argument("-o", "--output", type=Path, help="write the inventory JSON here")
    ap.add_argument("--compare", action="store_true", help="compare inventory JSON files")
    args = ap.parse_args(argv)
    if args.compare:
        return compare(args.paths)
    if len(args.paths) != 1:
        ap.error("give one built app (or use --compare)")
    inv = inventory(args.paths[0])
    text = json.dumps(inv, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
        print(f"{inv['app']} {inv['version']} ({inv['platform']}): Python {inv['python']}, "
              f"{len(inv['packages'])} packages, Tesseract {inv['tesseract']['version']} -> {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
