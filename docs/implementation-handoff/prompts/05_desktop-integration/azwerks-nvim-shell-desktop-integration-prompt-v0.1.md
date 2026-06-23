# Codex Prompt — AZWERKS Neovim Shell Phase 5: User-Local Desktop Integration

## Goal

Implement **Phase 5 desktop integration** for **AZWERKS Neovim Shell v0.1**.

This phase must add safe user-local install/uninstall behavior for:

```text id="s8v8hj"
azwerks-nvim-shell executable wrapper
desktop entry
application icon
launcher validation
```

This phase must **not** touch system paths.

This phase must **not** use sudo.

This phase must **not** modify Neovim config.

This phase must **not** implement child-exit lifecycle behavior.

This phase must **not** change GTK/VTE runtime behavior except where needed to make installed launching work.

---

## Previous Phase Status

Phase 4 completed GTK/VTE spawn integration.

Known current limitations:

```text id="jdq7xr"
No child-exit lifecycle behavior yet.
Desktop install behavior is placeholder-only.
GTK theme warnings are external theme CSS warnings, not app CSS.
```

Do not address child-exit lifecycle in this phase.

Do not attempt to fix external GTK theme CSS warnings.

Focus only on user-local desktop integration.

---

## Working Directory

Work only inside:

```text id="kx8kus"
/media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
```

Start with:

```zsh id="t2xnqi"
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
pwd
find . -maxdepth 4 -type f | sort
```

---

## Required Preflight

Before making changes, run:

```zsh id="env2w9"
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/smoke.sh
```

If preflight fails, stop and report that the previous phase must be repaired first.

---

## Scope

Allowed files to modify:

```text id="zqww14"
scripts/install-user.sh
scripts/uninstall-user.sh
scripts/dev-run.sh
data/com.azwerks.NvimShell.desktop
data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
README.md
CHANGELOG.md
docs/desktop-integration.md
docs/implementation-plan.md
tests/smoke.sh
```

Allowed files to create:

```text id="xi4orj"
docs/install-uninstall-safety.md
tests/test_install_scripts.sh
```

Do not modify unless strictly necessary:

```text id="f0ko8v"
src/azwerks_nvim_shell/main.py
src/azwerks_nvim_shell/app.py
src/azwerks_nvim_shell/cli.py
src/azwerks_nvim_shell/config.py
src/azwerks_nvim_shell/radium.py
```

Do not modify:

```text id="yipjb6"
/home/blndsft/.config/nvim
/home/blndsft/.local/bin/nvim
/home/blndsft/.local/opt/nvim-linux-x86_64
/usr
/usr/local
/etc
```

---

## Install Targets

The real user-local install script should install only these app-owned targets:

```text id="tqgau0"
~/.local/bin/azwerks-nvim-shell
~/.local/share/azwerks-nvim-shell/
~/.local/share/applications/com.azwerks.NvimShell.desktop
~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

The installed app source should live under:

```text id="9xhvdu"
~/.local/share/azwerks-nvim-shell/app
```

The wrapper executable should live at:

```text id="c81ixc"
~/.local/bin/azwerks-nvim-shell
```

The wrapper should launch the installed app using Python and preserve all arguments.

Expected wrapper behavior:

```zsh id="mwq2ti"
azwerks-nvim-shell
azwerks-nvim-shell --help
azwerks-nvim-shell --version
azwerks-nvim-shell /path/to/file
azwerks-nvim-shell --cwd /path/to/project
```

---

## Install Script Requirements

Implement:

```text id="cjx1f0"
scripts/install-user.sh
```

Required script properties:

```text id="tus5ik"
zsh script
set -euo pipefail
no sudo
no writes to /usr
no writes to /etc
no writes to system application directories
safe handling for paths with spaces
clear stdout status messages
clear stderr errors
non-zero exit on failure
```

The script must:

```text id="x9dc5b"
resolve project root relative to the script location
create user-local target directories
copy src/ into ~/.local/share/azwerks-nvim-shell/app/src/
copy pyproject.toml if needed for metadata/reference
copy README.md and CHANGELOG.md into the installed app directory
copy data/com.azwerks.NvimShell.desktop into ~/.local/share/applications/
copy icon SVG into ~/.local/share/icons/hicolor/scalable/apps/
create ~/.local/bin/azwerks-nvim-shell wrapper
make wrapper executable
validate the installed desktop file if desktop-file-validate exists
refresh desktop database if update-desktop-database exists
refresh icon cache if gtk-update-icon-cache exists
write an install manifest
```

The install manifest should be:

```text id="wg13rg"
~/.local/share/azwerks-nvim-shell/install-manifest.txt
```

It should list every file or directory installed by this app.

Do not include unrelated files.

---

## Wrapper Requirements

The installed wrapper at:

```text id="eqjznx"
~/.local/bin/azwerks-nvim-shell
```

must:

```text id="ykcbx9"
use zsh
use set -euo pipefail
set PYTHONPATH to the installed app src path
execute python3 -m azwerks_nvim_shell.main "$@"
preserve all arguments exactly
work with file paths containing spaces
```

Example wrapper shape:

```zsh id="t1boqb"
#!/usr/bin/env zsh
set -euo pipefail

APP_SRC="$HOME/.local/share/azwerks-nvim-shell/app/src"
PYTHONPATH="$APP_SRC" exec python3 -m azwerks_nvim_shell.main "$@"
```

Only use this exact structure if it matches the final installed layout.

---

## Desktop File Requirements

Update:

```text id="ksplhe"
data/com.azwerks.NvimShell.desktop
```

Required content:

```ini id="xcefd9"
[Desktop Entry]
Type=Application
Name=AZWERKS Neovim
GenericName=Text Editor
Comment=Launch Neovim inside the AZWERKS Neovim Shell
Exec=azwerks-nvim-shell %F
Icon=com.azwerks.NvimShell
Terminal=false
Categories=Utility;TextEditor;Development;
StartupNotify=true
MimeType=text/plain;text/markdown;
```

Validate with:

```zsh id="vatp7h"
desktop-file-validate data/com.azwerks.NvimShell.desktop
```

If the validator emits a non-fatal hint about multiple main categories, record it. Do not treat it as fatal unless validation exits non-zero.

If the desktop file is changed to reduce the hint, explain the change and validate again.

Do not claim launcher integration works unless the desktop file validates and the installed wrapper exists.

---

## Icon Requirements

Ensure this file exists and is valid SVG:

```text id="obgzws"
data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

Rules:

```text id="7dcf8i"
must be original
must not copy the official Neovim logo
must not embed raster images
must use valid SVG XML
must stay visually simple
```

Allowed colors:

```text id="7q1a83"
#202521
#23282b
#ddecc4
#ceda4a
#94a87a
```

Add a simple validation check in the smoke test or install script:

```zsh id="fo7ox6"
test -s data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
command grep -q "<svg" data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

Use `command grep`, not bare `grep`.

---

## Uninstall Script Requirements

Implement:

```text id="zv7t3b"
scripts/uninstall-user.sh
```

Required script properties:

```text id="13ddwm"
zsh script
set -euo pipefail
no sudo
remove only app-owned files
clear stdout status messages
clear stderr errors
safe if files are already missing
non-zero exit only for real failures
```

The uninstall script may remove:

```text id="3r9r89"
~/.local/bin/azwerks-nvim-shell
~/.local/share/applications/com.azwerks.NvimShell.desktop
~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
~/.local/share/azwerks-nvim-shell/
```

The uninstall script must never remove:

```text id="1sjlt5"
~/.config/nvim
~/.local/bin/nvim
~/.local/opt/nvim-linux-x86_64
/usr
/usr/local
/etc
```

The uninstall script should use the install manifest if it exists, but it must defensively refuse unsafe paths.

Unsafe paths include:

```text id="i7786u"
/usr
/usr/local
/etc
/
/home
/home/blndsft
~/.config
~/.local
~/.local/bin
~/.local/share
```

It may delete only exact known app-owned files/directories.

---

## Dry-Run Support

Both install and uninstall scripts must support:

```zsh id="lbnwts"
--dry-run
```

Dry run must print what would happen but make no filesystem changes.

Examples:

```zsh id="fc46g9"
scripts/install-user.sh --dry-run
scripts/uninstall-user.sh --dry-run
```

Do not skip dry-run support.

---

## Validation Mode

Install script must support:

```zsh id="9o68l9"
--validate-only
```

This should verify:

```text id="3wqapz"
source files exist
desktop file validates if desktop-file-validate exists
icon file exists and appears to be SVG
wrapper would be generated from valid paths
target directories are user-local
```

It must not install files.

---

## Script Test Requirements

Create:

```text id="n3057c"
tests/test_install_scripts.sh
```

It must test:

```text id="d8utke"
install-user.sh --dry-run
install-user.sh --validate-only
uninstall-user.sh --dry-run
scripts are executable
desktop file validates if validator exists
icon file exists
icon contains <svg
wrapper generation logic is present
scripts do not contain sudo
scripts do not write to /usr
```

Use zsh.

Use `command grep` instead of bare `grep`.

Do not run a destructive uninstall against the real home directory in tests.

Do not install files in tests unless the test uses a temporary redirected HOME or project-local fake home.

If adding redirected HOME support for tests, document it clearly.

---

## Smoke Test Update

Update:

```text id="av3bsu"
tests/smoke.sh
```

It must run:

```zsh id="w6rcm8"
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install_scripts.sh
```

It should keep the existing non-GUI GTK/VTE import probe.

It should keep desktop-file validation if available.

Do not make smoke tests launch the GUI.

Do not make smoke tests spawn Neovim.

---

## Manual Install Validation

After implementation, run non-destructive checks first:

```zsh id="96fi5k"
scripts/install-user.sh --dry-run
scripts/install-user.sh --validate-only
scripts/uninstall-user.sh --dry-run
tests/smoke.sh
```

Only if those pass, run the real user-local install:

```zsh id="zl1hsc"
scripts/install-user.sh
```

Then validate:

```zsh id="miowtu"
test -x ~/.local/bin/azwerks-nvim-shell
~/.local/bin/azwerks-nvim-shell --help
~/.local/bin/azwerks-nvim-shell --version
desktop-file-validate ~/.local/share/applications/com.azwerks.NvimShell.desktop
test -s ~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

Do not run `gtk-launch` unless a GUI launch test is intentionally desired.

If running `gtk-launch`, say clearly that it opens the app:

```zsh id="qmr9i4"
gtk-launch com.azwerks.NvimShell
```

Do not claim launcher GUI success unless actually tested.

---

## Documentation Updates

Update:

```text id="yyy6mu"
README.md
docs/desktop-integration.md
docs/install-uninstall-safety.md
docs/implementation-plan.md
CHANGELOG.md
```

Document:

```text id="wj4dk7"
install targets
uninstall targets
dry-run behavior
validate-only behavior
desktop file validation
icon installation
known limitations
```

Known limitations must still include:

```text id="kucmjk"
No child-exit lifecycle behavior yet.
GTK theme warnings are external theme CSS warnings, not app CSS.
```

Do not remove those limitations unless actually fixed and verified.

---

## Validation Commands

Run:

```zsh id="ap8w29"
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell

python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/test_install_scripts.sh
tests/smoke.sh

scripts/install-user.sh --dry-run
scripts/install-user.sh --validate-only
scripts/uninstall-user.sh --dry-run
```

If and only if all non-destructive checks pass, run:

```zsh id="qj12se"
scripts/install-user.sh
```

Then validate installed files:

```zsh id="c20g18"
test -x ~/.local/bin/azwerks-nvim-shell
~/.local/bin/azwerks-nvim-shell --help
~/.local/bin/azwerks-nvim-shell --version
desktop-file-validate ~/.local/share/applications/com.azwerks.NvimShell.desktop
test -s ~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

Do not run real uninstall unless explicitly intended.

If uninstall is tested, first run:

```zsh id="rqtvql"
scripts/uninstall-user.sh --dry-run
```

Then run real uninstall only if the installed files are confirmed app-owned.

---

## Hard Constraints

Do not:

```text id="uejolr"
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
run destructive uninstall without dry-run first
open GUI windows in automated tests
spawn Neovim in automated tests
implement child-exit lifecycle
attempt to fix external GTK theme warnings
```

---

## Done When

This phase is complete when:

```text id="ngseqv"
install-user.sh is implemented
uninstall-user.sh is implemented
both support --dry-run
install-user.sh supports --validate-only
desktop file validates
icon exists and is valid SVG
user-local wrapper generation works
non-destructive script tests pass
smoke test passes
real install works if executed
installed wrapper supports --help
installed wrapper supports --version
README documents install/uninstall
desktop integration docs are updated
CHANGELOG is updated truthfully
no system paths were modified
no Neovim config was modified
```

---

## Final Report Format

When finished, report:

```markdown id="cw4e0f"
# AZWERKS Neovim Shell Phase 5 Report — User-Local Desktop Integration

## Summary

## Preflight Result

## Files Changed

## Install Behavior

## Uninstall Behavior

## Dry-Run / Validate-Only Behavior

## Desktop Entry Validation

## Icon Validation

## Wrapper Validation

## Tests Run

## Real Install Result

## Real Uninstall Result

## Known Limitations

## What Was Not Done

## Next Recommended Prompt
```

