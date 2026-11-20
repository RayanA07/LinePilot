# Vendor a self-contained Tesseract OCR runtime into Digitizer\vendor\tesseract.
#
# The Windows twin of vendor_tesseract_macos.sh. Both read tesseract-lock.json and produce
# the same layout, so Digitizer.exe and Digitizer.app carry the same OCR engine:
#
#   vendor\tesseract\tesseract.exe        the pinned Tesseract version
#   vendor\tesseract\*.dll                exactly the libraries tesseract.exe loads
#   vendor\tesseract\tessdata\eng.traineddata, osd.traineddata   (SHA-256 checked)
#   vendor\tesseract\tessdata\configs\, tessconfigs\
#   vendor\tesseract\doc\AUTHORS, LICENSE, README.md
#
# Uses the official Windows build of the pinned version (checksum-verified), installed
# silently into -InstallDir. An existing install of the same version there is reused.
#
#   powershell -ExecutionPolicy Bypass -File vendor_tesseract_windows.ps1
#   ... -Python C:\path\to\python.exe        (needs pefile; build_windows.ps1 passes its venv)
#   ... -InstallDir C:\some\folder           (where the pinned installer puts Tesseract)

param(
    [string]$Python = "",
    [string]$InstallDir = ""
)

$ErrorActionPreference = "Stop"
# (No 2>&1 on native commands below: Windows PowerShell 5.1 turns redirected stderr into
# terminating errors under "Stop". Tesseract prints --version and --list-langs to stdout.)
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Lock = Get-Content (Join-Path $Root "tesseract-lock.json") -Raw | ConvertFrom-Json
$Version = $Lock.version
$Vendor = Join-Path $Root "vendor\tesseract"
if (-not $InstallDir) { $InstallDir = Join-Path $env:LOCALAPPDATA "LinePilot\tesseract-$Version" }

function Get-Sha256([string]$Path) { (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLower() }

function Test-PinnedTesseract([string]$Exe) {
    if (-not (Test-Path -LiteralPath $Exe)) { return $false }
    $first = (& $Exe --version | Select-Object -First 1) -as [string]
    return ($first -match ("^tesseract v?" + [regex]::Escape($Version) + "(\.|\s|$)"))
}

function Invoke-Python {
    if ($Python) { & $Python @args } else { & py @args }
}

# 1. The pinned Tesseract build.
$TessExe = Join-Path $InstallDir "tesseract.exe"
if (Test-PinnedTesseract $TessExe) {
    Write-Host "Using Tesseract $Version already installed at $InstallDir"
} else {
    $Installer = Join-Path $env:TEMP (Split-Path $Lock.windows.installer -Leaf)
    Write-Host "Downloading Tesseract $Version ($($Lock.windows.installer))"
    Invoke-WebRequest -Uri $Lock.windows.installer -OutFile $Installer -UseBasicParsing
    $got = Get-Sha256 $Installer
    if ($got -ne $Lock.windows.sha256) { throw "Tesseract installer checksum mismatch: got $got, expected $($Lock.windows.sha256)" }
    Write-Host "Installing silently into $InstallDir"
    # NSIS: /D= must come last and must not be quoted, even with spaces.
    $p = Start-Process -FilePath $Installer -ArgumentList "/S /D=$InstallDir" -Wait -PassThru
    if ($p.ExitCode -ne 0) { throw "Tesseract installer exited with code $($p.ExitCode)" }
    if (-not (Test-PinnedTesseract $TessExe)) { throw "Tesseract $Version not found at $TessExe after install" }
}

# 2. Copy the program and exactly the DLLs it loads.
if (Test-Path $Vendor) { Remove-Item -Recurse -Force $Vendor }
New-Item -ItemType Directory -Force -Path (Join-Path $Vendor "tessdata") | Out-Null
Copy-Item -LiteralPath $TessExe -Destination $Vendor
$Dlls = Invoke-Python (Join-Path $Root "..\tools\pe_deps.py") $TessExe
if ($LASTEXITCODE) { throw "could not list tesseract.exe's DLLs (is pefile installed?)" }
foreach ($dll in $Dlls) { Copy-Item -LiteralPath (Join-Path $InstallDir $dll) -Destination $Vendor }

# 3. Configs and the license / authors / readme, from the same release.
foreach ($dir in "configs", "tessconfigs") {
    Copy-Item -Recurse -LiteralPath (Join-Path $InstallDir "tessdata\$dir") -Destination (Join-Path $Vendor "tessdata\$dir")
}
New-Item -ItemType Directory -Force -Path (Join-Path $Vendor "doc") | Out-Null
foreach ($doc in "AUTHORS", "LICENSE", "README.md") {
    Copy-Item -LiteralPath (Join-Path $InstallDir "doc\$doc") -Destination (Join-Path $Vendor "doc")
}

# 4. The language models, from the pinned URLs, checksum-verified.
foreach ($model in $Lock.tessdata.PSObject.Properties) {
    $dest = Join-Path $Vendor "tessdata\$($model.Name)"
    Invoke-WebRequest -Uri $model.Value.url -OutFile $dest -UseBasicParsing
    $got = Get-Sha256 $dest
    if ($got -ne $model.Value.sha256) { throw "$($model.Name) checksum mismatch: got $got, expected $($model.Value.sha256)" }
}

# 5. Prove the vendored copy runs on its own, is the pinned version, has the same optional
#    features as the macOS build, and finds its own language data.
$env:TESSDATA_PREFIX = Join-Path $Vendor "tessdata"
$VendoredExe = Join-Path $Vendor "tesseract.exe"
$info = (& $VendoredExe --version) -join "`n"
if (-not (Test-PinnedTesseract $VendoredExe)) { throw "vendored tesseract is not version $Version`n$info" }
foreach ($feature in $Lock.required_features) {
    if ($info -notmatch "Found $feature") { throw "vendored tesseract was built without $feature`n$info" }
}
$langs = (& $VendoredExe --list-langs) -join "`n"
foreach ($lang in "eng", "osd") {
    if ($langs -notmatch "(?m)^$lang\s*$") { throw "vendored tesseract cannot list '$lang'`n$langs" }
}
Remove-Item Env:\TESSDATA_PREFIX

$count = (Get-ChildItem $Vendor -Recurse -File).Count
Write-Host "Vendored Tesseract $Version at $Vendor ($($Dlls.Count) DLLs, $count files)"
