# Install / Uninstall Safety

## Scope

The Phase 5 install and uninstall scripts are user-local only. They do not use
elevated permissions and do not write to system paths.

## Install Safety

`scripts/install-user.sh` supports:

```zsh
scripts/install-user.sh --dry-run
scripts/install-user.sh --validate-only
scripts/install-user.sh
```

`--dry-run` prints planned actions and makes no filesystem changes.

`--validate-only` verifies required source files, desktop metadata, icon
metadata, wrapper path safety, and user-local target paths without installing.

Real install writes only app-owned targets:

```text
~/.local/bin/azwerks-nvim-shell
~/.local/share/azwerks-nvim-shell/
~/.local/share/applications/com.azwerks.NvimShell.desktop
~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

The installed wrapper preserves all arguments and runs:

```zsh
PYTHONPATH="$APP_SRC" exec python3 -m azwerks_nvim_shell.main "$@"
```

## Manifest

The install script writes:

```text
~/.local/share/azwerks-nvim-shell/install-manifest.txt
```

The manifest records app-owned install paths and is used by the uninstall script
when present.

## Uninstall Safety

`scripts/uninstall-user.sh` supports:

```zsh
scripts/uninstall-user.sh --dry-run
scripts/uninstall-user.sh
```

The uninstall script removes only exact known app-owned targets. It is safe if
files are already missing.

Phase 6 ran real uninstall after dry-run and manifest inspection, then verified
that app-owned files were removed and Neovim config/binary paths remained
present. Reinstall was then run and validated.

The uninstall script refuses protected paths, including:

```text
/
/home
~/.config
~/.local
~/.local/bin
~/.local/share
~/.config/nvim
~/.local/bin/nvim
~/.local/opt/nvim-linux-x86_64
/usr
/usr/local
/etc
```

## Test Isolation

`tests/test_install_scripts.sh` uses a temporary redirected `HOME` for real
install validation. It does not install into the user's real home directory.

Phase 8 packaging readiness re-ran dry-run install, validate-only install, and
dry-run uninstall checks. These checks do not touch system paths and do not
modify Neovim configuration or binaries.
