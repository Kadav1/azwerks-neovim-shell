# Launcher Verification

## Scope

This document records Phase 6 launcher and installed-wrapper verification for
AZWERKS Neovim Shell.

## Installed Wrapper

The installed wrapper exists and is executable:

```text
~/.local/bin/azwerks-nvim-shell
```

Verified commands:

```zsh
~/.local/bin/azwerks-nvim-shell --help
~/.local/bin/azwerks-nvim-shell --version
command -v azwerks-nvim-shell || true
```

Results:

```text
--help: exited 0 and printed usage
--version: exited 0 and printed AZWERKS Neovim Shell 0.1.0
PATH: /home/blndsft/.local/bin/azwerks-nvim-shell
```

## Desktop Entry

The desktop category list was changed from:

```ini
Categories=Utility;TextEditor;Development;
```

to:

```ini
Categories=Utility;TextEditor;
```

This keeps the app discoverable as a utility/text editor and removes the
desktop-file-validator hint about multiple main categories.

Verified:

```zsh
desktop-file-validate data/com.azwerks.NvimShell.desktop
desktop-file-validate ~/.local/share/applications/com.azwerks.NvimShell.desktop
```

Both commands exited successfully with no output after reinstall.

## Icon

Verified project and installed icons are non-empty SVG files containing `<svg`.

## gtk-launch

A graphical session was available:

```text
DISPLAY=:0
WAYLAND_DISPLAY=
```

The launcher command was run:

```zsh
gtk-launch com.azwerks.NvimShell
```

Result:

```text
exit code 0
no stdout/stderr output
```

A follow-up external process check did not observe a persistent
`azwerks_nvim_shell`/`azwerks-nvim-shell` process. Visual confirmation of the
window, title, icon, and embedded Neovim was not available from this API session.

Interpretation: the desktop entry can be resolved by `gtk-launch`, but full
visual launcher success remains a manual desktop check.

## External GTK Theme Warnings

No new app-specific CSS was added. Previously observed GTK theme parser warnings
are treated as external desktop theme warnings, not app CSS issues.
