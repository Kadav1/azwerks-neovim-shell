# Implementation Plan

## Phase 0 — Scaffolding

Create the project structure, package metadata, documentation placeholders, script placeholders, desktop-entry placeholder, icon placeholder, and smoke test.

## Phase 1 — CLI Parsing

Implement locked left-to-right parsing rules, early exit flags, error reporting, cwd resolution, and Neovim argv construction.

## Phase 2 — GTK/VTE Window

Create the GTK application/window structure and embed a VTE terminal widget.

Status: implemented as a spawn-free skeleton. The VTE widget displays a
launch-contract placeholder and does not spawn Neovim yet.

## Phase 3 — GTK/VTE API Probe

Verify local GTK, PyGObject, and VTE introspection before implementing VTE
spawn behavior.

Status: completed. GTK 4.0 import succeeded, VTE 3.91 import succeeded,
`Vte.Terminal` exists, desktop-file validation output was recorded, and
`docs/gtk-vte-api-probe.md` was created.

## Phase 4 — GTK/VTE Spawn Integration

Create the GTK application/window, create the VTE terminal widget, apply basic
Radium visual defaults, and spawn Neovim through the locally documented
`Vte.Terminal.spawn_async` API.

Status: completed in code. Automated tests verify CLI pre-exit behavior,
launch-contract handoff, environment preparation, visual calls, and VTE spawn
arguments without opening a GUI or spawning Neovim.

A timeout-bound local GUI launch reached a running GTK/VTE process without a
reported VTE spawn failure.

## Phase 5 — Desktop Integration

Finalize user-local desktop file, icon installation, executable installation, and desktop database validation notes.

Status: completed for user-local install/uninstall scripts. The install script
creates the wrapper, installed app source directory, desktop entry, icon, and
manifest under the user's home directory. The uninstall script removes only
known app-owned paths and supports dry-run.

## Phase 6 — Radium Visual Defaults

Apply planned Radium-inspired terminal colors through GTK/VTE APIs after dependency behavior is verified.

Status: basic VTE foreground, background, cursor, and font defaults are applied.

## Phase 7 — Smoke Tests

Add practical smoke tests for CLI behavior, desktop metadata, Python compilation, and script permissions.

Current smoke tests compile the source, run unit tests, validate desktop
metadata when `desktop-file-validate` is available, and check script
permissions. They do not launch a GUI.

## Phase 8 — Hardening

Improve path validation, process errors, environment handling, packaging metadata, and user-facing diagnostics.

Status: Phase 8 runtime diagnostics and packaging readiness completed. The
GLib `waitid` lifecycle warning was investigated with a variant probe, opt-in
runtime diagnostics were added, packaging readiness checks were documented, and
automated tests remain non-GUI.

## Phase 9 — Child Lifecycle

Validate local VTE child lifecycle behavior and close the GTK app cleanly when
the spawned Neovim child exits.

Status: completed and hardened. Phase 7 verified child-exit handling. Phase 8
proved that explicit `watch_child(pid)` caused a duplicate-reaping GLib
`waitid` warning on this system, while the `do_child_exited(status)` subclass
path works without explicit `watch_child`. The app now quits cleanly on child
exit without that warning in the current runtime path.

## Phase 10 — Release Lock

Prepare v0.1.0 release records, clean generated Python cache files, exclude
historical handoff docs from the release archive, and create a manifest-based
source archive.

Status: completed. Release records live under `docs/releases/v0.1.0/`, and the
clean source archive is `dist/azwerks-nvim-shell-v0.1.0-source.tar.gz`.

## Phase 11 — Archive Handoff

Create final archive handoff, checksum record, repository decision note, and
post-release options without changing runtime behavior.

Status: completed. Handoff records live under `docs/releases/v0.1.0/`.

## Phase 12 — Local Git Baseline

Initialize a local Git repository, commit the release-locked v0.1.0 state, and
create a local annotated `v0.1.0` tag without creating a remote or pushing.

Status: completed locally. The initial commit records the release-locked
project tree, and `v0.1.0` is a local annotated tag.
