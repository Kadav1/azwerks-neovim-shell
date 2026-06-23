# Changelog

## 0.1.0

- Created initial project scaffolding.
- Added source package structure.
- Added documentation placeholders.
- Added desktop-entry placeholder.
- Added user-local install/uninstall script placeholders.
- Added smoke-test placeholder.
- Implemented CLI parsing and launch-contract generation.
- Added parser unit tests.
- Updated smoke test to run CLI unit tests.
- Added GTK/VTE application/window skeleton without Neovim spawning.
- Added app skeleton unit tests using local GTK/VTE fakes.
- Added GTK/VTE API probe documentation.
- Verified local GTK/VTE import and method availability.
- Implemented GTK/VTE runtime spawn integration for terminal Neovim.
- Added runtime notes for environment handling, visual defaults, spawn errors, and lifecycle limits.
- Implemented user-local desktop install/uninstall scripts.
- Added install/uninstall safety documentation and script tests.
- Cleaned desktop categories to remove desktop-file-validator hints.
- Verified real user-local uninstall and reinstall.
- Added launcher verification and child lifecycle research documentation.
- Implemented VTE child lifecycle handling using the locally verified `watch_child` path.
- Added lifecycle probe script and lifecycle contract unit tests.
- Investigated the GLib `waitid` lifecycle warning with a lifecycle variant probe.
- Switched child lifecycle handling to the verified `do_child_exited` path without duplicate explicit `watch_child` use.
- Added opt-in runtime diagnostics through `AZWERKS_NVIM_SHELL_DEBUG=1`.
- Added runtime diagnostics and packaging readiness documentation.
- Added v0.1.0 release notes, checklist, known limitations, install/uninstall summary, file manifest, and archive manifest.
- Removed generated Python cache files before release archive preparation.
- Prepared a manifest-based v0.1.0 source archive.
- Added v0.1.0 archive handoff, checksum record, repository decision note, and post-release options.
- Initialized local Git repository baseline and local annotated `v0.1.0` tag.
- Published `main` and the existing `v0.1.0` tag to the GitHub remote.
- Prepared GitHub Release draft for v0.1.0 with the clean source archive attached.
