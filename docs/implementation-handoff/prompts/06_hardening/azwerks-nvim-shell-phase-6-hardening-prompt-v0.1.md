# Codex Prompt — AZWERKS Neovim Shell Phase 6: Launcher, Install, and Lifecycle Hardening

## Goal

Implement **Phase 6 hardening** for **AZWERKS Neovim Shell v0.1**.

This phase focuses on:

```text id="kf8i62"
launcher/manual GUI verification
installed wrapper verification
optional desktop category cleanup
safe real uninstall verification
safe reinstall verification
focused child lifecycle research
documentation hardening
```

This phase must **not** modify the user’s Neovim config.

This phase must **not** modify the Neovim binary.

This phase must **not** use sudo.

This phase must **not** write to system paths.

This phase must **not** implement child-exit lifecycle behavior unless it is explicitly verified, trivial, isolated, and approved by the report. Prefer research/documentation only for lifecycle in this phase.

---

## Previous Phase Status

Phase 5 completed user-local desktop integration.

Known limitations after Phase 5:

```text id="n92wq3"
No child-exit lifecycle behavior yet.
GTK theme warnings are external theme CSS warnings, not app CSS.
No gtk-launch GUI launcher test was run.
No real uninstall was run.
```

This phase should address verification gaps, not broaden the app.

---

## Working Directory

Work only inside:

```text id="ygxvvh"
/media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
```

Start with:

```zsh id="29zr6j"
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
pwd
find . -maxdepth 4 -type f | sort
```

---

## Required Preflight

Run:

```zsh id="6bek8y"
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install_scripts.sh
tests/smoke.sh
```

If preflight fails, stop and report the failure.

Do not continue into install/uninstall or launcher verification if the current project is already broken.

---

## Scope

Allowed files to modify:

```text id="1n24im"
data/com.azwerks.NvimShell.desktop
scripts/install-user.sh
scripts/uninstall-user.sh
tests/smoke.sh
tests/test_install_scripts.sh
README.md
CHANGELOG.md
docs/desktop-integration.md
docs/install-uninstall-safety.md
docs/implementation-plan.md
docs/gtk-vte-api-probe.md
```

Allowed files to create:

```text id="w61f4f"
docs/launcher-verification.md
docs/child-lifecycle-research.md
docs/phase-6-hardening-report.md
```

Do not modify unless absolutely necessary:

```text id="jrwhsk"
src/azwerks_nvim_shell/main.py
src/azwerks_nvim_shell/app.py
src/azwerks_nvim_shell/cli.py
src/azwerks_nvim_shell/config.py
src/azwerks_nvim_shell/radium.py
```

If code changes are required, explain why before making them in the final report.

---

## Hard Constraints

Do not:

```text id="1rfibr"
use sudo
install packages
modify /usr
modify /usr/local
modify /etc
modify system desktop entries
modify Black Box
modify Neovim config
modify Neovim binary
delete unrelated files
run real uninstall before dry-run and ownership checks
run gtk-launch without clearly stating it opens the GUI
treat external GTK theme warnings as app bugs
implement nvim --embed
implement nvim_ui_attach
implement external UI protocol behavior
```

---

## Part 1 — Installed Wrapper Verification

Verify the installed wrapper if it exists.

Run:

```zsh id="jrr2n5"
test -x ~/.local/bin/azwerks-nvim-shell
~/.local/bin/azwerks-nvim-shell --help
~/.local/bin/azwerks-nvim-shell --version
```

Also check:

```zsh id="wuy3g6"
command -v azwerks-nvim-shell || true
```

Record:

```text id="y586ca"
whether wrapper exists
whether wrapper is executable
whether --help works
whether --version works
whether PATH resolves azwerks-nvim-shell
```

If `command -v azwerks-nvim-shell` fails but the wrapper exists at `~/.local/bin/azwerks-nvim-shell`, document that `~/.local/bin` may not be on PATH.

Do not modify shell profile files in this phase.

---

## Part 2 — Desktop Entry Validation

Validate the project desktop file:

```zsh id="kdw3eg"
desktop-file-validate data/com.azwerks.NvimShell.desktop
```

Validate the installed desktop file if it exists:

```zsh id="5i2i1u"
desktop-file-validate ~/.local/share/applications/com.azwerks.NvimShell.desktop
```

If the validator gives a non-fatal hint about multiple main categories, decide whether to clean it up.

Current category candidate:

```ini id="wwgl71"
Categories=Utility;TextEditor;Development;
```

Potential cleanup candidate:

```ini id="34u3rw"
Categories=Utility;TextEditor;
```

Only change categories if:

```text id="pii3vl"
desktop-file-validate still passes
the app remains discoverable as a text editor/utility
the change reduces warnings or hints
the change is documented
```

Do not make broad desktop-entry changes.

Do not remove `TextEditor` unless the validator requires it.

---

## Part 3 — Icon Validation

Verify project icon:

```zsh id="ev13h2"
test -s data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
command grep -q "<svg" data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

Verify installed icon if it exists:

```zsh id="uf1qxc"
test -s ~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
command grep -q "<svg" ~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

Do not redesign the icon in this phase.

Only fix the icon if it is missing, empty, or invalid SVG.

---

## Part 4 — Manual GUI Launcher Verification

Only run GUI tests if a graphical desktop session is available.

Check:

```zsh id="b0zlbv"
echo "${DISPLAY:-}"
echo "${WAYLAND_DISPLAY:-}"
```

If neither `DISPLAY` nor `WAYLAND_DISPLAY` is set, skip GUI launcher tests and document that no graphical session was available.

If a graphical session is available, run:

```zsh id="bfxan5"
gtk-launch com.azwerks.NvimShell
```

Important:

```text id="sj02f7"
gtk-launch opens the GUI app.
Do not run it inside automated smoke tests.
Do not claim success unless the window actually opened.
```

Manual verification checklist:

```text id="z7qzar"
App launches from gtk-launch.
Window title appears as AZWERKS Neovim or expected equivalent.
Neovim appears inside the VTE terminal.
App icon appears in launcher/window list if desktop environment exposes it.
No new app-specific CSS errors appear.
Known external GTK theme warnings, if present, are documented as external.
```

Record results in:

```text id="53pzdm"
docs/launcher-verification.md
```

---

## Part 5 — Real Uninstall Verification

This phase may run real uninstall only after dry-run and ownership checks.

First run:

```zsh id="43lfwg"
scripts/uninstall-user.sh --dry-run
```

Then inspect the install manifest:

```zsh id="gm83gc"
test -f ~/.local/share/azwerks-nvim-shell/install-manifest.txt && cat ~/.local/share/azwerks-nvim-shell/install-manifest.txt || true
```

Before real uninstall, verify that every target is app-owned and limited to:

```text id="jl25xx"
~/.local/bin/azwerks-nvim-shell
~/.local/share/applications/com.azwerks.NvimShell.desktop
~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
~/.local/share/azwerks-nvim-shell/
```

Then, only if safe:

```zsh id="ql5p2p"
scripts/uninstall-user.sh
```

After real uninstall, verify:

```zsh id="b3j3jl"
test ! -e ~/.local/bin/azwerks-nvim-shell
test ! -e ~/.local/share/applications/com.azwerks.NvimShell.desktop
test ! -e ~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
test ! -e ~/.local/share/azwerks-nvim-shell
```

Do not remove:

```text id="gxgqfw"
~/.config/nvim
~/.local/bin/nvim
~/.local/opt/nvim-linux-x86_64
```

Explicitly verify they still exist if present before uninstall:

```zsh id="w6htbe"
test -e ~/.config/nvim && echo "Neovim config still present" || true
test -e ~/.local/bin/nvim && echo "Neovim binary link still present" || true
test -e ~/.local/opt/nvim-linux-x86_64 && echo "Neovim install dir still present" || true
```

---

## Part 6 — Reinstall Verification

After successful real uninstall, reinstall:

```zsh id="qxspem"
scripts/install-user.sh
```

Then verify again:

```zsh id="01w7hy"
test -x ~/.local/bin/azwerks-nvim-shell
~/.local/bin/azwerks-nvim-shell --help
~/.local/bin/azwerks-nvim-shell --version
desktop-file-validate ~/.local/share/applications/com.azwerks.NvimShell.desktop
test -s ~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

Do not run `gtk-launch` again unless needed and a graphical session is available.

---

## Part 7 — Child Lifecycle Research

Research child lifecycle behavior without implementing it yet unless the evidence is extremely clear and the change is isolated.

Create:

```text id="mzoe9i"
docs/child-lifecycle-research.md
```

Investigate local VTE signal/API support.

Run:

```zsh id="25czsb"
python3 - <<'PY'
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Vte", "3.91")

from gi.repository import Vte, GObject

print("# Vte.Terminal signal names")
try:
    signals = GObject.signal_list_names(Vte.Terminal)
    for signal in sorted(signals):
        print(signal)
    if not signals:
        print("(no signals returned)")
except Exception as exc:
    print("signal_list_names failed:", repr(exc))

print()
print("# Vte.Terminal lifecycle-like members")
for name in dir(Vte.Terminal):
    lowered = name.lower()
    if any(key in lowered for key in ["child", "exit", "pty", "watch", "spawn"]):
        print(name)

print()
print("# spawn_async doc")
spawn = getattr(Vte.Terminal, "spawn_async", None)
print(spawn)
print(getattr(spawn, "__doc__", "NO DOCSTRING"))
PY
```

Search project files for current lifecycle assumptions:

```zsh id="zbsuhi"
command grep -RIn "child\\|exit\\|spawn\\|destroy\\|close\\|quit" src docs scripts tests 2>/dev/null || true
```

Document:

```text id="t95xwr"
whether VTE exposes a child-exit signal locally
whether app.py currently has lifecycle handling
whether there is a safe documented way to detect child exit
what a future Phase 7 patch should do
what must not be assumed
```

Do not invent signal names.

Do not implement lifecycle behavior unless the local API evidence is clear.

Preferred outcome for this phase:

```text id="4yfehv"
document lifecycle findings
prepare a future Phase 7 lifecycle prompt
```

---

## Part 8 — Documentation Updates

Update:

```text id="1u64gc"
README.md
CHANGELOG.md
docs/desktop-integration.md
docs/install-uninstall-safety.md
docs/implementation-plan.md
```

Create/update:

```text id="y77mrv"
docs/launcher-verification.md
docs/child-lifecycle-research.md
docs/phase-6-hardening-report.md
```

Documentation must truthfully reflect:

```text id="zm5zmv"
whether gtk-launch was tested
whether app launched from desktop entry
whether real uninstall was tested
whether reinstall was tested
whether category cleanup was performed
whether child lifecycle is still pending
```

Do not remove known limitations unless actually fixed and verified.

---

## Tests

Automated tests must not open GUI windows.

Automated tests must not spawn Neovim.

Keep:

```zsh id="08rmo2"
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install_scripts.sh
tests/smoke.sh
```

Do not add `gtk-launch` to `tests/smoke.sh`.

Manual GUI checks belong in documentation, not automated smoke tests.

---

## Validation Commands

Run:

```zsh id="yez4zy"
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell

python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install_scripts.sh
tests/smoke.sh

scripts/install-user.sh --dry-run
scripts/install-user.sh --validate-only
scripts/uninstall-user.sh --dry-run
```

If installed files exist and dry-run is safe, run real uninstall:

```zsh id="6pvdfn"
scripts/uninstall-user.sh
```

Then reinstall:

```zsh id="20wgrs"
scripts/install-user.sh
```

Then verify installed state:

```zsh id="02cw9e"
test -x ~/.local/bin/azwerks-nvim-shell
~/.local/bin/azwerks-nvim-shell --help
~/.local/bin/azwerks-nvim-shell --version
desktop-file-validate ~/.local/share/applications/com.azwerks.NvimShell.desktop
test -s ~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

If graphical session is available, run manual launcher test:

```zsh id="m471lj"
gtk-launch com.azwerks.NvimShell
```

---

## Done When

This phase is complete when:

```text id="6qxs4m"
preflight passes
installed wrapper is verified
desktop file validation is verified
icon validation is verified
gtk-launch is tested or explicitly skipped due to no display
real uninstall is tested safely or explicitly skipped with reason
reinstall is tested after uninstall if uninstall was run
child lifecycle research is documented
category cleanup is performed or explicitly not performed with reason
README is updated
CHANGELOG is updated
implementation plan is updated
no system paths are modified
Neovim config remains untouched
Neovim binary remains untouched
```

---

## Final Report Format

When finished, report:

```markdown id="jn1wpo"
# AZWERKS Neovim Shell Phase 6 Report — Launcher and Lifecycle Hardening

## Summary

## Preflight Result

## Files Changed

## Installed Wrapper Verification

## Desktop Entry Validation

## Category Cleanup Result

## Icon Validation

## gtk-launch Manual GUI Test

## Real Uninstall Verification

## Reinstall Verification

## Child Lifecycle Research

## Tests Run

## Known Limitations

## What Was Not Done

## Next Recommended Prompt
```
