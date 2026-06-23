#!/usr/bin/env zsh
set -euo pipefail

DRY_RUN=0

for arg in "$@"; do
  case "$arg" in
    --dry-run)
      DRY_RUN=1
      ;;
    *)
      print -u2 "error: unknown option '$arg'"
      exit 2
      ;;
  esac
done

APP_ROOT="$HOME/.local/share/azwerks-nvim-shell"
BIN_TARGET="$HOME/.local/bin/azwerks-nvim-shell"
DESKTOP_TARGET="$HOME/.local/share/applications/com.azwerks.NvimShell.desktop"
ICON_TARGET="$HOME/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg"
MANIFEST_TARGET="$APP_ROOT/install-manifest.txt"

PROTECTED_PATHS=(
  "/"
  "/usr"
  "/usr/local"
  "/etc"
  "/home"
  "$HOME"
  "$HOME/.config"
  "$HOME/.local"
  "$HOME/.local/bin"
  "$HOME/.local/share"
  "$HOME/.config/nvim"
  "$HOME/.local/bin/nvim"
  "$HOME/.local/opt/nvim-linux-x86_64"
)

is_protected_path() {
  local path="$1"
  local protected
  for protected in "${PROTECTED_PATHS[@]}"; do
    if [[ "$path" == "$protected" ]]; then
      return 0
    fi
  done
  return 1
}

is_app_owned_path() {
  local path="$1"
  case "$path" in
    "$BIN_TARGET"|"$DESKTOP_TARGET"|"$ICON_TARGET"|"$APP_ROOT"|"$APP_ROOT/"*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

remove_path() {
  local path="$1"

  if is_protected_path "$path"; then
    print -u2 "error: refusing protected path: $path"
    exit 1
  fi

  if ! is_app_owned_path "$path"; then
    print -u2 "error: refusing non-app-owned path: $path"
    exit 1
  fi

  if [[ ! -e "$path" && ! -L "$path" ]]; then
    print "Already absent: $path"
    return
  fi

  if (( DRY_RUN == 1 )); then
    print "Dry run: would remove $path"
    return
  fi

  if [[ -d "$path" && ! -L "$path" ]]; then
    /usr/bin/rm -rf "$path"
  else
    /usr/bin/rm -f "$path"
  fi
  print "Removed: $path"
}

refresh_desktop_caches() {
  if (( DRY_RUN == 1 )); then
    print "Dry run: would refresh desktop/icon caches if tools are available"
    return
  fi

  if command -v update-desktop-database >/dev/null; then
    if ! update-desktop-database "$HOME/.local/share/applications"; then
      print "warning: update-desktop-database failed; continuing"
    fi
  else
    print "update-desktop-database not found; skipping desktop database refresh"
  fi

  if command -v gtk-update-icon-cache >/dev/null; then
    if ! gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor"; then
      print "warning: gtk-update-icon-cache failed; continuing"
    fi
  else
    print "gtk-update-icon-cache not found; skipping icon cache refresh"
  fi
}

print "AZWERKS Neovim Shell user-local uninstall"
print "Protected Neovim paths will not be removed:"
print "  $HOME/.config/nvim"
print "  $HOME/.local/bin/nvim"
print "  $HOME/.local/opt/nvim-linux-x86_64"

if [[ -f "$MANIFEST_TARGET" ]]; then
  print "Using install manifest: $MANIFEST_TARGET"
  manifest_paths=()
  while IFS= read -r path; do
    [[ -n "$path" ]] && manifest_paths+=("$path")
  done < "$MANIFEST_TARGET"

  for path in "${manifest_paths[@]}"; do
    if [[ "$path" == "$APP_ROOT" || "$path" == "$APP_ROOT/"* ]]; then
      continue
    fi
    remove_path "$path"
  done
  remove_path "$APP_ROOT"
else
  print "Manifest not found; removing known app-owned targets."
  remove_path "$BIN_TARGET"
  remove_path "$DESKTOP_TARGET"
  remove_path "$ICON_TARGET"
  remove_path "$APP_ROOT"
fi

refresh_desktop_caches

print "Uninstall complete."
