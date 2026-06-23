# GLib waitid Warning Investigation

## Scope

Phase 8 investigated this warning observed during lifecycle checks:

```text
waitid(... ) failed: No child processes (10)
```

The goal was to determine whether the warning indicated broken lifecycle
behavior or duplicate child reaping.

## Current Warning Evidence

The Phase 7 lifecycle probe was captured with stdout and stderr split.

Observed stdout:

```text
spawning lifecycle probe child
spawn callback argc=4
spawn callback arg1=<pid> type=int
watch_child pid=<pid>
child-exited status=1792
lifecycle probe succeeded
```

Observed stderr included external GTK theme warnings and this GLib warning:

```text
/usr/lib/python3/dist-packages/gi/overrides/Gio.py:42: Warning: ../../../glib/gmain.c:5802: waitid(pid:<pid>, pidfd=<fd>) failed: No child processes (10). See documentation of g_child_watch_source_new() for possible causes.
```

The child-exit event was observed and the probe exited successfully.

## Implementation Inspection

Project search found:

- `spawn_async` is called in `src/azwerks_nvim_shell/app.py`.
- Phase 7 code called `watch_child(pid)` from the spawn callback.
- `do_child_exited(status)` is implemented in a `Vte.Terminal` subclass.
- No app code calls manual `waitid`, `waitpid`, or GLib child-watch APIs.
- App shutdown calls `Gtk.Application.quit()` from the child-exit handler.

## Local API Recheck

Local introspection reported:

```text
spawn_async
watch_child
do_child_exited
```

Base-class signal lookup before subclass registration returned:

```text
child-exited: 0
eof: 0
contents-changed: 0
```

The local `spawn_async` docstring remained:

```text
spawn_async(self, pty_flags:Vte.PtyFlags, working_directory:str=None, argv:list, envv:list=None, spawn_flags:GLib.SpawnFlags, child_setup:GLib.SpawnChildSetupFunc=None, timeout:int, cancellable:Gio.Cancellable=None, callback:Vte.TerminalSpawnAsyncCallback=None, user_data=None)
```

The local `watch_child` docstring remained:

```text
watch_child(self, child_pid:int)
```

## Lifecycle Variant Probe

Created:

```text
scripts/probe-vte-lifecycle-variants.py
```

The probe compares short-lived non-Neovim child lifecycle variants.

Results:

```text
current_watch:
  child_exited_observed: True
  waitid_warning: True
  traceback: False

no_explicit_watch:
  child_exited_observed: True
  waitid_warning: False
  traceback: False
```

## Decision

Outcome B: a cleaner local path was proven.

The current app now uses `do_child_exited(status)` without explicit
`watch_child(pid)`. The spawn callback still reports immediate spawn errors and
debug diagnostics, but it does not add a duplicate child watcher.

## Manual App Check

Phase 8 ran:

```zsh
timeout 8s scripts/dev-run.sh --nvim-bin /bin/sh -lc 'printf "azwerks phase 8 app lifecycle test\n"; exit 7'
```

Observed result:

```text
AZWERKS Neovim Shell child exited: status=1792 exit_code=7
```

No GLib `waitid` warning appeared in the current app path. External GTK theme
parser warnings still appeared and remain unrelated to app CSS.

The refreshed installed wrapper was also checked with:

```zsh
timeout 8s ~/.local/bin/azwerks-nvim-shell --nvim-bin /bin/sh -lc 'printf "azwerks phase 8 installed lifecycle test\n"; exit 7'
```

It exited successfully with:

```text
AZWERKS Neovim Shell child exited: status=1792 exit_code=7
```

No GLib `waitid` warning appeared in the installed-wrapper app path.
