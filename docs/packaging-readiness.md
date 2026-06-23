# Packaging Readiness

## Scope

This document records Phase 8 packaging readiness checks for AZWERKS Neovim
Shell v0.1.

## Project Structure

The project keeps source under:

```text
src/azwerks_nvim_shell/
```

Desktop metadata and icons live under:

```text
data/
```

User-local install and uninstall scripts live under:

```text
scripts/
```

## Python Metadata

`pyproject.toml` defines:

```toml
[project]
name = "azwerks-nvim-shell"
version = "0.1.0"
requires-python = ">=3.10"

[project.scripts]
azwerks-nvim-shell = "azwerks_nvim_shell.main:main"
```

GTK/VTE dependencies are intentionally documented as system dependencies, not
pip dependencies.

## Desktop File

The project desktop file validates with:

```zsh
desktop-file-validate data/com.azwerks.NvimShell.desktop
```

The desktop entry uses:

```ini
Exec=azwerks-nvim-shell %F
Icon=com.azwerks.NvimShell
Terminal=false
Categories=Utility;TextEditor;
```

## Icon

The project icon exists at:

```text
data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

Readiness checks verify that the file is non-empty and contains `<svg`.

## Install / Uninstall Scripts

Readiness checks include:

```zsh
scripts/install-user.sh --dry-run
scripts/install-user.sh --validate-only
scripts/uninstall-user.sh --dry-run
```

The scripts remain user-local, avoid `sudo`, and do not write to system paths.

## Wrapper Behavior

The installed wrapper is expected at:

```text
~/.local/bin/azwerks-nvim-shell
```

It sets `PYTHONPATH` to the installed app source path and executes:

```zsh
python3 -m azwerks_nvim_shell.main "$@"
```

Phase 8 refreshed the user-local install from the current project after
non-destructive checks passed. The installed wrapper passed `--help` and
`--version`.

## Automated Readiness Checks

Phase 8 readiness validation includes Python compilation, unit tests, install
script tests, smoke tests, dry-run install, validate-only install, dry-run
uninstall, desktop validation, and icon validation.

Automated checks do not open a GUI and do not spawn Neovim.

## Manual GUI Status

Manual timeout-bound GTK/VTE lifecycle checks were run with a short-lived
non-Neovim child through both `scripts/dev-run.sh` and the refreshed installed
wrapper. Full visual `gtk-launch` confirmation remains a manual desktop check.

## Known Limitations

- GTK/VTE and a display server are required for runtime GUI use.
- GTK theme parser warnings are external desktop theme CSS warnings.
- User-local install is implemented; distribution packaging is not implemented.
- Full visual `gtk-launch` confirmation remains pending.
