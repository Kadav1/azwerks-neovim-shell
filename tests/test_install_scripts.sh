#!/usr/bin/env zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TMP_HOME="$(mktemp -d)"

cleanup() {
  rm -rf "$TMP_HOME"
}
trap cleanup EXIT

cd "$ROOT_DIR"

test -x "$ROOT_DIR/scripts/install-user.sh"
test -x "$ROOT_DIR/scripts/uninstall-user.sh"
test -x "$ROOT_DIR/scripts/dev-run.sh"

HOME="$TMP_HOME" "$ROOT_DIR/scripts/install-user.sh" --dry-run
HOME="$TMP_HOME" "$ROOT_DIR/scripts/install-user.sh" --validate-only
HOME="$TMP_HOME" "$ROOT_DIR/scripts/uninstall-user.sh" --dry-run

if command -v desktop-file-validate >/dev/null; then
  desktop-file-validate "$ROOT_DIR/data/com.azwerks.NvimShell.desktop"
else
  echo "desktop-file-validate not found; skipping desktop validation"
fi

test -s "$ROOT_DIR/data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg"
command grep -q "<svg" "$ROOT_DIR/data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg"

command grep -q 'PYTHONPATH="$APP_SRC" exec python3 -m azwerks_nvim_shell.main "$@"' "$ROOT_DIR/scripts/install-user.sh"

if command grep -Eq '(^|[^[:alnum:]_])sudo([^[:alnum:]_]|$)' "$ROOT_DIR/scripts/install-user.sh" "$ROOT_DIR/scripts/uninstall-user.sh"; then
  echo "error: install/uninstall scripts must not use sudo" >&2
  exit 1
fi

if command grep -Eq '(^|[[:space:]])(cp|mv|mkdir|rm|install)([[:space:]].*)?/usr' "$ROOT_DIR/scripts/install-user.sh" "$ROOT_DIR/scripts/uninstall-user.sh"; then
  echo "error: install/uninstall scripts must not write to /usr" >&2
  exit 1
fi

HOME="$TMP_HOME" "$ROOT_DIR/scripts/install-user.sh"

test -x "$TMP_HOME/.local/bin/azwerks-nvim-shell"
test -f "$TMP_HOME/.local/share/azwerks-nvim-shell/install-manifest.txt"
test -f "$TMP_HOME/.local/share/applications/com.azwerks.NvimShell.desktop"
test -s "$TMP_HOME/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg"

HOME="$TMP_HOME" "$TMP_HOME/.local/bin/azwerks-nvim-shell" --help >/dev/null
HOME="$TMP_HOME" "$TMP_HOME/.local/bin/azwerks-nvim-shell" --version >/dev/null

HOME="$TMP_HOME" "$ROOT_DIR/scripts/uninstall-user.sh" --dry-run

echo "Install script tests passed."
