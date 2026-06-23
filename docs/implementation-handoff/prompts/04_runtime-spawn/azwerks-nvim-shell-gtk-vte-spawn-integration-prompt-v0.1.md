# Codex Prompt — AZWERKS Neovim Shell Phase 4: GTK/VTE Window + Controlled Spawn Integration

## Goal

Implement the first working GTK/VTE runtime layer for **AZWERKS Neovim Shell v0.1**.

This is **Phase 4**, following:

```text id="oz6lvh"
Phase 1 — Scaffolding
Phase 2 — CLI Parsing + Launch Contract
Phase 3 — GTK/VTE Documentation Probe
```

Phase 3 confirmed:

```text id="zrsnki"
python3-gi installed
gir1.2-gtk-4.0 installed
gir1.2-vte-3.91 installed
desktop-file-utils installed
Gtk.Application import works
Gtk.ApplicationWindow import works
Vte.Terminal import works
Vte.Terminal.spawn_async exists
Vte.Terminal color/font APIs exist
desktop-file-validate runs successfully
```

The goal of this phase is to implement:

```text id="f5xpgf"
GTK application startup
GTK application window
VTE terminal widget
safe Neovim process spawn through the locally documented Vte.Terminal.spawn_async API
basic runtime error handling
manual GUI launch path
```

Do **not** implement install behavior in this phase.

Do **not** redesign the app.

Do **not** modify the user’s Neovim config.

---

## Working Directory

Work only inside:

```text id="mx8xwu"
/media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
```

Start with:

```zsh id="wqtck4"
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
pwd
find . -maxdepth 4 -type f | sort
```

---

## Required Preflight

Before implementing, run:

```zsh id="r06odn"
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/smoke.sh
```

Then inspect the Phase 3 probe:

```zsh id="abajdt"
sed -n '1,260p' docs/gtk-vte-api-probe.md
```

If the Phase 3 probe does not contain the local `Vte.Terminal.spawn_async` docstring or method availability results, stop and report that Phase 3 must be completed first.

Do not implement spawn behavior from memory.

Use the locally recorded `spawn_async` information.

---

## Scope

Allowed files to modify:

```text id="00wwvq"
src/azwerks_nvim_shell/main.py
src/azwerks_nvim_shell/app.py
src/azwerks_nvim_shell/cli.py
src/azwerks_nvim_shell/config.py
src/azwerks_nvim_shell/radium.py
scripts/dev-run.sh
tests/smoke.sh
README.md
CHANGELOG.md
docs/architecture.md
docs/implementation-plan.md
docs/gtk-vte-api-probe.md
```

Allowed files to create if useful:

```text id="jopeo2"
tests/test_app_contract.py
docs/runtime-notes.md
```

Do not modify:

```text id="tlfdti"
/home/blndsft/.config/nvim
/home/blndsft/.local/bin/nvim
/home/blndsft/.local/opt/nvim-linux-x86_64
```

Do not install packages.

Do not use sudo.

Do not write outside the project.

---

## Important Boundary

This app remains a GTK/VTE wrapper around terminal Neovim.

Do not implement:

```text id="b2r8mh"
nvim --embed
nvim_ui_attach()
MessagePack-RPC
external UI protocol
manual Neovim grid rendering
custom Neovim popup rendering
custom Neovim command line rendering
```

Architecture remains:

```text id="dejau2"
AZWERKS Neovim Shell
  └── Gtk.Application
      └── Gtk.ApplicationWindow
          └── Vte.Terminal
              └── nvim
```

---

## Required Runtime Behavior

### 1. CLI still controls launch contract

The existing Phase 2 CLI parser remains authoritative.

The app must use the parser’s launch contract:

```text id="r2fdv2"
nvim_binary
cwd
positional_args
nvim_argv
```

Do not re-parse arguments in `app.py`.

Do not duplicate CLI logic in GTK code.

Do not pass `--cwd` to Neovim.

Spawn Neovim with:

```text id="n1k0zo"
[nvim_binary, *positional_args]
```

Set the process working directory through the VTE spawn API, not by adding Neovim flags.

---

### 2. `--help` and `--version`

These must continue to exit before GTK starts.

Examples:

```zsh id="iz1ok4"
scripts/dev-run.sh --help
scripts/dev-run.sh --version
```

Expected behavior:

```text id="r6omwg"
print output
exit 0
do not open GTK
do not create VTE terminal
do not spawn Neovim
```

---

### 3. CLI errors

CLI errors must continue to exit before GTK starts.

Examples:

```zsh id="nxj4hn"
scripts/dev-run.sh --foo
scripts/dev-run.sh --cwd
scripts/dev-run.sh --nvim-bin /bad/path
```

Expected behavior:

```text id="sqxda9"
print exact error to stderr
exit non-zero
do not open GTK
do not create VTE terminal
do not spawn Neovim
```

---

### 4. Valid invocation

Examples:

```zsh id="tpa8b5"
scripts/dev-run.sh
scripts/dev-run.sh /path/to/file
scripts/dev-run.sh --cwd /path/to/project
scripts/dev-run.sh --nvim-bin /home/blndsft/.local/bin/nvim
```

Expected behavior:

```text id="38izwy"
create GTK application
create GTK application window
create VTE terminal widget
spawn Neovim through VTE
show terminal Neovim in the window
```

Do not claim this works unless manually tested in a graphical session.

---

## GTK Implementation Requirements

Implement `app.py` using GTK4 through PyGObject.

Use the import pattern validated in Phase 3:

```python id="6jvot4"
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Vte", "3.91")
from gi.repository import Gtk, Vte, GLib, Gio, Gdk, Pango
```

Only import modules that are actually needed.

Create a GTK application structure using `Gtk.Application`.

Use application ID:

```text id="t7p5jw"
com.azwerks.NvimShell
```

Create a main application window titled:

```text id="uqrqkh"
AZWERKS Neovim
```

Default window size:

```text id="9b04tl"
1200 x 800
```

If GTK APIs differ locally, adapt to the installed API and document the change.

---

## VTE Implementation Requirements

Create a `Vte.Terminal` widget.

Spawn Neovim using the locally documented `Vte.Terminal.spawn_async` API.

Do not invent the signature.

Use the exact local documentation captured in:

```text id="r6q446"
docs/gtk-vte-api-probe.md
```

If needed, re-run a focused introspection probe before coding:

```zsh id="d48cyz"
python3 - <<'PY'
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Vte", "3.91")
from gi.repository import Vte
spawn = getattr(Vte.Terminal, "spawn_async")
print(spawn)
print(getattr(spawn, "__doc__", "NO DOCSTRING"))
PY
```

The implementation must:

```text id="h65se6"
use argv arrays
preserve paths with spaces
set cwd through the spawn API
surface spawn errors clearly
avoid shell=True
avoid os.system()
avoid command-string concatenation
```

---

## Environment Requirements

When spawning Neovim, preserve the current process environment.

Ensure the child environment includes:

```text id="3lpoig"
TERM=xterm-256color
COLORTERM=truecolor
```

Do not wipe the user environment.

Do not override unrelated environment variables.

---

## Visual Defaults

Apply only basic visual defaults that are supported by the local VTE API.

Use constants from `radium.py`.

Expected colors:

```text id="r4xz8s"
background: #202521
foreground: #ddecc4
surface:    #23282b
accent:     #ceda4a
muted:      #94a87a
faint:      #8e9290
```

Apply:

```text id="81uzyd"
terminal foreground color if supported
terminal background color if supported
terminal cursor color if supported
terminal font if supported
```

Default font:

```text id="tppdus"
Monospace 11
```

Do not add:

```text id="ygl067"
glow
scanlines
CRT effects
cyberpunk styling
decorative noise
animations
fake terminal chrome
```

If a color or font API call fails or is unavailable, do not fake it. Record it in the report.

---

## Process Lifecycle

Handle Neovim child exit if the local VTE API exposes a documented signal or callback.

Phase 3 reported that `GObject.signal_list_names(Vte.Terminal)` printed no signal names.

Therefore:

```text id="llowcb"
do not invent signal names
do not assume child-exited exists unless verified locally
```

Before connecting any VTE signal, verify it exists.

If child-exit detection cannot be verified, document this as a known limitation and keep the app behavior simple.

---

## Error Handling

If GTK/VTE import fails:

```text id="942ag4"
print a clear error
exit non-zero
do not produce a traceback unless useful for debugging
```

If Neovim spawn fails:

```text id="tthv41"
show a clear error in stderr
if possible, show a clear terminal/window message
exit or keep window open only if behavior is intentional and documented
```

Do not hide failures.

---

## Tests

### Unit Tests

Existing CLI tests must continue to pass.

If adding app contract tests, they must not require a GUI display.

Suggested tests:

```text id="qti29u"
main.py does not start GTK for --help
main.py does not start GTK for --version
main.py does not start GTK for CLI errors
valid launch contract is passed toward app runner
environment preparation preserves existing env
environment preparation adds TERM and COLORTERM where needed
```

Use mocks or pure helper functions.

Do not open a GTK window in unit tests.

Do not spawn Neovim in unit tests.

### Smoke Test

Update `tests/smoke.sh` to keep:

```zsh id="5zqo95"
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

Keep the non-GUI GTK/VTE import check.

Do not make smoke tests require a display server.

---

## Manual Runtime Test

Only run this if a graphical session is available:

```zsh id="k5ebvu"
scripts/dev-run.sh
```

Also test:

```zsh id="j1lpqv"
scripts/dev-run.sh --help
scripts/dev-run.sh --version
scripts/dev-run.sh --foo
scripts/dev-run.sh --cwd
```

If `scripts/dev-run.sh` opens a GTK window and Neovim appears inside the VTE terminal, record that honestly.

If it cannot be tested because no display is available, say so clearly.

Do not claim runtime success without testing.

---

## Documentation Updates

Update:

```text id="exmsez"
docs/architecture.md
docs/implementation-plan.md
README.md
CHANGELOG.md
```

The docs must truthfully state the current implementation status.

If GTK/VTE window works, say so.

If Neovim spawning works only in manual local testing, say so.

If child-exit behavior is not implemented because no verified signal was found, say so.

---

## Validation Commands

Run:

```zsh id="80ffpk"
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell

python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/smoke.sh
```

Run CLI non-GUI checks:

```zsh id="zlnnix"
scripts/dev-run.sh --help
scripts/dev-run.sh --version
scripts/dev-run.sh --foo
scripts/dev-run.sh --cwd
scripts/dev-run.sh --nvim-bin /bad/path
```

Run GUI check only if available:

```zsh id="tn1pnt"
scripts/dev-run.sh
```

---

## Hard Constraints

Do not:

```text id="gme52b"
use sudo
install packages
modify /usr
modify system desktop entries
modify Black Box
modify the user's Neovim config
modify the user's Neovim binary
delete user files
use Electron
use a webview
use nvim --embed
use nvim_ui_attach
use shell=True
use os.system()
invent VTE signals
invent spawn_async signature
claim GUI success without running GUI
```

---

## Done When

This phase is complete when:

```text id="w1o7lo"
GTK Application code exists
GTK ApplicationWindow code exists
Vte.Terminal widget code exists
VTE spawn_async is used according to local documentation
Neovim argv comes from the existing launch contract
cwd comes from the existing launch contract
--help exits before GTK
--version exits before GTK
CLI errors exit before GTK
unit tests pass
smoke test passes
README is updated truthfully
CHANGELOG is updated truthfully
implementation plan marks Phase 4 complete only if actually completed
no files outside the project were modified
```

---

## Final Report Format

When finished, report:

```markdown id="p9ggnn"
# AZWERKS Neovim Shell Phase 4 Report — GTK/VTE Spawn Integration

## Summary

## Preflight Result

## GTK/VTE APIs Used

## Files Changed

## CLI Behavior Verified

## GTK Window Behavior

## VTE Spawn Behavior

## Visual Defaults Applied

## Process Lifecycle Handling

## Tests Run

## Manual GUI Test Result

## Known Limitations

## What Was Not Done

## Next Recommended Prompt
```

