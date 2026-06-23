# AZWERKS Neovim Shell

## Purpose

AZWERKS Neovim Shell provides a native Linux desktop shell for launching terminal Neovim with AZWERKS desktop identity and Radium-inspired defaults.

## What This Is

AZWERKS Neovim Shell is a GTK/VTE wrapper around terminal Neovim.

It runs Neovim inside a VTE terminal widget while presenting a dedicated desktop application identity.

## What This Is Not

It is not a true Neovim GUI frontend.

It does not use nvim --embed.

It does not implement the Neovim UI protocol.

It does not modify the user's Neovim config.

## Target Platform

The initial target platform is Linux Mint / Ubuntu-style desktop Linux with GTK and VTE introspection packages available from the system package manager.

## Expected Neovim Path

The default expected Neovim path is:

```text
/home/blndsft/.local/bin/nvim
```

This scaffold does not validate or modify that binary.

## Dependencies

GTK/VTE dependencies are expected to be system packages, not pip packages. See [docs/dependency-notes.md](docs/dependency-notes.md).

Local GTK/VTE introspection findings are recorded in [docs/gtk-vte-api-probe.md](docs/gtk-vte-api-probe.md).

Runtime behavior notes are recorded in [docs/runtime-notes.md](docs/runtime-notes.md).

Launcher verification is recorded in [docs/launcher-verification.md](docs/launcher-verification.md).
Child lifecycle research is recorded in [docs/child-lifecycle-research.md](docs/child-lifecycle-research.md).
Child lifecycle behavior is recorded in [docs/child-lifecycle-behavior.md](docs/child-lifecycle-behavior.md).
Runtime diagnostics are recorded in [docs/runtime-diagnostics.md](docs/runtime-diagnostics.md).
Packaging readiness is recorded in [docs/packaging-readiness.md](docs/packaging-readiness.md).
The v0.1.0 release lock is recorded in [docs/releases/v0.1.0/release-lock-report-v0.1.0.md](docs/releases/v0.1.0/release-lock-report-v0.1.0.md).

## Development Run

```zsh
scripts/dev-run.sh
```

At this stage, the command validates CLI arguments, opens a GTK/VTE window when
GTK/VTE dependencies and a display server are available, and spawns terminal
Neovim through VTE.

## CLI Contract

The current implementation validates arguments and produces a launch contract.
Valid launch contracts are handed to the GTK/VTE runtime.

The VTE terminal uses the launch contract argv and cwd directly. It does not
re-parse CLI arguments.

## User Install

```zsh
scripts/install-user.sh
```

The install script installs only user-local app-owned files:

```text
~/.local/bin/azwerks-nvim-shell
~/.local/share/azwerks-nvim-shell/
~/.local/share/applications/com.azwerks.NvimShell.desktop
~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

Use `--dry-run` to preview changes and `--validate-only` to verify source files,
desktop metadata, icon metadata, and target safety without installing.

## User Uninstall

```zsh
scripts/uninstall-user.sh
```

The uninstall script removes only known app-owned user-local files. Use
`--dry-run` to preview removal. It explicitly refuses protected Neovim and
system paths.

## Known Limitations

- GTK/VTE dependency and display availability are required for the runtime window.
- Child-exit lifecycle handling is implemented through the locally verified VTE `do_child_exited` subclass path.
- GTK theme warnings are external theme CSS warnings, not app CSS.
- Desktop integration is user-local only and does not touch system paths.
- Full visual confirmation of `gtk-launch` remains a manual desktop check.
- The Phase 8 lifecycle variant probe removed the GLib `waitid` warning from the current app path by avoiding duplicate explicit `watch_child` use.

## Runtime Diagnostics

Set `AZWERKS_NVIM_SHELL_DEBUG=1` to print opt-in runtime diagnostics to stderr.
Diagnostics include the resolved Neovim binary, working directory, final argv,
spawn callback PID, and child-exit status. The app does not log the full child
environment.

## Release

The v0.1.0 release records live under:

```text
docs/releases/v0.1.0/
```

The clean source archive is:

```text
dist/azwerks-nvim-shell-v0.1.0-source.tar.gz
```

## Project Status

Version 0.1.0 currently includes scaffolding, CLI launch-contract parsing,
GTK/VTE Neovim spawn integration, child-exit lifecycle handling, opt-in runtime
diagnostics, and user-local desktop integration scripts.

A timeout-bound local GUI launch reached a running GTK/VTE process without a
reported spawn error. See [docs/runtime-notes.md](docs/runtime-notes.md).
