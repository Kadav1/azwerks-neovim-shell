# Codex Prompt - AZWERKS Neovim Shell Phase 7: VTE Child Lifecycle Probe + Implementation

## Goal

Implement **Phase 7 child lifecycle behavior** for **AZWERKS Neovim Shell v0.1**.

This phase must focus only on:

```text id="kncipk"
validating the local VTE child lifecycle API path
testing a minimal child process lifecycle
implementing clean app behavior when the Neovim child exits
documenting what was verified
```

Do **not** broaden the app.

Do **not** modify Neovim config.

Do **not** modify the Neovim binary.

Do **not** implement `nvim --embed`.

Do **not** implement the Neovim external UI protocol.

---

## Previous Phase Status

Phase 6 completed launcher and install hardening.

Known limitations after Phase 6:

```text id="lfp2j4"
Child-exit lifecycle behavior is still pending.
Full visual gtk-launch confirmation remains a manual desktop check.
GTK theme warnings, if observed, are external desktop theme CSS warnings.
```

This phase should address only the first limitation:

```text id="p1pf1f"
Child-exit lifecycle behavior is still pending.
```

The other two limitations should remain documented unless independently verified.

---

## Working Directory

Work only inside:

```text id="zgvnzh"
/media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
```

Start with:

```zsh id="d3h1ca"
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
pwd
find . -maxdepth 4 -type f | sort
```

---

## Required Preflight

Run:

```zsh id="3ijhku"
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install_scripts.sh
tests/smoke.sh
```

If preflight fails, stop and report the failure.

Do not continue into lifecycle work if the current app is already broken.

---

## Scope

Allowed files to modify:

```text id="vfz4lj"
src/azwerks_nvim_shell/app.py
src/azwerks_nvim_shell/config.py
tests/smoke.sh
README.md
CHANGELOG.md
docs/child-lifecycle-research.md
docs/implementation-plan.md
```

Allowed files to create:

```text id="wqscew"
scripts/probe-vte-child-lifecycle.py
docs/child-lifecycle-behavior.md
tests/test_lifecycle_contract.py
```

Do not modify unless necessary:

```text id="kzy1kg"
src/azwerks_nvim_shell/main.py
src/azwerks_nvim_shell/cli.py
src/azwerks_nvim_shell/radium.py
scripts/install-user.sh
scripts/uninstall-user.sh
data/com.azwerks.NvimShell.desktop
```

Do not modify:

```text id="1jd8zq"
/home/blndsft/.config/nvim
/home/blndsft/.local/bin/nvim
/home/blndsft/.local/opt/nvim-linux-x86_64
/usr
/usr/local
/etc
```

---

## Hard Constraints

Do not:

```text id="6hyxzy"
use sudo
install packages
modify system paths
modify Black Box
modify Neovim config
modify Neovim binary
use nvim --embed
use nvim_ui_attach
implement external UI protocol behavior
invent VTE signal names
invent VTE callback signatures
claim lifecycle behavior works unless tested
add GUI-launching tests to automated smoke tests
spawn Neovim in automated tests
```

---

## Part 1 - Local Lifecycle API Probe

Before changing app behavior, validate the local VTE lifecycle API.

Run:

```zsh id="h99431"
python3 - <<'PY'
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Vte", "3.91")

from gi.repository import Vte, GObject

print("# Vte.Terminal lifecycle API probe")

methods = dir(Vte.Terminal)
for name in [
    "spawn_async",
    "watch_child",
]:
    print(f"{name}: {name in methods}")

print()
print("# Signal lookup")

for signal_name in [
    "child-exited",
    "eof",
    "contents-changed",
]:
    signal_id = GObject.signal_lookup(signal_name, Vte.Terminal)
    print(f"{signal_name}: id={signal_id}")
    if signal_id:
        try:
            query = GObject.signal_query(signal_id)
            print(f"  query={query}")
        except Exception as exc:
            print(f"  query failed: {exc!r}")

print()
print("# signal_list_names result")
try:
    names = GObject.signal_list_names(Vte.Terminal)
    if names:
        for name in sorted(names):
            print(name)
    else:
        print("(no signal names returned)")
except Exception as exc:
    print("signal_list_names failed:", repr(exc))

print()
print("# spawn_async doc")
spawn = getattr(Vte.Terminal, "spawn_async", None)
print(spawn)
print(getattr(spawn, "__doc__", "NO DOCSTRING"))

print()
print("# watch_child doc")
watch_child = getattr(Vte.Terminal, "watch_child", None)
print(watch_child)
print(getattr(watch_child, "__doc__", "NO DOCSTRING"))
PY
```

Record results in:

```text id="poh16z"
docs/child-lifecycle-research.md
```

Do not continue to implementation unless local evidence shows a valid lifecycle path.

Acceptable evidence includes:

```text id="7lt407"
Vte.Terminal.watch_child exists
GObject.signal_lookup("child-exited", Vte.Terminal) returns a non-zero signal id
spawn_async callback behavior is understood from local docstring or minimal runtime probe
```

If these cannot be verified, stop and report that lifecycle implementation should not proceed.

---

## Part 2 - Minimal Runtime Probe

Create:

```text id="ibkcby"
scripts/probe-vte-child-lifecycle.py
```

Purpose:

```text id="qncjy1"
Open a minimal GTK/VTE window.
Spawn a short-lived non-Neovim child process.
Validate whether VTE reports child exit through the locally verified API path.
Exit the probe app after the child lifecycle event is observed.
```

Do **not** spawn Neovim in this probe.

Use a harmless child command such as:

```text id="ssg5ah"
/bin/sh -lc 'printf "azwerks lifecycle probe\n"; exit 7'
```

The probe must:

```text id="f8nso6"
use Gtk 4
use Vte 3.91
use Vte.Terminal
use the local spawn_async API
use watch_child only if locally available
connect child-exited only if signal_lookup confirms it
print observed lifecycle events to stdout/stderr
exit with 0 if lifecycle observation succeeds
exit non-zero if lifecycle observation fails
```

Do not invent callback signatures.

Use the local `spawn_async` docstring and trial carefully.

If a graphical session is not available, the probe may be skipped with a clear message.

Check display availability with:

```zsh id="n7b2bd"
echo "${DISPLAY:-}"
echo "${WAYLAND_DISPLAY:-}"
```

Run the probe only if a graphical session exists:

```zsh id="wdcrb2"
python3 scripts/probe-vte-child-lifecycle.py
```

Document the result in:

```text id="oxerq8"
docs/child-lifecycle-research.md
```

---

## Part 3 - Implementation Decision Gate

Only implement lifecycle behavior in the real app if the minimal runtime probe proves the local API path.

If the probe fails or cannot be run, do **not** change app lifecycle behavior.

If the probe succeeds, implement minimal app behavior:

```text id="v1brk3"
when the Neovim child exits, close the GTK application cleanly
print the child exit status to stderr or debug output
do not leave a dead VTE window open
do not crash
do not raise an unhandled exception
```

Preferred behavior:

```text id="zf7ty8"
Neovim exits
VTE reports child-exited
AZWERKS Neovim Shell quits cleanly
```

Do not implement complex restart, session restore, or prompt-on-exit behavior.

---

## Part 4 - App Implementation Requirements

If lifecycle implementation is approved by the evidence gate, update:

```text id="qr3osp"
src/azwerks_nvim_shell/app.py
```

Requirements:

```text id="v6v3am"
keep current GTK/VTE spawn behavior
preserve launch-contract argv and cwd behavior
connect child-exited only after verifying signal exists
call watch_child only if local API requires it and it is available
handle callback errors clearly
quit application cleanly on child exit
avoid duplicate signal connections
avoid lifecycle behavior for failed spawns
```

Do not hard-code unverified signal behavior.

Do not assume `child-exited` works unless runtime probe confirmed it.

If spawn callback gives a child PID and local `watch_child` exists, use that path if proven.

If spawn\_async itself already causes child-exited to fire without explicit watch\_child, document that and implement accordingly.

---

## Part 5 - Tests

Automated tests must not open GUI windows.

Automated tests must not spawn Neovim.

Allowed automated tests:

```text id="nn4mav"
pure lifecycle policy tests
helper function tests
signal-name constant tests
app runner injection/mocking tests
```

Create:

```text id="7x145y"
tests/test_lifecycle_contract.py
```

Suggested test coverage:

```text id="m0c68b"
lifecycle policy defaults to close-on-child-exit
child exit handler calls app quit function through injected mock
non-zero child status is recorded/logged without exception
handler is safe if app object is missing or already closing
lifecycle setup refuses to connect unknown signal in helper-level tests
```

Do not require a display server.

Do not instantiate a real GTK window in unit tests unless it is proven display-free.

Do not spawn child processes in unit tests unless they are pure non-GUI stdlib tests.

---

## Part 6 - Documentation Updates

Update:

```text id="m1ktal"
docs/child-lifecycle-research.md
docs/child-lifecycle-behavior.md
docs/implementation-plan.md
README.md
CHANGELOG.md
```

Documentation must say:

```text id="n0im2y"
which local VTE API path was verified
whether watch_child exists locally
whether child-exited signal lookup succeeded
whether the minimal runtime probe succeeded
whether real app lifecycle behavior was implemented
how the app behaves when Neovim exits
what remains unverified
```

If lifecycle implementation was not done, document why.

---

## Part 7 - Manual Runtime Verification

After implementation, run standard validation:

```zsh id="cdg8n7"
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install_scripts.sh
tests/smoke.sh
```

If a graphical session is available, test the app manually:

```zsh id="qrt15q"
scripts/dev-run.sh
```

Inside Neovim, exit cleanly:

```vim id="gfxmk5"
:qa
```

Expected behavior:

```text id="rt7wn3"
Neovim exits.
AZWERKS Neovim Shell detects child exit.
The GTK window closes cleanly.
No traceback appears.
No zombie app window remains.
```

If installed app exists, also test:

```zsh id="gv5zih"
~/.local/bin/azwerks-nvim-shell
```

Then exit Neovim with:

```vim id="j1k3t7"
:qa
```

Do not claim manual lifecycle success unless this is actually tested.

---

## Part 8 - Smoke Test Policy

Do not add GUI lifecycle tests to:

```text id="l1x3o1"
tests/smoke.sh
```

Smoke tests should remain non-GUI and safe.

They may run:

```text id="p7i20a"
Python compile
unit tests
install-script tests
non-GUI GTK/VTE import check
desktop file validation
```

They must not run:

```text id="ppx0x9"
gtk-launch
scripts/dev-run.sh
Neovim
the lifecycle probe if it opens a GUI
```

---

## Validation Commands

Run:

```zsh id="lcfgyi"
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell

python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install_scripts.sh
tests/smoke.sh
```

Run lifecycle API probe:

```zsh id="u6k5ay"
python3 scripts/probe-vte-child-lifecycle.py
```

Only run that probe if a graphical session is available.

Manual app lifecycle test:

```zsh id="z6kz8x"
scripts/dev-run.sh
```

Then inside Neovim:

```vim id="m38sf8"
:qa
```

Installed app test, if installed:

```zsh id="9lp7by"
~/.local/bin/azwerks-nvim-shell
```

Then inside Neovim:

```vim id="ejte9k"
:qa
```

---

## Done When

This phase is complete when:

```text id="l3pc39"
preflight passes
local lifecycle API probe is documented
minimal runtime lifecycle probe is created
runtime lifecycle probe is run or skipped with a clear reason
implementation decision is evidence-based
child-exit behavior is implemented only if verified
unit tests pass
smoke tests pass
manual lifecycle behavior is tested or clearly marked untested
README is updated
CHANGELOG is updated
implementation plan is updated
no system paths were modified
Neovim config was not modified
Neovim binary was not modified
```

---

## Final Report Format

When finished, report:

```markdown id="s6cemy"
# AZWERKS Neovim Shell Phase 7 Report - VTE Child Lifecycle

## Summary

## Preflight Result

## Local Lifecycle API Probe

## Minimal Runtime Probe Result

## Implementation Decision

## Files Changed

## Lifecycle Behavior Implemented

## Unit Tests

## Smoke Tests

## Manual App Lifecycle Test

## Installed App Lifecycle Test

## Known Limitations

## What Was Not Done

## Next Recommended Prompt
```

