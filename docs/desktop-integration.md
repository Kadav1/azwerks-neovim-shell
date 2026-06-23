# Desktop Integration

The app installs user-local desktop integration only. It does not use elevated
permissions and does not write to system desktop directories.

## Install Targets

The executable wrapper installs to:

```text
~/.local/bin/azwerks-nvim-shell
```

The installed app source and metadata install to:

```text
~/.local/share/azwerks-nvim-shell/app
```

The install manifest installs to:

```text
~/.local/share/azwerks-nvim-shell/install-manifest.txt
```

The desktop entry installs to:

```text
~/.local/share/applications/com.azwerks.NvimShell.desktop
```

The app icon installs to:

```text
~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

## Desktop Entry

The desktop entry uses:

```ini
Terminal=false
Exec=azwerks-nvim-shell %F
Icon=com.azwerks.NvimShell
```

Current project desktop file:

```text
data/com.azwerks.NvimShell.desktop
```

Phase 6 removed the extra `Development` category to avoid a validator hint about
multiple main categories. The desktop entry now uses:

```ini
Categories=Utility;TextEditor;
```

The project and installed desktop files validate successfully with this category
list.

Phase 8 packaging readiness rechecked the project desktop file with
`desktop-file-validate`. Installed desktop validation is valid when the
user-local install has been refreshed from the current project.

## Install

Preview install:

```zsh
scripts/install-user.sh --dry-run
```

Validate without installing:

```zsh
scripts/install-user.sh --validate-only
```

Install:

```zsh
scripts/install-user.sh
```

## Uninstall

Preview uninstall:

```zsh
scripts/uninstall-user.sh --dry-run
```

Uninstall:

```zsh
scripts/uninstall-user.sh
```

The uninstall script removes only these app-owned targets:

```text
~/.local/bin/azwerks-nvim-shell
~/.local/share/applications/com.azwerks.NvimShell.desktop
~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
~/.local/share/azwerks-nvim-shell/
```

It refuses protected paths, including:

```text
~/.config/nvim
~/.local/bin/nvim
~/.local/opt/nvim-linux-x86_64
/usr
/usr/local
/etc
```
