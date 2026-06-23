# azwerks Neovim Shell v0.1.0 - Archive Handoff

## Summary

This document hands off the v0.1.0 release-locked source archive for azwerks
Neovim Shell.

## Release Status

- Phase 9 verdict: `PASS WITH MINOR FINDINGS`.
- Phase 10 verdict: `PASS`.
- v0.1.0 is release-locked as a user-local release candidate.

## Archive Path

```text
dist/azwerks-nvim-shell-v0.1.0-source.tar.gz
```

## Archive Checksum

SHA-256:

```text
bd7db5be0430dcfbc3c0ecaed65e8ca99bf918f0bd6a94293f8814d55f200a55
```

Checksum file:

```text
docs/releases/v0.1.0/checksums-v0.1.0.txt
```

## Contents Summary

The archive contains:

- project metadata and documentation
- Python source package
- GTK/VTE runtime code
- CLI parser and launch-contract code
- user-local install/uninstall scripts
- desktop entry and SVG icon
- unit tests and smoke tests
- v0.1.0 release records

## Excluded Content

The archive excludes:

```text
.git/
dist/
__pycache__/
*.pyc
*.pyo
docs/ChatGPT-Neovim_Audit_and_Handoff.md
docs/implementation-handoff/
```

Historical handoff docs remain in the working tree but are not release-clean
archive content.

## Install Shape

User-local install is the supported v0.1 install shape.

Expected installed targets:

```text
~/.local/bin/azwerks-nvim-shell
~/.local/share/azwerks-nvim-shell/
~/.local/share/applications/com.azwerks.NvimShell.desktop
~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

## Runtime Scope

This is a GTK/VTE wrapper around terminal Neovim.

This is not a true Neovim GUI frontend.

This does not use `nvim --embed`.

This does not implement the Neovim external UI protocol.

## Known Limitations

- Full visual `gtk-launch` confirmation remains manual.
- GTK theme parser warnings are external desktop theme CSS warnings.
- Distribution packaging is not implemented.
- User-local install is the supported v0.1 install shape.

## Validation Commands Passed

```zsh
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install_scripts.sh
tests/smoke.sh
scripts/install-user.sh --dry-run
scripts/install-user.sh --validate-only
scripts/uninstall-user.sh --dry-run
desktop-file-validate data/com.azwerks.NvimShell.desktop
sha256sum -c docs/releases/v0.1.0/checksums-v0.1.0.txt
```

## What This Archive Is Not

This is a source-only local release archive.

This is not a deb/rpm/AppImage/Flatpak package.

This is not distribution packaging.

## Obsidian Mirror Plan

Recommended mirror target, not created automatically:

```text
/home/blndsft/Documents/AZWERKS/20_Products/azwerks-nvim-shell/releases/v0.1.0/
```

Suggested files to mirror if approved:

```text
dist/azwerks-nvim-shell-v0.1.0-source.tar.gz
docs/releases/v0.1.0/
```

## Recommended Next Owner Action

Choose one maintenance path:

- keep this as a source-only local release
- use the local Git v0.1.0 baseline created in Phase 12 for future patches
- start packaging research as a separate track
- mirror the archive and release records to long-term storage

Phase 12 creates a local Git repository, initial release commit, and annotated
`v0.1.0` tag. It does not create a remote and does not push.
