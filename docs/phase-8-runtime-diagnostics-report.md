# Phase 8 Runtime Diagnostics Report

## Summary

Phase 8 investigated the GLib `waitid` lifecycle warning, preserved verified
child-exit behavior, added opt-in runtime diagnostics, and documented packaging
readiness.

## Decision Gate

Outcome B was selected. A cleaner local lifecycle path was proven by
`scripts/probe-vte-lifecycle-variants.py`.

## Lifecycle Result

The app now relies on `do_child_exited(status)` without explicitly calling
`watch_child(pid)`. The variant probe showed this still observes child exit and
removes the GLib `waitid` warning from the current app path.

## Diagnostics Result

`AZWERKS_NVIM_SHELL_DEBUG=1` enables runtime diagnostics to stderr. Default
runtime output remains quiet.

## Packaging Result

Packaging readiness checks passed for project metadata, desktop metadata, icon
presence, install script dry-run, install script validate-only mode, uninstall
dry-run, unit tests, and smoke tests.

The user-local install was refreshed from the current project after
non-destructive checks passed. The installed wrapper passed `--help`,
`--version`, desktop validation, icon validation, and a timeout-bound lifecycle
check with a short-lived non-Neovim child.
