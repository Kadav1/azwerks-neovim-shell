#!/usr/bin/env zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

python3 -m py_compile "$ROOT_DIR"/src/azwerks_nvim_shell/*.py
python3 -m py_compile \
  "$ROOT_DIR/scripts/probe-vte-child-lifecycle.py" \
  "$ROOT_DIR/scripts/probe-vte-lifecycle-variants.py"
PYTHONPATH="$ROOT_DIR/src" python3 -m unittest discover -s "$ROOT_DIR/tests" -p 'test_*.py'
"$ROOT_DIR/tests/test_install_scripts.sh"
python3 - <<'PY'
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Vte", "3.91")
from gi.repository import Gtk, Vte
print("GTK/VTE import smoke OK")
PY

if command -v desktop-file-validate >/dev/null; then
  desktop-file-validate "$ROOT_DIR/data/com.azwerks.NvimShell.desktop"
else
  echo "desktop-file-validate not found; skipping desktop validation"
fi

test -x "$ROOT_DIR/scripts/dev-run.sh"
test -x "$ROOT_DIR/scripts/install-user.sh"
test -x "$ROOT_DIR/scripts/uninstall-user.sh"
test -x "$ROOT_DIR/scripts/probe-vte-child-lifecycle.py"
test -x "$ROOT_DIR/scripts/probe-vte-lifecycle-variants.py"
test -s "$ROOT_DIR/data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg"
command grep -q "<svg" "$ROOT_DIR/data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg"

echo "Smoke test passed."
