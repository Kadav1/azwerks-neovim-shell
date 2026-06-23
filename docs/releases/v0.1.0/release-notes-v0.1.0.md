# azwerks Neovim Shell v0.1.0 - Release Notes

## Summary

azwerks Neovim Shell v0.1.0 is a user-local Linux desktop shell for launching
terminal Neovim inside a GTK/VTE window with AZWERKS desktop identity and
Radium-inspired defaults.

## What This Release Is

This is a GTK/VTE wrapper around terminal Neovim. It creates a GTK application
window, embeds a VTE terminal widget, and launches terminal Neovim through the
validated launch contract.

## What This Release Is Not

This is not a true Neovim GUI frontend.

It does not use `nvim --embed`.

It does not implement the Neovim external UI protocol.

It does not implement distribution packaging.

## Implemented Features

- Deterministic CLI parsing and launch-contract generation.
- GTK application and window startup.
- VTE terminal widget creation.
- Terminal Neovim spawn through local PyGObject/VTE APIs.
- Radium-inspired VTE foreground, background, cursor, and font defaults.
- Child-exit lifecycle behavior through `do_child_exited(status)`.
- Optional runtime diagnostics through `AZWERKS_NVIM_SHELL_DEBUG=1`.
- User-local install and uninstall scripts.
- Desktop entry and original SVG icon.
- Non-GUI smoke tests and install-script tests.

## Verified Behavior

- `--help` and `--version` exit before GTK starts.
- CLI errors exit before GTK starts.
- Valid launch contracts are passed to the GTK/VTE runtime.
- Child exit closes the GTK application cleanly.
- The project desktop file validates with `desktop-file-validate`.
- The installed wrapper supports `--help` and `--version` when user-local install is present.

## Install / Uninstall Support

User-local install is the supported v0.1 install shape.

Install:

```zsh
scripts/install-user.sh
```

Preview install:

```zsh
scripts/install-user.sh --dry-run
```

Validate without installing:

```zsh
scripts/install-user.sh --validate-only
```

Preview uninstall:

```zsh
scripts/uninstall-user.sh --dry-run
```

## Runtime / Lifecycle Behavior

Neovim is spawned as a terminal child process in VTE. The app does not pass
`--cwd` to Neovim; it sets the working directory through the VTE spawn call.

When the child exits, the app logs the decoded child status and quits cleanly.

## Known Limitations

- Full visual `gtk-launch` confirmation remains manual unless separately completed.
- GTK theme parser warnings are external desktop theme CSS warnings.
- Distribution packaging is not implemented.
- User-local install is the supported v0.1 install shape.
- The app is a GTK/VTE terminal wrapper, not a true Neovim GUI frontend.
- No `nvim --embed` support.
- No Neovim external UI protocol support.

## Safety Boundaries

The app does not modify:

```text
~/.config/nvim
~/.local/bin/nvim
~/.local/opt/nvim-linux-x86_64
```

The install and uninstall scripts do not use `sudo` and do not write to system
paths.

## Validation Summary

Release-lock validation runs:

```zsh
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install_scripts.sh
tests/smoke.sh
scripts/install-user.sh --dry-run
scripts/install-user.sh --validate-only
scripts/uninstall-user.sh --dry-run
desktop-file-validate data/com.azwerks.NvimShell.desktop
```

## Next Development Track

The next track should focus on post-v0.1 polish: optional visual `gtk-launch`
confirmation, broader manual GUI QA, and packaging exploration if distribution
packaging becomes a goal.
