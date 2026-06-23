# Codex Prompt — azwerks Neovim Shell Phase 9: Final Regression Audit + v0.1 Release-Readiness Review

## Goal

Perform a final regression audit and release-readiness review for **azwerks Neovim Shell v0.1**.

This is **Phase 9**.

This phase is an audit and release gate.

Do **not** add new features.

Do **not** redesign the app.

Do **not** modify Neovim config.

Do **not** modify the Neovim binary.

Do **not** use sudo.

Do **not** write to system paths.

Do **not** implement distribution packaging.

The goal is to determine whether the current project is ready to be treated as a stable **v0.1 user-local release candidate**.

---

## Previous Phase Status

Phase 8 completed runtime diagnostics and packaging-readiness review.

Known limitations after Phase 8:

```text id="v1w5lc"
Full visual gtk-launch confirmation remains a manual desktop check.
GTK theme parser warnings are external desktop theme CSS warnings.
Distribution packaging is not implemented; readiness is for current project/user-local install shape.
```

These limitations are acceptable for v0.1 if clearly documented.

---

## Working Directory

Work only inside:

```text id="d7abkz"
/media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
```

Start with:

```zsh id="ew5q3f"
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
pwd
find . -maxdepth 5 -type f | sort
```

---

## Audit Policy

This is an audit-first pass.

Allowed changes:

```text id="7z2606"
documentation typo fixes
documentation truth corrections
CHANGELOG truth corrections
test script typo fixes if they block audit execution
```

Do not make functional code changes unless:

```text id="dhm6zc"
the issue is trivial
the fix is clearly safe
the fix is required for audit commands to run
the fix is fully reported
```

If functional bugs are found, do not silently patch them. Record them as findings and recommend a follow-up patch prompt.

---

## Hard Constraints

Do not:

```text id="u4rexn"
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
run destructive uninstall without dry-run and explicit safety checks
add GUI tests to automated smoke tests
spawn Neovim in automated tests
implement nvim --embed
implement nvim_ui_attach
implement Neovim external UI protocol
implement distribution packaging
```

---

## Part 1 — Source Tree / File Presence Audit

Check expected files.

Expected core files:

```text id="j1zaz8"
README.md
CHANGELOG.md
pyproject.toml
src/azwerks_nvim_shell/__init__.py
src/azwerks_nvim_shell/main.py
src/azwerks_nvim_shell/app.py
src/azwerks_nvim_shell/cli.py
src/azwerks_nvim_shell/config.py
src/azwerks_nvim_shell/radium.py
data/com.azwerks.NvimShell.desktop
data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
scripts/dev-run.sh
scripts/install-user.sh
scripts/uninstall-user.sh
tests/smoke.sh
tests/test_install_scripts.sh
```

Expected documentation files:

```text id="oy3w11"
docs/architecture.md
docs/implementation-plan.md
docs/dependency-notes.md
docs/argument-parsing-rules.md
docs/desktop-integration.md
docs/install-uninstall-safety.md
docs/gtk-vte-api-probe.md
docs/child-lifecycle-research.md
docs/child-lifecycle-behavior.md
docs/runtime-diagnostics.md
docs/glib-waitid-warning-investigation.md
docs/packaging-readiness.md
```

Run:

```zsh id="frw7pg"
find . -maxdepth 5 -type f | sort
```

Record missing or unexpected files.

---

## Part 2 — Version Consistency Audit

Check version consistency across:

```text id="82ujgp"
pyproject.toml
src/azwerks_nvim_shell/__init__.py
src/azwerks_nvim_shell/config.py
CHANGELOG.md
README.md
docs/
```

Run:

```zsh id="qzxvo8"
command grep -RIn "0\\.1\\.0\\|version\\|VERSION" \
  pyproject.toml README.md CHANGELOG.md src docs 2>/dev/null || true
```

Expected version:

```text id="iicw0f"
0.1.0
```

Flag mismatches.

---

## Part 3 — Naming / Identity Audit

Check app identity consistency.

Expected identifiers:

```text id="hg3986"
Executable: azwerks-nvim-shell
Application ID: com.azwerks.NvimShell
Desktop file: com.azwerks.NvimShell.desktop
Icon name: com.azwerks.NvimShell
Visible app name: azwerks Neovim or current documented equivalent
```

Run:

```zsh id="uqv8z6"
command grep -RIn "AZWERKS\\|azwerks\\|com.azwerks.NvimShell\\|azwerks-nvim-shell" \
  README.md CHANGELOG.md pyproject.toml src data docs scripts tests 2>/dev/null || true
```

Important:

```text id="pcqtk1"
Do not perform a broad rename in this audit.
Only flag inconsistent naming.
If uppercase legacy strings are present, report where they appear and whether they affect runtime behavior.
```

---

## Part 4 — Python / Unit Test Regression

Run:

```zsh id="yp06nu"
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

Record:

```text id="eolelk"
number of tests run
whether tests passed
any failures/errors
```

---

## Part 5 — Smoke / Script Regression

Run:

```zsh id="kkyg31"
tests/test_install_scripts.sh
tests/smoke.sh
```

Record results.

Confirm smoke tests do **not** open GUI windows and do **not** spawn Neovim.

Inspect:

```zsh id="y9fki8"
sed -n '1,240p' tests/smoke.sh
sed -n '1,260p' tests/test_install_scripts.sh
```

Flag any unsafe behavior.

---

## Part 6 — Desktop Entry Audit

Validate project desktop file:

```zsh id="vknnhc"
desktop-file-validate data/com.azwerks.NvimShell.desktop
```

If an installed desktop file exists, validate it:

```zsh id="v205me"
if test -f ~/.local/share/applications/com.azwerks.NvimShell.desktop; then
  desktop-file-validate ~/.local/share/applications/com.azwerks.NvimShell.desktop
fi
```

Inspect desktop file content:

```zsh id="zs0bfd"
sed -n '1,160p' data/com.azwerks.NvimShell.desktop
```

Check:

```text id="3sgpt9"
Type=Application
Name is correct
Exec points to azwerks-nvim-shell %F
Icon points to com.azwerks.NvimShell
Terminal=false
Categories validate
MimeType is reasonable
```

Do not change categories unless the validator fails or a prior documented warning has a clear safe cleanup.

---

## Part 7 — Icon Audit

Check project icon:

```zsh id="szn9ly"
test -s data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
command grep -q "<svg" data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

If installed icon exists:

```zsh id="7f7ca7"
if test -f ~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg; then
  test -s ~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
  command grep -q "<svg" ~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
fi
```

Do not redesign the icon.

Flag only if:

```text id="pbfju6"
missing
empty
invalid SVG
wrong filename
wrong install target
```

---

## Part 8 — Install Script Safety Audit

Inspect install/uninstall scripts:

```zsh id="f9gxdm"
sed -n '1,320p' scripts/install-user.sh
sed -n '1,360p' scripts/uninstall-user.sh
```

Search for unsafe operations:

```zsh id="d4txpq"
command grep -RIn "sudo\\|/usr\\|/etc\\|rm -rf /\\|rm -rf \\$HOME\\|\\.config/nvim\\|\\.local/bin/nvim\\|nvim-linux-x86_64" \
  scripts tests docs README.md 2>/dev/null || true
```

Run non-destructive checks:

```zsh id="xztnwg"
scripts/install-user.sh --dry-run
scripts/install-user.sh --validate-only
scripts/uninstall-user.sh --dry-run
```

Verify:

```text id="qdb6mw"
no sudo
no system writes
only user-local app-owned targets
dry-run changes nothing
validate-only changes nothing
uninstall dry-run is safe
known Neovim paths are protected
```

---

## Part 9 — Installed App Audit

If installed files exist, audit them.

Check:

```zsh id="fitbn1"
test -x ~/.local/bin/azwerks-nvim-shell && echo "installed wrapper exists" || true
test -f ~/.local/share/applications/com.azwerks.NvimShell.desktop && echo "installed desktop file exists" || true
test -f ~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg && echo "installed icon exists" || true
test -d ~/.local/share/azwerks-nvim-shell && echo "installed app dir exists" || true
```

If wrapper exists:

```zsh id="nk5sfr"
~/.local/bin/azwerks-nvim-shell --help
~/.local/bin/azwerks-nvim-shell --version
```

If installed desktop file exists:

```zsh id="odx13p"
desktop-file-validate ~/.local/share/applications/com.azwerks.NvimShell.desktop
```

Do not run real uninstall unless explicitly chosen for this audit and preceded by dry-run.

---

## Part 10 — Optional Manual gtk-launch Visual Confirmation

This section is optional but recommended if a graphical desktop session is available.

Check:

```zsh id="pxbqba"
echo "${DISPLAY:-}"
echo "${WAYLAND_DISPLAY:-}"
```

If neither is set, skip and document:

```text id="i28u8a"
Manual gtk-launch visual confirmation skipped: no graphical session detected.
```

If a graphical session is available and the user wants explicit visual confirmation, run:

```zsh id="h4oftc"
gtk-launch com.azwerks.NvimShell
```

This opens the app.

Manual checklist:

```text id="ywh5ug"
Launcher opens the app.
Window title is correct or acceptable.
App icon appears if the desktop environment exposes it.
Neovim appears inside the VTE terminal.
Radium visual defaults are visible or acceptable.
Exiting Neovim closes the app cleanly.
GTK theme parser warnings, if seen, are external desktop theme warnings.
No app traceback appears.
```

Do not claim success unless this was actually tested.

Record whether this was:

```text id="n5wmhh"
tested and passed
tested and failed
skipped by choice
skipped because no graphical session was available
```

---

## Part 11 — Documentation Truth Audit

Review documentation for claims that no longer match implementation.

Inspect:

```zsh id="99tylx"
sed -n '1,260p' README.md
sed -n '1,220p' CHANGELOG.md

find docs -maxdepth 1 -type f | sort | while read -r file; do
  printf '\n===== %s =====\n' "$file"
  sed -n '1,220p' "$file"
done
```

Flag documentation that incorrectly claims:

```text id="flyrn1"
distribution packaging exists
gtk-launch visual confirmation passed when it did not
real uninstall was run when it was not
GTK theme warnings are app CSS bugs
Neovim config was modified
nvim --embed is used
external UI protocol is implemented
child lifecycle is unverified if it was actually verified
GLib waitid warning was fixed if it still appears
```

Apply only factual documentation fixes if needed.

---

## Part 12 — Release Readiness Verdict

Use one of:

```text id="c3f7u6"
PASS
PASS WITH MINOR FINDINGS
PATCH REQUIRED
FAIL
```

Definitions:

```text id="jxe3lp"
PASS
All tests pass, install safety is verified, docs are truthful, no blocking issues.

PASS WITH MINOR FINDINGS
All core behavior works, but small documentation/manual-check caveats remain.

PATCH REQUIRED
A fix is needed before v0.1 should be considered stable, but project is not fundamentally broken.

FAIL
Core behavior, install safety, or documentation truth is broken.
```

---

## Final Report Format

Produce:

```markdown id="ygjeq7"
# azwerks Neovim Shell v0.1 Final Regression Audit + Release-Readiness Review

## 1. Scope

## 2. Method

State whether this was:
- static only
- static + script-assisted
- manual GUI tested

## 3. Source Checked

Include:
- project path
- version
- key files present/missing

## 4. Executive Verdict

Use:
- PASS
- PASS WITH MINOR FINDINGS
- PATCH REQUIRED
- FAIL

## 5. Findings Summary Table

| ID | Severity | Area | Finding | Patch Required |
|---|---|---|---|---|

Severity levels:
- S0 Critical
- S1 High
- S2 Medium
- S3 Low
- S4 Documentation / Cosmetic

## 6. Detailed Findings

For each finding:

### [ID] Finding title

Severity:
Area:
Evidence:
Why it matters:
Recommended fix:

## 7. Test Results

Include:
- py_compile
- unittest
- install script tests
- smoke test
- desktop-file-validate
- wrapper --help / --version if installed

## 8. Install / Uninstall Safety Review

## 9. Desktop Entry / Icon Review

## 10. Runtime / Lifecycle Review

## 11. Optional Manual gtk-launch Visual Confirmation

State clearly whether it was tested or skipped.

## 12. Documentation Truth Review

## 13. Known Limitations Accepted for v0.1

## 14. Release Readiness Decision

## 15. Recommended Next Step

If PASS or PASS WITH MINOR FINDINGS:
recommend tagging or archiving v0.1.

If PATCH REQUIRED or FAIL:
recommend a focused patch prompt.
```

---

## Done When

This phase is complete when:

```text id="f2fqdg"
all audit commands have been run or explicitly skipped with reason
test results are recorded
desktop entry is validated
icon is validated
install/uninstall safety is reviewed
installed wrapper is checked if present
manual gtk-launch is tested or explicitly skipped
docs are checked against implementation
final verdict is given
next step is recommended
no system paths are modified
Neovim config is untouched
Neovim binary is untouched
```
