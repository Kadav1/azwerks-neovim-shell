# Phase 6 Hardening Report

## Summary

Phase 6 verified installed wrapper behavior, cleaned desktop categories, tested
real uninstall/reinstall, ran launcher command verification, and documented child
lifecycle research.

## Preflight

Passed:

```text
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install_scripts.sh
tests/smoke.sh
```

## Installed Wrapper

The wrapper exists, is executable, and supports `--help` and `--version`.

`command -v azwerks-nvim-shell` resolves to:

```text
/home/blndsft/.local/bin/azwerks-nvim-shell
```

## Desktop Category Cleanup

`Development` was removed from the desktop categories, leaving:

```ini
Categories=Utility;TextEditor;
```

This removed the previous desktop-file-validator hint.

## Real Uninstall / Reinstall

Real uninstall was run after dry-run and manifest inspection. It removed only:

```text
~/.local/bin/azwerks-nvim-shell
~/.local/share/applications/com.azwerks.NvimShell.desktop
~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
~/.local/share/azwerks-nvim-shell
```

Protected Neovim paths remained present:

```text
~/.config/nvim
~/.local/bin/nvim
~/.local/opt/nvim-linux-x86_64
```

Reinstall was run and the installed wrapper, desktop entry, and icon validated.

## gtk-launch

`gtk-launch com.azwerks.NvimShell` exited successfully with code 0. A follow-up
process check did not observe a persistent app process. Visual confirmation was
not available from this API session, so full desktop launcher GUI success remains
a manual check.

## Child Lifecycle

Lifecycle behavior remains pending. Local signal introspection returned no VTE
terminal signal names. Lifecycle-like members exist, but their runtime contract
was not verified.

Supersession note: Phase 7 and Phase 8 later verified and implemented child
lifecycle behavior through `Vte.Terminal.do_child_exited(status)` without
explicit `watch_child(pid)`.
