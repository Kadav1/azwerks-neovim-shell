# azwerks Neovim Shell v0.1.0 - Release Lock Report

## Phase 9 Verdict

Phase 9 verdict: `PASS WITH MINOR FINDINGS`.

Accepted findings:

- F-01 - Generated Python cache files are present.
- F-02 - Historical handoff documentation is not release-clean.
- F-03 - Stale lifecycle docs were corrected during audit.
- F-04 - Manual `gtk-launch` visual confirmation was skipped.

Release lock target: v0.1.0 user-local release candidate.

## Release Lock Actions

- Removed generated Python cache files.
- Created release notes, checklist, known limitations, install/uninstall summary,
  file manifest, archive exclusion list, archive manifest, and release-lock report.
- Excluded historical handoff and implementation prompt docs from the release archive.
- Prepared a manifest-based source archive in `dist/`.

## Source Archive

Created archive:

```text
dist/azwerks-nvim-shell-v0.1.0-source.tar.gz
```

Archive contents are defined by:

```text
docs/releases/v0.1.0/archive-manifest-v0.1.0.txt
```

The archive excludes `.git`, `dist`, generated Python cache files, the unrelated
ChatGPT handoff document, and the implementation handoff prompt tree.

## Historical Handoff Docs Decision

The working tree keeps historical handoff and implementation prompt documents for
project continuity. They are excluded from the v0.1.0 source archive because
they contain historical prompts, unrelated Neovim/Black Box context, sudo/package
manager examples, and implementation-process material that is not release
documentation.

Excluded historical documentation:

```text
./docs/ChatGPT-Neovim_Audit_and_Handoff.md
./docs/implementation-handoff
```

## Manual gtk-launch Status

Manual visual `gtk-launch` confirmation remains skipped. This release lock does
not claim full visual launcher confirmation.

## Git Tag Recommendation

Suggested tag command, not run:

```zsh
git tag -a v0.1.0 -m "azwerks Neovim Shell v0.1.0"
```

Suggested push command, not run:

```zsh
git push origin v0.1.0
```
