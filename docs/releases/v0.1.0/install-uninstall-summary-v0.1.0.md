# azwerks Neovim Shell v0.1.0 - Install / Uninstall Summary

## Scripts

Install script:

```text
scripts/install-user.sh
```

Uninstall script:

```text
scripts/uninstall-user.sh
```

## Dry Run

Install dry-run:

```zsh
scripts/install-user.sh --dry-run
```

Uninstall dry-run:

```zsh
scripts/uninstall-user.sh --dry-run
```

Dry-run mode prints planned actions and makes no filesystem changes.

## Validate Only

Install validation:

```zsh
scripts/install-user.sh --validate-only
```

Validate-only mode checks source files, desktop metadata, icon metadata, wrapper
paths, and user-local target safety without installing files.

## User-Local Targets

Installed wrapper path:

```text
~/.local/bin/azwerks-nvim-shell
```

Installed app data path:

```text
~/.local/share/azwerks-nvim-shell/
```

Installed desktop entry path:

```text
~/.local/share/applications/com.azwerks.NvimShell.desktop
```

Installed icon path:

```text
~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

## Protected Neovim Paths

The uninstall script explicitly protects:

```text
~/.config/nvim
~/.local/bin/nvim
~/.local/opt/nvim-linux-x86_64
```

## Real Uninstall Status

Phase 6 ran a real uninstall after dry-run and ownership checks, then reinstalled
and validated the user-local app. Phase 10 does not run real uninstall.
