# Child Lifecycle Research

## Scope

This document records child lifecycle research for AZWERKS Neovim Shell. Phase
7 implemented lifecycle handling. Phase 8 investigated the GLib `waitid`
warning and refined the implementation.

## Phase 7 Lifecycle API Probe

Local API evidence:

```text
# Vte.Terminal lifecycle API probe
spawn_async: True
watch_child: True

# Signal lookup
child-exited: id=0
eof: id=0
contents-changed: id=0

# signal_list_names result
(no signal names returned)

# watch_child doc
gi.FunctionInfo(watch_child, bound=None)
watch_child(self, child_pid:int)
```

Original Phase 7 decision: do not connect invented signal names. Use the
locally verified `spawn_async` callback child PID plus
`Vte.Terminal.watch_child(pid)`, and observe child exit through a
`Vte.Terminal` subclass override of `do_child_exited(status)`.

## Local VTE Signal Probe

Result:

```text
# Vte.Terminal signal names
(no signals returned)

# Vte.Terminal lifecycle-like members
bind_template_child_full
child_focus
do_child_exited
do_set_focus_child
feed_child
feed_child_binary
get_child_visible
get_first_accessible_child
get_first_child
get_focus_child
get_last_child
get_pty
get_template_child
observe_children
pty_new_sync
set_child_visible
set_focus_child
set_pty
snapshot_child
spawn_async
spawn_sync
spawn_with_fds_async
watch_child
watch_closure

# spawn_async doc
gi.FunctionInfo(spawn_async, bound=None)
spawn_async(self, pty_flags:Vte.PtyFlags, working_directory:str=None, argv:list, envv:list=None, spawn_flags:GLib.SpawnFlags, child_setup:GLib.SpawnChildSetupFunc=None, timeout:int, cancellable:Gio.Cancellable=None, callback:Vte.TerminalSpawnAsyncCallback=None, user_data=None)
```

## Project Search

The source currently has spawn setup, spawn callback error reporting, optional
runtime diagnostics, and child-exit handling in `app.py`.

Documentation records the current lifecycle behavior in
`docs/child-lifecycle-behavior.md`. Tests verify spawn argument construction,
immediate spawn error handling, lifecycle helper behavior, and runtime
diagnostic helper behavior without opening a GUI.

## Phase 7 Minimal Runtime Probe

Created:

```text
scripts/probe-vte-child-lifecycle.py
```

The probe opens a minimal GTK/VTE window, spawns:

```text
/bin/sh -lc 'printf "azwerks lifecycle probe\n"; exit 7'
```

Observed result:

```text
spawn callback argc=4
spawn callback arg1=<pid> type=int
watch_child pid=<pid>
child-exited status=1792
lifecycle probe succeeded
```

`1792` decodes to exit code `7`.

The probe also produced a GLib warning:

```text
waitid(... ) failed: No child processes (10)
```

Despite that warning, VTE delivered `do_child_exited(status)` and the probe
exited successfully.

## Interpretation

`GObject.signal_list_names(Vte.Terminal)` returned no signal names locally. The
class exposes lifecycle-like members such as `do_child_exited`, `watch_child`,
and `watch_closure`.

Phase 7 verified the `watch_child` plus `do_child_exited` path with a
short-lived non-Neovim child process. Phase 8 later found a cleaner local path.

## Current App Behavior

The app now:

- extracts the child PID from the VTE `spawn_async` callback
- handles `do_child_exited(status)` in a VTE terminal subclass
- logs the raw status and decoded exit code or signal
- calls `application.quit()` to close the GTK app cleanly

## Phase 8 Warning Investigation

Phase 8 reproduced the original warning with the Phase 7 path:

```text
/usr/lib/python3/dist-packages/gi/overrides/Gio.py:42: Warning: ../../../glib/gmain.c:5802: waitid(pid:<pid>, pidfd=<fd>) failed: No child processes (10). See documentation of g_child_watch_source_new() for possible causes.
```

The lifecycle variant probe compared explicit `watch_child(pid)` against no
explicit watch:

```text
current_watch: child_exited_observed=True waitid_warning=True
no_explicit_watch: child_exited_observed=True waitid_warning=False
```

Decision: keep the `do_child_exited(status)` subclass path and stop explicitly
calling `watch_child(pid)` from the app spawn callback. This preserves verified
child-exit behavior and removes the duplicate-reaping warning from the current
app path.

## Remaining Notes

The app still must not assume `child-exited` or other signal names. GTK theme
parser warnings observed during manual probes are external desktop theme CSS
warnings, not app CSS.
