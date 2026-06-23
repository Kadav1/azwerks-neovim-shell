# azwerks Neovim Shell v0.1.0 - Repository Decision

## Current State

Phase 12 initializes a local Git repository for this project, creates the
initial v0.1.0 commit, and creates a local annotated `v0.1.0` tag.

The v0.1.0 source archive exists and is verified:

```text
dist/azwerks-nvim-shell-v0.1.0-source.tar.gz
```

Phase 11 did not initialize Git. Phase 12 performs local Git initialization
only.

## Option A - Source-Only Local Release

Keep v0.1.0 as a source-only local release.

Pros:

- lowest process overhead
- no repository setup required
- preserves the current release lock as a simple archive

Tradeoff:

- no commit history for future patches unless Git is initialized later

## Option B - Initialize Git Repository

Initialize Git in this directory, commit the release-locked tree, and tag
`v0.1.0`.

Pros:

- creates version history for future v0.1.1 and v0.2 work
- makes release tags and diffs straightforward
- supports future remote publishing

Tradeoff:

- requires deciding what historical docs and generated files belong in version
  control

## Option C - Move Into Existing Monorepo

Move or import this project into an existing AZWERKS repository if one is the
preferred long-term home.

Pros:

- centralizes AZWERKS projects
- can reuse existing repository conventions

Tradeoff:

- requires migration decisions and may complicate clean source archive history

## Option D - Create Remote Repository Later

Keep the local source archive now and create a remote repository only when
active development resumes.

Pros:

- avoids premature hosting decisions
- still preserves the v0.1.0 archive

Tradeoff:

- postpones collaboration and remote backup

## Recommendation

Conservative recommendation: keep v0.1.0 as a source-only local release unless
future work is expected soon. Initialize Git only if version history for future
changes is wanted.

If Git is initialized, use the release archive and `docs/releases/v0.1.0/`
records as the source of truth for the initial v0.1.0 state.

## Commands Not Run During Phase 11

These commands were not run during Phase 11:

```zsh
git init
git add
git commit
git tag
git push
```

## Phase 12 Local Git Baseline

Phase 12 runs the local-only subset:

```zsh
git init
git commit -m "Release azwerks Neovim Shell v0.1.0"
git tag -a v0.1.0 -m "azwerks Neovim Shell v0.1.0"
```

No remote is created and no push is performed.

## Future Remote Command If Approved Later

```zsh
git push origin main --tags
```
