# azwerks Neovim Shell v0.1.0

## Summary

azwerks Neovim Shell v0.1.0 is a source-only user-local Linux release for
launching terminal Neovim inside a GTK/VTE window with AZWERKS desktop identity
and Radium-inspired defaults.

## What This Is

This is a GTK/VTE wrapper around terminal Neovim.

It creates a GTK application window, embeds a VTE terminal widget, and launches
terminal Neovim through the validated launch contract.

## Install Shape

User-local install is the supported v0.1 install shape.

Install:

```zsh
scripts/install-user.sh
```

Preview install:

```zsh
scripts/install-user.sh --dry-run
```

Validate without installing:

```zsh
scripts/install-user.sh --validate-only
```

Preview uninstall:

```zsh
scripts/uninstall-user.sh --dry-run
```

## Included Asset

The attached source archive is the clean release archive:

```text
azwerks-nvim-shell-v0.1.0-source.tar.gz
```

This is not a deb/rpm/AppImage/Flatpak package.

## Verification

SHA-256:

```text
bd7db5be0430dcfbc3c0ecaed65e8ca99bf918f0bd6a94293f8814d55f200a55
```

Verify locally:

```zsh
sha256sum -c docs/releases/v0.1.0/checksums-v0.1.0.txt
```

Release-lock validation included:

```zsh
python3 -m unittest discover -s tests -p 'test_*.py'
tests/smoke.sh
scripts/install-user.sh --dry-run
scripts/install-user.sh --validate-only
scripts/uninstall-user.sh --dry-run
desktop-file-validate data/com.azwerks.NvimShell.desktop
```

## Known Limitations

- Full visual `gtk-launch` confirmation remains manual.
- GTK theme parser warnings are external desktop theme CSS warnings.
- Distribution packaging is not implemented.
- User-local install is the supported v0.1 install shape.

## Not Included

This is not a true Neovim GUI frontend.

This does not use `nvim --embed`.

This does not implement the Neovim external UI protocol.

This does not include distribution packaging.

No deb/rpm/AppImage/Flatpak package artifacts are attached.

## Safety Notes

The app does not modify:

```text
~/.config/nvim
~/.local/bin/nvim
~/.local/opt/nvim-linux-x86_64
```

The install and uninstall scripts do not use `sudo` and do not write to system
paths.
