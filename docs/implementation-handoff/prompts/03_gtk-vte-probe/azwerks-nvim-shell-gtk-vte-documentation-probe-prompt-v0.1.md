# Codex Prompt — AZWERKS Neovim Shell Phase 3: GTK/VTE Documentation Probe

## Goal

Run a documentation and local API probe for the GTK/VTE layer of **AZWERKS Neovim Shell v0.1**.

This is **Phase 3** after:

```text
Phase 1 — Scaffolding
Phase 2 — CLI Parsing + Launch Contract
```

Do **not** implement the GTK application window yet.

Do **not** implement VTE spawning yet.

Do **not** launch Neovim yet.

The purpose of this phase is to verify the exact GTK, PyGObject, and VTE APIs available on the user’s system before writing GTK/VTE application code.

This phase must produce documentation that can safely guide the next implementation phase.

---

## Working Directory

Work only inside:

```text
/media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
```

Start with:

```zsh
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
pwd
find . -maxdepth 4 -type f | sort
```

---

## Preflight: Confirm Phase 2 Is Complete

Before probing GTK/VTE, verify the current project state.

Run:

```zsh
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/smoke.sh
```

If Phase 2 tests fail, stop and report that the CLI phase must be repaired first.

Do not continue into GTK/VTE probing if the CLI layer is broken.

---

## Scope

Allowed files to create or modify:

```text
docs/gtk-vte-api-probe.md
docs/dependency-notes.md
docs/implementation-plan.md
README.md
CHANGELOG.md
tests/smoke.sh
```

Do not modify unless necessary:

```text
src/azwerks_nvim_shell/main.py
src/azwerks_nvim_shell/app.py
src/azwerks_nvim_shell/cli.py
src/azwerks_nvim_shell/config.py
src/azwerks_nvim_shell/radium.py
```

This phase is primarily documentation and environment verification.

---

## Required Dependency Checks

Check installed package availability and versions.

Run:

```zsh
dpkg-query -W -f='${Package} ${Version}\n' \
  python3-gi \
  gir1.2-gtk-4.0 \
  gir1.2-vte-3.91 \
  desktop-file-utils 2>/dev/null || true
```

Also check:

```zsh
python3 --version
command -v desktop-file-validate || true
command -v gtk-launch || true
command -v nvim || true
command -v /home/blndsft/.local/bin/nvim || true
```

Record all results in:

```text
docs/gtk-vte-api-probe.md
```

Do not install missing packages.

If any required package is missing, report it clearly.

---

## Required Python GI Import Probe

Run:

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

If this fails, stop and report the exact failure.

Do not guess a fix.

---

## Required VTE API Probe

Probe available `Vte.Terminal` methods.

Run:

```zsh
python3 - <<'PY'
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Vte", "3.91")

from gi.repository import Vte, GObject

methods = dir(Vte.Terminal)

wanted_methods = [
    "spawn_async",
    "set_color_foreground",
    "set_color_background",
    "set_color_cursor",
    "set_colors",
    "set_font",
    "set_font_scale",
    "copy_clipboard",
    "paste_clipboard",
    "get_text",
]

print("# Vte.Terminal method availability")
for name in wanted_methods:
    print(f"{name}: {name in methods}")

print()
print("# Vte.Terminal spawn_async doc")
spawn = getattr(Vte.Terminal, "spawn_async", None)
print(spawn)
print(getattr(spawn, "__doc__", "NO DOCSTRING"))

print()
print("# Vte.Terminal signals")
try:
    signals = GObject.signal_list_names(Vte.Terminal)
    for signal in sorted(signals):
        print(signal)
except Exception as exc:
    print("Could not list signals:", repr(exc))
PY
```

Record the results in:

```text
docs/gtk-vte-api-probe.md
```

Important: do not invent the `spawn_async` signature. Use what the local introspection/docs show.

---

## Required GTK API Probe

Probe GTK application/window basics.

Run:

```zsh
python3 - <<'PY'
import gi
gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

print("# Gtk method/class availability")

items = [
    ("Gtk.Application", hasattr(Gtk, "Application")),
    ("Gtk.ApplicationWindow", hasattr(Gtk, "ApplicationWindow")),
    ("Gtk.Box", hasattr(Gtk, "Box")),
    ("Gtk.Orientation", hasattr(Gtk, "Orientation")),
    ("Gtk.CssProvider", hasattr(Gtk, "CssProvider")),
    ("Gtk.StyleContext", hasattr(Gtk, "StyleContext")),
]

for name, exists in items:
    print(f"{name}: {exists}")

print()
print("# Gtk.Application doc")
print(getattr(Gtk.Application, "__doc__", "NO DOCSTRING"))

print()
print("# Gtk.ApplicationWindow doc")
print(getattr(Gtk.ApplicationWindow, "__doc__", "NO DOCSTRING"))
PY
```

Record the results in:

```text
docs/gtk-vte-api-probe.md
```

---

## Required Desktop Entry Probe

Validate the current desktop file if it exists.

Run:

```zsh
if command -v desktop-file-validate >/dev/null; then
  desktop-file-validate data/com.azwerks.NvimShell.desktop
else
  echo "desktop-file-validate not found"
fi
```

Record the result in:

```text
docs/gtk-vte-api-probe.md
```

Do not claim desktop integration is valid unless this validation passes.

---

## Required Documentation Output

Create or update:

```text
docs/gtk-vte-api-probe.md
```

Use this structure:

```markdown
# GTK/VTE API Probe — AZWERKS Neovim Shell v0.1

## 1. Scope

This document records the local GTK, PyGObject, VTE, and desktop-entry environment available for AZWERKS Neovim Shell.

## 2. Phase 2 Preflight Result

## 3. System Package Check

## 4. Python / GI Import Check

## 5. GTK API Availability

## 6. VTE API Availability

## 7. VTE Spawn API Notes

Document the discovered `Vte.Terminal.spawn_async` availability and docstring/signature evidence from local introspection.

Do not invent the signature.

## 8. VTE Color / Font API Notes

Document which color/font methods exist.

## 9. VTE Signal Notes

Document discovered VTE signals relevant to child exit or terminal lifecycle.

## 10. Desktop Entry Validation

## 11. Implementation Implications

Explain what the next phase may safely implement.

## 12. Risks / Unknowns

List anything that could not be verified.
```

---

## Update `docs/dependency-notes.md`

Update dependency notes with the actual package check results.

Do not claim a package is installed unless `dpkg-query` confirms it.

If a package is missing, write:

```text
Missing: <package-name>
```

Do not install it.

---

## Update `docs/implementation-plan.md`

Mark Phase 3 as completed only if:

```text
GTK import succeeded
VTE import succeeded
Vte.Terminal exists
desktop-file-validate result was recorded
docs/gtk-vte-api-probe.md was created
```

Do not mark future phases complete.

---

## Update `CHANGELOG.md`

Add a factual entry under `0.1.0`:

```markdown
- Added GTK/VTE API probe documentation.
- Verified local GTK/VTE import and method availability.
```

Only include the second line if imports actually succeeded.

---

## Update `tests/smoke.sh`

Add a non-GUI dependency/import probe that does not open a window:

```zsh
python3 - <<'PY'
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Vte", "3.91")
from gi.repository import Gtk, Vte
print("GTK/VTE import smoke OK")
PY
```

Do not require a display server.

Do not launch the app.

Do not open a GTK window.

---

## Validation Commands

After updates, run:

```zsh
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/smoke.sh
```

Then show:

```zsh
sed -n '1,260p' docs/gtk-vte-api-probe.md
```

---

## Hard Constraints

Do not:

```text
implement GTK window code
implement VTE spawn code
launch Neovim
open a GUI window
install packages
use sudo
modify files outside the project
modify ~/.config/nvim
modify ~/.local/bin/nvim
modify ~/.local/opt/nvim-linux-x86_64
guess API behavior
claim success without command output
```

This is a documentation and API verification phase only.

---

## Done When

The phase is complete when:

```text
Phase 2 tests still pass
GTK/VTE import probe has been run
VTE method availability has been documented
VTE spawn_async evidence has been documented
VTE color/font method availability has been documented
desktop file validation result has been documented
docs/gtk-vte-api-probe.md exists
dependency notes are updated
implementation plan is updated
smoke test includes non-GUI GTK/VTE import check
no GTK window was implemented
no Neovim process was launched
```

---

## Final Report Format

When finished, report:

```markdown
# AZWERKS Neovim Shell Phase 3 Report — GTK/VTE Documentation Probe

## Summary

## Phase 2 Preflight Result

## Dependency Check Result

## GTK Import Result

## VTE Import Result

## VTE API Findings

## Desktop Entry Validation

## Files Changed

## Validation Commands Run

## Results

## Known Unknowns

## Next Recommended Prompt
```

