#!/usr/bin/env bash
# Guard against Windows-only text creeping back into the macOS CLI help.
#
# Help text is written once in its Windows form and rewritten for macOS at print time by
# Digitizer/platform_info.py (for_this_os). The failure mode is a new example added later
# that the rewrite doesn't cover - a `C:\Users\...` path or `tesseract.exe` printed straight
# to a Mac user's terminal by --help or `digitizer.py template`. Cheap to check, easy to
# regress, so it runs in CI.
#
# Every command must exit 0 AND produce output. A guard that greps empty output would
# report "clean" when the interpreter is missing, which is worse than no guard at all.
#
# Run:  bash tools/check_help_text.sh    (from the repo root)
#       PYTHON=python bash tools/check_help_text.sh   (if python3 is not the right name)

set -uo pipefail

cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-python3}"

if ! "$PYTHON" -c 'import sys; sys.exit(0)' >/dev/null 2>&1; then
  echo "error: '$PYTHON' is not a working Python interpreter. Set PYTHON=... and retry." >&2
  exit 2
fi

out=""
collect() {  # collect <dir> <args...>
  local dir="$1"; shift
  local text status
  text="$(cd "$dir" && "$PYTHON" "$@" 2>&1)"
  status=$?
  if [ $status -ne 0 ]; then
    echo "error: '$PYTHON $*' in $dir exited $status" >&2
    printf '%s\n' "$text" >&2
    exit 2
  fi
  if [ -z "${text//[[:space:]]/}" ]; then
    echo "error: '$PYTHON $*' in $dir printed nothing - cannot verify its help text" >&2
    exit 2
  fi
  out+="
--- $dir: $PYTHON $* ---
$text"
}

collect Digitizer      digitizer.py --help
collect Digitizer      digitizer.py template
collect Digitizer      digitizer_batch_cli.py --help
collect AccuracyTester accuracy_batch_cli.py --help

# 'C:\' / 'D:\' drive paths, .exe references, and `py script.py` (the Windows launcher).
pattern='C:\\|D:\\|\.exe|(^|[^a-zA-Z0-9_-])py [a-z_]+\.py'

if printf '%s\n' "$out" | grep -nE "$pattern"; then
  echo ""
  echo "::error::macOS CLI help still contains Windows-only text (matches shown above)"
  exit 1
fi

echo "CLI help is macOS-clean (no C:\\ paths, .exe references, or 'py script.py')"
