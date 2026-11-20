# Build Digitizer.exe on Windows.
#
# The Windows twin of build_macos.sh: the same steps from the same pinned inputs, so the
# .exe and the .app contain the same things.
#   1. a clean build environment (.build-venv) on the Python in ..\.python-version,
#      with exactly the packages in ..\constraints.txt
#   2. the OCR engine pinned in tesseract-lock.json   (vendor_tesseract_windows.ps1)
#   3. PyInstaller with digitizer.spec                 (settings shared via tools\build_common.py)
#   4. an inventory of what went in                    (tools\bundle_inventory.py)
#
#   .\build_windows.ps1                 or double-click build.cmd
#   .\build_windows.ps1 -SkipInstall    reuse the existing build environment
#   $env:PYTHON = "C:\path\to\python.exe"   use that Python instead of "py -3.12"

param(
    [switch]$SkipInstall,
    [string]$TesseractDir = ""
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
Set-Location $ScriptDir
$PyVersion = (Get-Content (Join-Path $RepoRoot ".python-version") -Raw).Trim()
$Venv = Join-Path $ScriptDir ".build-venv"
$VenvPy = Join-Path $Venv "Scripts\python.exe"

function Invoke-BasePython {
    # Plain $args (no [Parameter]) so "-m" reaches Python in Windows PowerShell 5.1 too.
    if ($env:PYTHON) { & $env:PYTHON @args } else { & py "-$PyVersion" @args }
}

# 1. Clean build environment with the pinned packages.
if (-not $SkipInstall -or -not (Test-Path $VenvPy)) {
    if (Test-Path $Venv) { Remove-Item -Recurse -Force $Venv }
    Invoke-BasePython -m venv $Venv
    if ($LASTEXITCODE -or -not (Test-Path $VenvPy)) {
        throw "Could not create a build environment with Python $PyVersion. Install it from https://python.org, or set `$env:PYTHON to a python.exe."
    }
    & $VenvPy -m pip install --disable-pip-version-check --only-binary=:all: -r requirements.txt -c ..\constraints.txt
    if ($LASTEXITCODE) { throw "pip install failed" }
}
$got = (& $VenvPy -c "import sys; print('%d.%d' % sys.version_info[:2])").Trim()
if ($got -ne $PyVersion -and -not $env:ALLOW_ANY_PYTHON) {
    throw "The build environment uses Python $got, but LinePilot is built with $PyVersion (.python-version) so Windows and macOS bundle the same thing. Install Python $PyVersion, or set ALLOW_ANY_PYTHON=1 to build anyway."
}

# 2. The pinned OCR engine.
$vendorArgs = @{ Python = $VenvPy }
if ($TesseractDir) { $vendorArgs.InstallDir = $TesseractDir }
& (Join-Path $ScriptDir "vendor_tesseract_windows.ps1") @vendorArgs

# 3. PyInstaller.
& $VenvPy -m PyInstaller --clean --noconfirm digitizer.spec
if ($LASTEXITCODE -or -not (Test-Path "dist\Digitizer.exe")) { throw "PyInstaller did not produce dist\Digitizer.exe" }

# 4. What went in (compared against the macOS builds in CI).
& $VenvPy ..\tools\bundle_inventory.py dist\Digitizer.exe -o dist\Digitizer-inventory-Windows.json
if ($LASTEXITCODE) { throw "bundle inventory failed" }

$Version = (Get-Content "version.json" -Raw | ConvertFrom-Json).version
Write-Host ""
Write-Host "Built: $ScriptDir\dist\Digitizer.exe  (LinePilot Digitizer $Version, Python $got)"
