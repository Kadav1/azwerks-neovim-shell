# Child Lifecycle Behavior

## Verified API Path

Phase 8 verified this local VTE lifecycle path:

```text
spawn_async callback returns child pid
Vte.Terminal.do_child_exited(status) is invoked without explicit watch_child
```

The app does not connect a `child-exited` signal. Base-class signal lookup
returned `id=0` before subclass registration, and the verified app path uses the
`do_child_exited(status)` virtual method override.

## App Behavior

When the spawned Neovim child exits, AZWERKS Neovim Shell:

1. Receives `do_child_exited(status)` on the lifecycle terminal subclass.
2. Logs the child status to stderr.
3. Decodes normal exit codes when possible.
4. Calls `Gtk.Application.quit()`.

This closes the GTK application instead of leaving a dead VTE window open.

## Manual Verification

The lifecycle path was verified with:

```zsh
python3 scripts/probe-vte-child-lifecycle.py
timeout 8s scripts/dev-run.sh --nvim-bin /bin/sh -lc 'printf "azwerks app lifecycle test\n"; exit 7'
timeout 8s scripts/dev-run.sh --nvim-bin /home/blndsft/.local/bin/nvim -u NONE -n -es -c qa
timeout 8s ~/.local/bin/azwerks-nvim-shell --nvim-bin /home/blndsft/.local/bin/nvim -u NONE -n -es -c qa
```

The Neovim checks use `-u NONE -n -es -c qa` to avoid loading or modifying the
user's Neovim configuration.

## Known Warning

Phase 7 lifecycle checks using explicit `watch_child(pid)` printed a GLib
warning:

```text
waitid(... ) failed: No child processes (10)
```

Phase 8 compared lifecycle variants and found that explicit `watch_child(pid)`
caused the warning, while `do_child_exited(status)` without explicit
`watch_child` still observed child exit and exited successfully. The current app
path uses the cleaner variant.
