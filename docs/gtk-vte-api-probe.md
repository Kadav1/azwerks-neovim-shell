# GTK/VTE API Probe — AZWERKS Neovim Shell v0.1

## 1. Scope

This document records the local GTK, PyGObject, VTE, and desktop-entry environment available for AZWERKS Neovim Shell.

The probe was run from:

```text
/media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
```

This phase did not install packages, open a GUI window, spawn VTE, or launch Neovim.

## 2. Phase 2 Preflight Result

Phase 2 preflight passed before GTK/VTE probing.

```text
python3 -m py_compile src/azwerks_nvim_shell/*.py
```

Result: passed.

```text
python3 -m unittest discover -s tests -p 'test_*.py'
```

Result:

```text
..............................
----------------------------------------------------------------------
Ran 30 tests in 0.007s

OK
```

```text
tests/smoke.sh
```

Result:

```text
..............................
----------------------------------------------------------------------
Ran 30 tests in 0.007s

OK
data/com.azwerks.NvimShell.desktop: hint: value "Utility;TextEditor;Development;" for key "Categories" in group "Desktop Entry" contains more than one main category; application might appear more than once in the application menu
CLI smoke test passed.
```

## 3. System Package Check

Command:

```zsh
dpkg-query -W -f='${Package} ${Version}\n' python3-gi gir1.2-gtk-4.0 gir1.2-vte-3.91 desktop-file-utils 2>/dev/null || true
```

Result:

```text
desktop-file-utils 0.27-2build1
gir1.2-gtk-4.0 4.14.5+ds-0ubuntu0.10
gir1.2-vte-3.91 0.76.0-1ubuntu0.1
python3-gi 3.48.2-1
```

Additional command checks:

```text
python3 --version
Python 3.12.3

command -v desktop-file-validate || true
/usr/bin/desktop-file-validate

command -v gtk-launch || true
/usr/bin/gtk-launch

command -v nvim || true
/home/blndsft/.local/bin/nvim

command -v /home/blndsft/.local/bin/nvim || true
/home/blndsft/.local/bin/nvim
```

No required package was missing from the `dpkg-query` result.

## 4. Python / GI Import Check

Command:

```zsh
python3 - <<'PY'
import gi

print("GI import OK")

try:
    gi.require_version("Gtk", "4.0")
    print("Gtk 4.0 requirement OK")
except Exception as exc:
    print("Gtk 4.0 requirement FAILED:", repr(exc))
    raise

try:
    gi.require_version("Vte", "3.91")
    print("Vte 3.91 requirement OK")
except Exception as exc:
    print("Vte 3.91 requirement FAILED:", repr(exc))
    raise

from gi.repository import Gtk, Vte, GLib, Gio, GObject, Pango

print("Gtk.Application:", Gtk.Application)
print("Gtk.ApplicationWindow:", Gtk.ApplicationWindow)
print("Vte.Terminal:", Vte.Terminal)
print("GLib:", GLib)
print("Gio:", Gio)
print("GObject:", GObject)
print("Pango:", Pango)
PY
```

Result:

```text
GI import OK
Gtk 4.0 requirement OK
Vte 3.91 requirement OK
Gtk.Application: <class 'gi.repository.Gtk.Application'>
Gtk.ApplicationWindow: <class 'gi.repository.Gtk.ApplicationWindow'>
Vte.Terminal: <class 'gi.repository.Vte.Terminal'>
GLib: <GLibProxyModule <IntrospectionModule 'GLib' from '/usr/lib/x86_64-linux-gnu/girepository-1.0/GLib-2.0.typelib'>>
Gio: <GioProxyModule <IntrospectionModule 'Gio' from '/usr/lib/x86_64-linux-gnu/girepository-1.0/Gio-2.0.typelib'>>
GObject: <GObjectProxyModule <IntrospectionModule 'GObject' from '/usr/lib/x86_64-linux-gnu/girepository-1.0/GObject-2.0.typelib'>>
Pango: <PangoProxyModule <IntrospectionModule 'Pango' from '/usr/lib/x86_64-linux-gnu/girepository-1.0/Pango-1.0.typelib'>>
```

## 5. GTK API Availability

Command result:

```text
# Gtk method/class availability
Gtk.Application: True
Gtk.ApplicationWindow: True
Gtk.Box: True
Gtk.Orientation: True
Gtk.CssProvider: True
Gtk.StyleContext: True

# Gtk.Application doc

:Constructors:

::

    Application(**properties)
    new(application_id:str=None, flags:Gio.ApplicationFlags) -> Gtk.Application


# Gtk.ApplicationWindow doc

:Constructors:

::

    ApplicationWindow(**properties)
    new(application:Gtk.Application) -> Gtk.Widget
```

## 6. VTE API Availability

Command result:

```text
# Vte.Terminal method availability
spawn_async: True
set_color_foreground: True
set_color_background: True
set_color_cursor: True
set_colors: True
set_font: True
set_font_scale: True
copy_clipboard: True
paste_clipboard: True
get_text: True
```

`Vte.Terminal` exists locally:

```text
Vte.Terminal: <class 'gi.repository.Vte.Terminal'>
```

## 7. VTE Spawn API Notes

Local introspection reports `Vte.Terminal.spawn_async` as available.

Command result:

```text
# Vte.Terminal spawn_async doc
gi.FunctionInfo(spawn_async, bound=None)
spawn_async(self, pty_flags:Vte.PtyFlags, working_directory:str=None, argv:list, envv:list=None, spawn_flags:GLib.SpawnFlags, child_setup:GLib.SpawnChildSetupFunc=None, timeout:int, cancellable:Gio.Cancellable=None, callback:Vte.TerminalSpawnAsyncCallback=None, user_data=None)
```

Implementation should use this local introspection evidence directly. This document does not invent or alter the signature.

## 8. VTE Color / Font API Notes

The local `Vte.Terminal` introspection result confirms these color/font methods exist:

```text
set_color_foreground: True
set_color_background: True
set_color_cursor: True
set_colors: True
set_font: True
set_font_scale: True
```

The next implementation phase may use these methods after verifying expected argument types with local runtime checks.

## 9. VTE Signal Notes

Command result:

```text
# Vte.Terminal signals
```

`GObject.signal_list_names(Vte.Terminal)` returned no printed signal names in this probe. Child-exit or lifecycle signal wiring should not be implemented from assumptions; it needs a follow-up runtime check if signal handling is required.

## 10. Desktop Entry Validation

Command:

```zsh
if command -v desktop-file-validate >/dev/null; then
  desktop-file-validate data/com.azwerks.NvimShell.desktop
else
  echo "desktop-file-validate not found"
fi
```

Result:

```text
data/com.azwerks.NvimShell.desktop: hint: value "Utility;TextEditor;Development;" for key "Categories" in group "Desktop Entry" contains more than one main category; application might appear more than once in the application menu
```

The command exited successfully and reported a non-fatal hint. Desktop integration installation was not tested in this phase.

## 11. Implementation Implications

The next implementation phase may safely rely on:

- PyGObject import support through `python3-gi`.
- GTK 4.0 introspection through `gir1.2-gtk-4.0`.
- VTE 3.91 introspection through `gir1.2-vte-3.91`.
- `Gtk.Application` and `Gtk.ApplicationWindow`.
- `Vte.Terminal`.
- `Vte.Terminal.spawn_async` availability with the locally reported docstring.
- VTE color/font methods listed in this document.

The next phase should still avoid changing Neovim configuration and should set the working directory through the VTE spawn call rather than passing `--cwd` to Neovim.

## 12. Risks / Unknowns

- `GObject.signal_list_names(Vte.Terminal)` printed no signal names in this probe.
- The exact argument object types for VTE color/font methods were not runtime-tested.
- No GUI window was opened, so display-server behavior remains unverified.
- No VTE child process was spawned, so `spawn_async` runtime behavior remains unverified.
- Desktop entry installation and launcher behavior were not tested.

## 13. Phase 4 Focused Follow-Up Probe

Before implementing controlled spawn integration, a focused local introspection
probe was run for `spawn_finish`, VTE feed/color/font methods, and enum names.

Result:

```text
# spawn_async
gi.FunctionInfo(spawn_async, bound=None)
spawn_async(self, pty_flags:Vte.PtyFlags, working_directory:str=None, argv:list, envv:list=None, spawn_flags:GLib.SpawnFlags, child_setup:GLib.SpawnChildSetupFunc=None, timeout:int, cancellable:Gio.Cancellable=None, callback:Vte.TerminalSpawnAsyncCallback=None, user_data=None)
# spawn_finish
None
None
# feed
gi.FunctionInfo(feed, bound=None)
feed(self, data:list=None)
# set_color_foreground
gi.FunctionInfo(set_color_foreground, bound=None)
set_color_foreground(self, foreground:Gdk.RGBA)
# set_color_background
gi.FunctionInfo(set_color_background, bound=None)
set_color_background(self, background:Gdk.RGBA)
# set_color_cursor
gi.FunctionInfo(set_color_cursor, bound=None)
set_color_cursor(self, cursor_background:Gdk.RGBA=None)
# set_font
gi.FunctionInfo(set_font, bound=None)
set_font(self, font_desc:Pango.FontDescription=None)
# Vte.PtyFlags names ['DEFAULT', 'NO_CTTY', 'NO_FALLBACK', 'NO_HELPER', 'NO_LASTLOG', 'NO_SESSION', 'NO_UTMP', 'NO_WTMP']
# GLib.SpawnFlags names ['CHILD_INHERITS_STDERR', 'CHILD_INHERITS_STDIN', 'CHILD_INHERITS_STDOUT', 'CLOEXEC_PIPES', 'DEFAULT', 'DO_NOT_REAP_CHILD', 'FILE_AND_ARGV_ZERO', 'LEAVE_DESCRIPTORS_OPEN', 'SEARCH_PATH', 'SEARCH_PATH_FROM_ENVP', 'STDERR_TO_DEV_NULL', 'STDIN_FROM_DEV_NULL', 'STDOUT_TO_DEV_NULL']
```

Phase 4 therefore uses `Vte.PtyFlags.DEFAULT` and `GLib.SpawnFlags.DEFAULT`.
During manual runtime testing, `spawn_async` rejected keyword arguments and
reported that it requires 12 non-keyword arguments. A direct GI FunctionInfo
argument probe showed these local arguments:

```text
0 pty_flags
1 working_directory
2 argv
3 envv
4 spawn_flags
5 child_setup
6 child_setup_data
7 child_setup_data_destroy
8 timeout
9 cancellable
10 callback
11 user_data
```

Manual runtime testing showed that `child_setup_data_destroy` is exposed by
FunctionInfo but is not accepted in the Python-callable positional form. Phase 4
therefore calls `spawn_async` with `child_setup_data`, omits
`child_setup_data_destroy`, passes `Gio.Cancellable()` for `cancellable`, and
passes a no-op spawn callback. It does not interpret child-exit status because
`spawn_finish` was not available locally.

Supersession note: Phase 7 and Phase 8 later verified child-exit lifecycle
behavior through a `Vte.Terminal.do_child_exited(status)` subclass path. The
current app spawn callback now handles spawn errors and optional debug
diagnostics; child-exit behavior is no longer pending.

## 14. Phase 6 Lifecycle Research

Phase 6 rechecked local lifecycle-related VTE API evidence.
`GObject.signal_list_names(Vte.Terminal)` returned no signal names.
Lifecycle-like members included `do_child_exited`, `watch_child`, and
`watch_closure`, but no runtime contract was verified. Child lifecycle handling
remains pending and should not assume signal names.

Supersession note: Phase 7 and Phase 8 verified the runtime contract. The app
now uses `do_child_exited(status)` without explicit `watch_child(pid)`.
