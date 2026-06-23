#!/usr/bin/env zsh
set -euo pipefail

DRY_RUN=0
VALIDATE_ONLY=0

for arg in "$@"; do
  case "$arg" in
    --dry-run)
      DRY_RUN=1
      ;;
    --validate-only)
      VALIDATE_ONLY=1
      ;;
    *)
      print -u2 "error: unknown option '$arg'"
      exit 2
      ;;
  esac
done

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

APP_ROOT="$HOME/.local/share/azwerks-nvim-shell"
APP_DIR="$APP_ROOT/app"
APP_SRC="$APP_DIR/src"
BIN_TARGET="$HOME/.local/bin/azwerks-nvim-shell"
DESKTOP_TARGET="$HOME/.local/share/applications/com.azwerks.NvimShell.desktop"
ICON_TARGET="$HOME/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg"
MANIFEST_TARGET="$APP_ROOT/install-manifest.txt"

DESKTOP_SOURCE="$ROOT_DIR/data/com.azwerks.NvimShell.desktop"
ICON_SOURCE="$ROOT_DIR/data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg"

run() {
  print -- "$*"
  if (( DRY_RUN == 0 && VALIDATE_ONLY == 0 )); then
    "$@"
  fi
}

require_source() {
  local path="$1"
  if [[ ! -e "$path" ]]; then
    print -u2 "error: required source missing: $path"
    exit 1
  fi
}

require_user_local_target() {
  local path="$1"
  case "$path" in
    "$HOME/.local/bin/azwerks-nvim-shell"|"$HOME/.local/share/azwerks-nvim-shell"|"$HOME/.local/share/azwerks-nvim-shell/"*|"$HOME/.local/share/applications/com.azwerks.NvimShell.desktop"|"$HOME/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg")
      ;;
    *)
      print -u2 "error: refusing unsafe install target: $path"
      exit 1
      ;;
  esac
}

validate_inputs() {
  require_source "$ROOT_DIR/src/azwerks_nvim_shell/main.py"
  require_source "$ROOT_DIR/src/azwerks_nvim_shell/app.py"
  require_source "$ROOT_DIR/src/azwerks_nvim_shell/cli.py"
  require_source "$ROOT_DIR/src/azwerks_nvim_shell/config.py"
  require_source "$ROOT_DIR/src/azwerks_nvim_shell/radium.py"
  require_source "$ROOT_DIR/pyproject.toml"
  require_source "$ROOT_DIR/README.md"
  require_source "$ROOT_DIR/CHANGELOG.md"
  require_source "$DESKTOP_SOURCE"
  require_source "$ICON_SOURCE"

  require_user_local_target "$APP_ROOT"
  require_user_local_target "$APP_DIR"
  require_user_local_target "$APP_SRC"
  require_user_local_target "$BIN_TARGET"
  require_user_local_target "$DESKTOP_TARGET"
  require_user_local_target "$ICON_TARGET"
  require_user_local_target "$MANIFEST_TARGET"

  if command -v desktop-file-validate >/dev/null; then
    desktop-file-validate "$DESKTOP_SOURCE"
  else
    print "desktop-file-validate not found; skipping desktop validation"
  fi

  test -s "$ICON_SOURCE"
  command grep -q "<svg" "$ICON_SOURCE"
}

write_wrapper() {
  local target="$1"
  {
    print '#!/usr/bin/env zsh'
    print 'set -euo pipefail'
    print ''
    print 'APP_SRC="$HOME/.local/share/azwerks-nvim-shell/app/src"'
    print 'PYTHONPATH="$APP_SRC" exec python3 -m azwerks_nvim_shell.main "$@"'
  } > "$target"
}

write_manifest() {
  local tmp_manifest="$MANIFEST_TARGET.tmp"
  {
    print "$APP_ROOT"
    print "$APP_DIR"
    print "$APP_SRC"
    find "$APP_DIR" -type f | sort
    print "$BIN_TARGET"
    print "$DESKTOP_TARGET"
    print "$ICON_TARGET"
    print "$MANIFEST_TARGET"
  } > "$tmp_manifest"
  mv "$tmp_manifest" "$MANIFEST_TARGET"
}

refresh_desktop_caches() {
  if command -v update-desktop-database >/dev/null; then
    if (( DRY_RUN == 1 || VALIDATE_ONLY == 1 )); then
      run update-desktop-database "$HOME/.local/share/applications"
    elif ! update-desktop-database "$HOME/.local/share/applications"; then
      print "warning: update-desktop-database failed; continuing"
    fi
  else
    print "update-desktop-database not found; skipping desktop database refresh"
  fi

  if command -v gtk-update-icon-cache >/dev/null; then
    if (( DRY_RUN == 1 || VALIDATE_ONLY == 1 )); then
      run gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor"
    elif ! gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor"; then
      print "warning: gtk-update-icon-cache failed; continuing"
    fi
  else
    print "gtk-update-icon-cache not found; skipping icon cache refresh"
  fi
}

print "AZWERKS Neovim Shell user-local install"
print "Project root: $ROOT_DIR"
print "App target: $APP_DIR"
print "Wrapper target: $BIN_TARGET"
print "Desktop target: $DESKTOP_TARGET"
print "Icon target: $ICON_TARGET"

validate_inputs

if (( VALIDATE_ONLY == 1 )); then
  print "Validation passed. No files installed."
  exit 0
fi

if (( DRY_RUN == 1 )); then
  print "Dry run: would create user-local directories"
  print "Dry run: would copy source and metadata to $APP_DIR"
  print "Dry run: would install desktop file to $DESKTOP_TARGET"
  print "Dry run: would install icon to $ICON_TARGET"
  print "Dry run: would create wrapper at $BIN_TARGET"
  print "Dry run: would write manifest to $MANIFEST_TARGET"
  print "Dry run complete. No files installed."
  exit 0
fi

mkdir -p "$HOME/.local/bin"
mkdir -p "$APP_DIR"
mkdir -p "$HOME/.local/share/applications"
mkdir -p "$HOME/.local/share/icons/hicolor/scalable/apps"

rm -rf "$APP_SRC"
mkdir -p "$APP_SRC"
cp -R "$ROOT_DIR/src/." "$APP_SRC/"
find "$APP_SRC" -type d -name "__pycache__" -prune -exec rm -rf {} +
find "$APP_SRC" -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete
cp "$ROOT_DIR/pyproject.toml" "$APP_DIR/pyproject.toml"
cp "$ROOT_DIR/README.md" "$APP_DIR/README.md"
cp "$ROOT_DIR/CHANGELOG.md" "$APP_DIR/CHANGELOG.md"
cp "$DESKTOP_SOURCE" "$DESKTOP_TARGET"
cp "$ICON_SOURCE" "$ICON_TARGET"
write_wrapper "$BIN_TARGET"
chmod +x "$BIN_TARGET"
write_manifest

if command -v desktop-file-validate >/dev/null; then
  desktop-file-validate "$DESKTOP_TARGET"
fi

refresh_desktop_caches

print "Install complete."
print "Run: $BIN_TARGET --help"
