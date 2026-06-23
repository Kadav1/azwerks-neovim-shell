# azwerks Neovim Shell v0.1.0 - Release Checklist

## Core App

- [x] Project version is `0.1.0`.
- [x] Core source files are present.
- [x] Runtime behavior was not changed during release lock.

## CLI

- [x] `--help` exits before GTK.
- [x] `--version` exits before GTK.
- [x] CLI parser unit tests pass.

## GTK/VTE Runtime

- [x] GTK/VTE imports are covered by non-GUI smoke tests.
- [x] VTE spawn behavior is documented.
- [x] No `nvim --embed` behavior is implemented.
- [x] No Neovim external UI protocol behavior is implemented.

## Child Lifecycle

- [x] Child lifecycle behavior is documented.
- [x] Phase 8 verified `do_child_exited(status)` without explicit `watch_child(pid)`.
- [x] Lifecycle helper tests pass.

## Desktop Integration

- [x] Project desktop file validates.
- [x] Installed desktop file validates when installed.
- [x] Icon file exists and contains `<svg`.
- [x] Installed wrapper `--help` works when installed.
- [x] Installed wrapper `--version` works when installed.

## Install / Uninstall Safety

- [x] Install dry-run passes.
- [x] Install validate-only passes.
- [x] Uninstall dry-run passes.
- [x] Known Neovim paths are protected.
- [x] No system paths are written by install/uninstall scripts.

## Documentation

- [x] Release notes exist.
- [x] Known limitations record exists.
- [x] Install/uninstall summary exists.
- [x] Release-lock report exists.

## Release Hygiene

- [x] `__pycache__` files removed.
- [x] `*.pyc` and `*.pyo` files removed.
- [x] Archive excludes historical handoff docs.
- [x] Archive excludes generated/cache paths.

## Tests

- [x] Python compile passes.
- [x] Unit tests pass.
- [x] Install script tests pass.
- [x] Smoke test passes.
- [x] Desktop validation passes.

## Known Limitations

- [x] Manual `gtk-launch` visual confirmation is skipped, not claimed as complete.
- [x] Distribution packaging is documented as not implemented.
- [x] External GTK theme parser warnings are documented as external.

## Release Decision

- [x] Phase 9 verdict recorded as `PASS WITH MINOR FINDINGS`.
- [x] v0.1.0 is ready as a user-local release candidate after release archive preparation.
