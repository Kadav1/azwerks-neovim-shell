# Runtime Notes

## GTK/VTE Runtime

Valid CLI invocations create a `Gtk.Application`, a `Gtk.ApplicationWindow`, and
a `Vte.Terminal` widget.

The terminal spawns Neovim with the argv produced by the CLI launch contract:

```text
[nvim_binary, *positional_args]
```

The working directory is passed through the locally documented
`Vte.Terminal.spawn_async` `working_directory` argument. The app does not pass
`--cwd` to Neovim.

## Environment

The child process receives a copy of the current process environment with these
terminal color variables set:

```text
TERM=xterm-256color
COLORTERM=truecolor
```

Unrelated environment variables are preserved.

## Visual Defaults

The VTE terminal applies the Radium foreground, background, and cursor colors
through the local VTE color APIs. It also applies:

```text
Monospace 11
```

No glow, scanlines, CRT effect, animation, or decorative terminal chrome is
implemented.

## Spawn Errors

Immediate `spawn_async` failures are printed to stderr and also written into the
terminal widget when possible. The window intentionally remains open so the user
can read the error.

## Process Lifecycle

Child-exit lifecycle handling is implemented through a `Vte.Terminal` subclass
that overrides `do_child_exited(status)`. When the Neovim child exits, the app
logs the decoded status and calls `Gtk.Application.quit()`.

The app does not connect a named `child-exited` signal because local signal
lookup did not provide a stable base-class signal name before subclass
registration. Phase 8 verified that explicit `watch_child(pid)` caused a
duplicate-reaping GLib `waitid` warning on this system, while the subclass
`do_child_exited(status)` path works without explicit `watch_child`.

The implementation calls `spawn_async` using the Python-callable argument layout
verified during manual runtime testing. The callable requires `child_setup_data`
between `child_setup` and `timeout`, even though the short docstring omitted it.
`child_setup_data_destroy` appears in FunctionInfo but is not accepted in the
Python-callable positional form. The local binding rejects `None` for
`cancellable`, so a `Gio.Cancellable()` instance is passed. The spawn callback
is still used for immediate spawn errors and optional debug diagnostics.

## Manual GUI Test

A timeout-bound manual GUI launch was run in an X11 session:

```zsh
timeout 8s scripts/dev-run.sh
```

The process stayed alive until `timeout` terminated it with exit code `124`.
No VTE spawn failure was printed after the final spawn-argument fix. The command
did print GTK theme parser warnings from the active desktop theme.

This confirms startup reached a running GTK/VTE process without a reported spawn
error. It does not independently verify visual rendering contents beyond the
manual launch process behavior.
