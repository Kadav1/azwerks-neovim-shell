# Codex Prompt - azwerks Neovim Shell Phase 8: Runtime Diagnostics + Packaging Readiness

## Goal

Implement **Phase 8 runtime diagnostics and packaging readiness** for **azwerks Neovim Shell v0.1**.

This phase must focus on:

```text id="a6ru66"
investigating the GLib waitid(...): No child processes warning
preserving verified lifecycle behavior
improving runtime diagnostics
confirming install/package readiness
tightening documentation
preparing for a final regression audit
```

Do **not** change the verified lifecycle behavior unless a cleaner local API path is proven with evidence.

Do **not** suppress warnings blindly.

Do **not** hide stderr.

Do **not** modify Neovim config.

Do **not** modify the Neovim binary.

Do **not** use sudo.

Do **not** write to system paths.

---

## Previous Phase Status

Phase 7 implemented VTE child lifecycle behavior.

Known limitations after Phase 7:

```text id="hivcuk"
A GLib waitid(...): No child processes warning appears during lifecycle checks.
The lifecycle event is still observed.
The app exits successfully.
GTK theme parser warnings remain external desktop theme warnings.
```

This phase should investigate the GLib warning without breaking the working lifecycle behavior.

---

## Working Directory

Work only inside:

```text id="tv8e42"
/media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
```

Start with:

```zsh id="p7iq7w"
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
pwd
find . -maxdepth 4 -type f | sort
```

---

## Required Preflight

Run:

```zsh id="fxim5p"
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install_scripts.sh
tests/smoke.sh
```

If preflight fails, stop and report the failure.

Do not investigate packaging readiness if the current app is already broken.

---

## Scope

Allowed files to modify:

```text id="c3ddx0"
src/azwerks_nvim_shell/app.py
src/azwerks_nvim_shell/config.py
README.md
CHANGELOG.md
docs/child-lifecycle-research.md
docs/child-lifecycle-behavior.md
docs/desktop-integration.md
docs/install-uninstall-safety.md
docs/implementation-plan.md
tests/smoke.sh
```

Allowed files to create:

```text id="ycis78"
docs/runtime-diagnostics.md
docs/glib-waitid-warning-investigation.md
docs/packaging-readiness.md
docs/phase-8-runtime-diagnostics-report.md
scripts/probe-vte-lifecycle-variants.py
tests/test_runtime_diagnostics.py
```

Do not modify unless required:

```text id="r9rbvq"
src/azwerks_nvim_shell/main.py
src/azwerks_nvim_shell/cli.py
src/azwerks_nvim_shell/radium.py
scripts/install-user.sh
scripts/uninstall-user.sh
data/com.azwerks.NvimShell.desktop
data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

Do not modify:

```text id="ssxg83"
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

```text id="mcigpf"
use sudo
install packages
modify system paths
modify Black Box
modify Neovim config
modify Neovim binary
use nvim --embed
use nvim_ui_attach
implement external UI protocol behavior
suppress GLib warnings blindly
redirect stderr to hide warnings
remove working lifecycle behavior without a proven replacement
add GUI-launching checks to automated smoke tests
spawn Neovim in automated tests
```

---

## Part 1 - Capture Current Warning Evidence

Create:

```text id="x6t901"
docs/glib-waitid-warning-investigation.md
```

Record the exact observed warning.

Run the current lifecycle probe and capture output.

If a graphical session is available:

```zsh id="1dvchl"
python3 scripts/probe-vte-child-lifecycle.py > /tmp/azwerks-vte-probe.stdout 2> /tmp/azwerks-vte-probe.stderr || true

printf '%s\n' '--- STDOUT ---'
cat /tmp/azwerks-vte-probe.stdout

printf '%s\n' '--- STDERR ---'
cat /tmp/azwerks-vte-probe.stderr
```

If a graphical session is not available, skip runtime probe and document why.

Check display availability:

```zsh id="bnwzho"
echo "${DISPLAY:-}"
echo "${WAYLAND_DISPLAY:-}"
```

Do not claim runtime results if no graphical session is available.

---

## Part 2 - Inspect Current Lifecycle Implementation

Inspect the current app lifecycle code.

Run:

```zsh id="wh1rg5"
command grep -RIn "watch_child\\|child-exited\\|eof\\|spawn_async\\|waitid\\|waitpid\\|child_watch\\|close_pid\\|quit\\|destroy" \
  src scripts docs tests 2>/dev/null || true
```

Document:

```text id="kku0dt"
where spawn_async is called
where watch_child is called
where child-exited is connected
whether any manual wait/waitpid/waitid call exists
whether any GLib child-watch API is used
whether lifecycle handling can run twice
whether app quit/destroy can be called multiple times
```

Do not change code yet.

---

## Part 3 - Local API Recheck

Re-run focused local introspection.

```zsh id="g9jmig"
python3 - <<'PY'
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Vte", "3.91")

from gi.repository import Vte, GObject, GLib

print("# VTE lifecycle-related methods")
for name in dir(Vte.Terminal):
    lowered = name.lower()
    if any(token in lowered for token in ["watch", "child", "exit", "spawn", "pty", "pid"]):
        print(name)

print()
print("# VTE signal lookup")
for signal_name in ["child-exited", "eof", "contents-changed"]:
    signal_id = GObject.signal_lookup(signal_name, Vte.Terminal)
    print(f"{signal_name}: {signal_id}")
    if signal_id:
        try:
            print("query:", GObject.signal_query(signal_id))
        except Exception as exc:
            print("query failed:", repr(exc))

print()
print("# spawn_async doc")
spawn = getattr(Vte.Terminal, "spawn_async", None)
print(getattr(spawn, "__doc__", "NO DOCSTRING"))

print()
print("# watch_child doc")
watch_child = getattr(Vte.Terminal, "watch_child", None)
print(getattr(watch_child, "__doc__", "NO DOCSTRING"))

print()
print("# GLib spawn/child-watch related names")
for name in dir(GLib):
    lowered = name.lower()
    if any(token in lowered for token in ["spawn", "child", "pid"]):
        print(name)
PY
```

Record findings in:

```text id="5lzqz2"
docs/glib-waitid-warning-investigation.md
```

---

## Part 4 - Lifecycle Variant Probe

Create:

```text id="kmv3r5"
scripts/probe-vte-lifecycle-variants.py
```

Purpose:

```text id="eh9pf8"
Compare minimal VTE child lifecycle paths.
Identify whether the GLib waitid warning is caused by duplicate watching/reaping.
Prove whether a cleaner local API path exists.
Do not use Neovim.
```

The probe should test safe, short-lived non-Neovim child commands only.

Use a harmless child command:

```text id="7iphv4"
/bin/sh -lc 'printf "azwerks lifecycle variant probe\n"; exit 7'
```

The probe should compare variants only if supported by local APIs:

```text id="lnq6iv"
Variant A - current lifecycle path
Variant B - spawn_async callback + child-exited connection, without explicit watch_child if possible
Variant C - explicit watch_child once, child-exited connection once
Variant D - child-exited connection only if signal lookup succeeds
```

Do not invent unsupported variants.

Do not use manual `os.waitpid()` or `waitid()`.

Do not add GLib child watches unless the local API evidence supports it.

For each variant, record:

```text id="uoy2pc"
whether child-exited was observed
whether eof was observed
whether app quit occurred
whether the expected child status was visible
whether GLib waitid/ECHILD warning appeared
whether any traceback occurred
```

The probe may open a minimal GTK/VTE window.

Do not run it in automated smoke tests.

Only run manually if a graphical session is available:

```zsh id="bnbb0q"
python3 scripts/probe-vte-lifecycle-variants.py
```

Record results in:

```text id="rlm9l5"
docs/glib-waitid-warning-investigation.md
```

---

## Part 5 - Decision Gate

After the variant probe, decide one of three outcomes.

### Outcome A - Current behavior is best available

Use this outcome if:

```text id="ey2j9z"
lifecycle event is observed
app exits successfully
all alternative variants either fail or still warn
no cleaner local API path is proven
```

Required action:

```text id="u1l8lo"
keep current lifecycle behavior
document the warning as a known GLib/VTE lifecycle warning
do not suppress it
do not hide it
```

### Outcome B - Cleaner local path is proven

Use this outcome if:

```text id="uh8snt"
an alternative variant observes child exit
app exits successfully
the GLib waitid warning disappears
no new regression appears
the implementation path uses documented local APIs
```

Required action:

```text id="463gej"
apply the minimal lifecycle change
update tests/docs
record before/after evidence
```

### Outcome C - Lifecycle behavior is unstable

Use this outcome if:

```text id="smkxkq"
child exit is not reliably observed
app does not exit reliably
warning is accompanied by lifecycle failure
```

Required action:

```text id="5mdw7n"
do not pretend the app is stable
mark lifecycle as requiring further work
prepare a focused Phase 9 repair prompt
```

Do not choose an outcome without evidence.

---

## Part 6 - Runtime Diagnostics

Add lightweight runtime diagnostics only if useful.

Preferred approach:

```text id="54hu4e"
no noisy default logs
optional debug logs enabled by environment variable
```

If implemented, use:

```text id="hw8kgp"
AZWERKS_NVIM_SHELL_DEBUG=1
```

Debug logs may report:

```text id="bhgu6g"
resolved nvim binary
resolved cwd
final argv
whether VTE spawn callback fired
whether watch_child was used
whether child-exited was observed
child exit status if available
```

Do not log sensitive environment variables.

Do not log full user environment.

Do not write logs to disk unless explicitly requested.

Do not add dependencies.

Add unit tests for diagnostic helper functions if implemented.

---

## Part 7 - Packaging Readiness

Create:

```text id="cczqkm"
docs/packaging-readiness.md
```

Check and document:

```text id="m0cw14"
project structure
pyproject.toml correctness
entry point correctness
desktop file validation
icon existence
install-user.sh behavior
uninstall-user.sh behavior
wrapper behavior
README completeness
CHANGELOG truthfulness
known limitations
manual GUI verification status
```

Run:

```zsh id="n51cyr"
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install_scripts.sh
tests/smoke.sh

scripts/install-user.sh --dry-run
scripts/install-user.sh --validate-only
scripts/uninstall-user.sh --dry-run

desktop-file-validate data/com.azwerks.NvimShell.desktop
test -s data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
command grep -q "<svg" data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

If installed app exists, verify:

```zsh id="ea1fsv"
test -x ~/.local/bin/azwerks-nvim-shell
~/.local/bin/azwerks-nvim-shell --help
~/.local/bin/azwerks-nvim-shell --version
desktop-file-validate ~/.local/share/applications/com.azwerks.NvimShell.desktop
test -s ~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

Do not run real uninstall unless needed for readiness verification and preceded by dry-run.

---

## Part 8 - Documentation Updates

Update:

```text id="g5u26w"
README.md
CHANGELOG.md
docs/runtime-diagnostics.md
docs/glib-waitid-warning-investigation.md
docs/packaging-readiness.md
docs/child-lifecycle-behavior.md
docs/implementation-plan.md
```

Documentation must truthfully state:

```text id="hchse8"
whether the GLib waitid warning remains
whether it affects app behavior
whether a cleaner local lifecycle path was found
whether lifecycle behavior was changed
whether debug diagnostics were added
whether packaging readiness checks passed
whether manual gtk-launch confirmation remains pending
```

Do not erase known limitations unless they were actually fixed.

---

## Part 9 - Automated Test Policy

Automated tests must remain safe.

They may run:

```text id="kzi2gj"
Python compile
unit tests
install-script tests
smoke test
non-GUI GTK/VTE import probe
desktop file validation
icon file validation
```

They must not run:

```text id="7x08xq"
gtk-launch
scripts/dev-run.sh
Neovim
GUI lifecycle probe
real uninstall
real install unless explicitly intended
```

---

## Validation Commands

Run:

```zsh id="2jyn9i"
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell

python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install_scripts.sh
tests/smoke.sh

scripts/install-user.sh --dry-run
scripts/install-user.sh --validate-only
scripts/uninstall-user.sh --dry-run
desktop-file-validate data/com.azwerks.NvimShell.desktop
```

If graphical session is available, run manual probes:

```zsh id="znr6qv"
python3 scripts/probe-vte-child-lifecycle.py
python3 scripts/probe-vte-lifecycle-variants.py
```

Manual app test if needed:

```zsh id="b382jl"
scripts/dev-run.sh
```

Then inside Neovim:

```vim id="q6mvfr"
:qa
```

Do not claim GUI/manual success unless actually tested.

---

## Done When

This phase is complete when:

```text id="vnwr27"
preflight passes
GLib waitid warning is investigated
current lifecycle code is inspected
variant probe is created
variant probe is run or skipped with reason
decision gate outcome is documented
verified lifecycle behavior is preserved
cleaner lifecycle path is implemented only if proven
runtime diagnostics are added or explicitly deferred
packaging readiness document exists
README is updated
CHANGELOG is updated
implementation plan is updated
automated tests pass
no system paths were modified
Neovim config was not modified
Neovim binary was not modified
```

---

## Final Report Format

When finished, report:

```markdown id="xq7qec"
# azwerks Neovim Shell Phase 8 Report - Runtime Diagnostics + Packaging Readiness

## Summary

## Preflight Result

## Files Changed

## GLib waitid Warning Investigation

## Lifecycle Variant Probe

## Decision Gate Outcome

## Lifecycle Behavior Change

## Runtime Diagnostics

## Packaging Readiness

## Tests Run

## Manual GUI / Lifecycle Test Result

## Known Limitations

## What Was Not Done

## Next Recommended Prompt
```
