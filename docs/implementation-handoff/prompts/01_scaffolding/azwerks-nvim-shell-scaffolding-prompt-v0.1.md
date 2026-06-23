
# Codex Prompt — AZWERKS Neovim Shell v0.1 Scaffolding Pass

## Goal

Create the initial project scaffolding for **AZWERKS Neovim Shell** under this exact path:

```text
/media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
```

This is a **scaffolding-only pass**.

Do not implement the full application logic yet.

Do not build the GTK/VTE app yet.

Do not install system packages.

Do not modify the existing Neovim config.

Do not modify:

```text
/home/blndsft/.config/nvim
/home/blndsft/.local/bin/nvim
/home/blndsft/.local/opt/nvim-linux-x86_64
```

The purpose of this pass is to create a clean, documented, implementation-ready project structure for the future AZWERKS Neovim Shell build.

---

## Product Definition

Project name:

```text
AZWERKS Neovim Shell
```

Executable name:

```text
azwerks-nvim-shell
```

Version:

```text
0.1.0
```

Application ID:

```text
com.azwerks.NvimShell
```

Desktop file:

```text
com.azwerks.NvimShell.desktop
```

Target purpose:

```text
A native Linux GTK/VTE application shell that launches terminal Neovim with AZWERKS desktop identity and Radium-inspired defaults.
```

Important boundary:

```text
This is not a true Neovim GUI frontend.
This does not use nvim --embed.
This does not implement the Neovim UI protocol.
This is a GTK/VTE wrapper around terminal Neovim.
```

---

## Working Directory

Start by checking the parent folder:

```zsh
cd /media/blndsft/SLP-ARCH-01/azwerks
pwd
ls -la
```

Then create the project folder only if it does not already contain unrelated work:

```text
/media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
```

If the target folder already exists, inspect it first and report its contents before modifying anything.

Do not delete an existing folder.

Do not overwrite existing non-placeholder files without reporting first.

---

## Required Scaffolding

Create this structure:

```text
azwerks-nvim-shell/
├── README.md
├── CHANGELOG.md
├── LICENSE.md
├── pyproject.toml
├── .gitignore
├── docs/
│   ├── architecture.md
│   ├── implementation-plan.md
│   ├── dependency-notes.md
│   ├── argument-parsing-rules.md
│   ├── desktop-integration.md
│   └── radium-visual-defaults.md
├── src/
│   └── azwerks_nvim_shell/
│       ├── __init__.py
│       ├── main.py
│       ├── app.py
│       ├── config.py
│       └── radium.py
├── data/
│   ├── com.azwerks.NvimShell.desktop
│   └── icons/
│       └── hicolor/
│           └── scalable/
│               └── apps/
│                   └── com.azwerks.NvimShell.svg
├── scripts/
│   ├── dev-run.sh
│   ├── install-user.sh
│   └── uninstall-user.sh
└── tests/
    └── smoke.sh
```

---

## File Content Requirements

### `README.md`

Create a clear README with these sections:

```markdown
# AZWERKS Neovim Shell

## Purpose

## What This Is

## What This Is Not

## Target Platform

## Expected Neovim Path

## Dependencies

## Development Run

## User Install

## User Uninstall

## Known Limitations

## Project Status
```

The README must explicitly state:

```text
AZWERKS Neovim Shell is a GTK/VTE wrapper around terminal Neovim.
It is not a true Neovim GUI frontend.
It does not use nvim --embed.
It does not implement the Neovim UI protocol.
It does not modify the user's Neovim config.
```

---

### `CHANGELOG.md`

Create:

```markdown
# Changelog

## 0.1.0

- Created initial project scaffolding.
- Added source package structure.
- Added documentation placeholders.
- Added desktop-entry placeholder.
- Added user-local install/uninstall script placeholders.
- Added smoke-test placeholder.
```

---

### `LICENSE.md`

Create a placeholder license file with this text:

```markdown
# License

License not selected yet.

This project is currently private/internal unless a license is explicitly added.
```

Do not invent a license.

---

### `.gitignore`

Create a Python/GTK-friendly `.gitignore`:

```gitignore
__pycache__/
*.py[cod]
*.pyo
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.venv/
venv/
dist/
build/
*.log
.DS_Store
.cache/
```

---

### `pyproject.toml`

Create a minimal packaging placeholder.

It should define:

```toml
[project]
name = "azwerks-nvim-shell"
version = "0.1.0"
description = "A native Linux GTK/VTE application shell for launching terminal Neovim with AZWERKS desktop identity."
readme = "README.md"
requires-python = ">=3.10"

[project.scripts]
azwerks-nvim-shell = "azwerks_nvim_shell.main:main"
```

Do not add dependency claims that may be wrong.

Do not add package dependencies for GTK/VTE through pip unless verified. GTK/VTE should be documented as system dependencies.

---

## Source File Placeholders

### `src/azwerks_nvim_shell/__init__.py`

Create:

```python
"""AZWERKS Neovim Shell."""

__version__ = "0.1.0"
```

---

### `src/azwerks_nvim_shell/main.py`

Create a placeholder CLI entry point.

It should include:

```python
def main() -> int:
    """CLI entry point placeholder."""
    print("AZWERKS Neovim Shell scaffolding placeholder.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Do not implement full argument parsing yet.

---

### `src/azwerks_nvim_shell/app.py`

Create a placeholder with a module docstring explaining that this file will contain GTK application/window logic.

Do not implement GTK yet.

---

### `src/azwerks_nvim_shell/config.py`

Create a placeholder with constants:

```python
APP_ID = "com.azwerks.NvimShell"
APP_NAME = "AZWERKS Neovim"
EXECUTABLE_NAME = "azwerks-nvim-shell"
DEFAULT_NVIM_PATH = "/home/blndsft/.local/bin/nvim"
VERSION = "0.1.0"
```

Do not implement detection logic yet.

---

### `src/azwerks_nvim_shell/radium.py`

Create a placeholder with Radium color constants:

```python
RADIUM_BACKGROUND = "#202521"
RADIUM_FOREGROUND = "#ddecc4"
RADIUM_SURFACE = "#23282b"
RADIUM_ACCENT = "#ceda4a"
RADIUM_MUTED = "#94a87a"
RADIUM_FAINT = "#8e9290"
```

Do not implement GTK color application yet.

---

## Documentation Files

### `docs/architecture.md`

Include:

```markdown
# Architecture

AZWERKS Neovim Shell v0.1 is planned as a GTK/VTE wrapper.

It will launch terminal Neovim inside a VTE terminal widget.

It will not implement Neovim's external UI protocol in v0.1.
```

Add an architecture diagram in text:

```text
AZWERKS Neovim Shell
  └── GTK Application Window
      └── VTE Terminal Widget
          └── nvim
```

---

### `docs/implementation-plan.md`

Create a phased plan:

```markdown
# Implementation Plan

## Phase 0 — Scaffolding

## Phase 1 — CLI Parsing

## Phase 2 — GTK/VTE Window

## Phase 3 — Desktop Integration

## Phase 4 — Radium Visual Defaults

## Phase 5 — Smoke Tests

## Phase 6 — Hardening
```

---

### `docs/dependency-notes.md`

Document expected system dependencies but do not install them:

````markdown
# Dependency Notes

Expected Linux Mint / Ubuntu-style packages:

```zsh
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-vte-3.91 desktop-file-utils
````

These should be verified before implementation.

Do not install dependencies automatically from this project.

````

---

### `docs/argument-parsing-rules.md`

Create a document containing the locked argument parsing rules.

Include this summary:

```markdown
# Argument Parsing Rules

## Overview

- Arguments are processed strictly left-to-right.
- Flags and positional arguments may be interleaved.
- Later occurrences of the same flag override earlier ones.
- Flags that require values consume the next token.

## Early Exit Flags

- `--help` and `--version` have absolute precedence.
- They immediately stop parsing.
- They print output and exit without launching GTK or Neovim.

## Supported Flags

- `--help`
- `--version`
- `--cwd <path>`
- `--nvim-bin <path>`

## Working Directory Resolution

1. Use `--cwd` if provided.
2. Else if exactly one positional argument is a directory, use it.
3. Else use the current process working directory.
4. If multiple directory arguments exist, do not infer cwd.

## Neovim Invocation

- Final argv is `[nvim_binary, *positional_args]`.
- Do not pass `--cwd` to Neovim.
- Set working directory through the process spawn call.

## Error Handling

- Missing values produce: `error: missing value for flag '<flag>'`
- Unknown flags produce: `error: unknown flag '<flag>'`
- Invalid nvim binary path produces: `error: invalid nvim binary path '<path>'`
- Invalid working directory produces: `error: invalid working directory '<path>'`
- CLI errors print to stderr, exit non-zero, and do not launch GTK or Neovim.
````

---

### `docs/desktop-integration.md`

Document the planned desktop integration:

````markdown
# Desktop Integration

The app should install a user-local desktop entry to:

```text
~/.local/share/applications/com.azwerks.NvimShell.desktop
````

The app icon should install to:

```text
~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

The executable should be available as:

```text
~/.local/bin/azwerks-nvim-shell
```

The desktop entry must use:

```ini
Terminal=false
Exec=azwerks-nvim-shell %F
Icon=com.azwerks.NvimShell
```

````

---

### `docs/radium-visual-defaults.md`

Document the Radium visual defaults:

```markdown
# Radium Visual Defaults

Planned terminal shell defaults:

| Role | Hex |
|---|---|
| Background | `#202521` |
| Foreground | `#ddecc4` |
| Surface | `#23282b` |
| Accent | `#ceda4a` |
| Muted | `#94a87a` |
| Faint | `#8e9290` |

No glow, CRT, scanlines, cyberpunk styling, or decorative terminal cosplay.
````

---

## Desktop File Placeholder

Create:

```text
data/com.azwerks.NvimShell.desktop
```

With:

```ini
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

Do not claim it is installed yet.

---

## Icon Placeholder

Create:

```text
data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

Use a simple valid SVG placeholder.

It should not copy the official Neovim logo.

It should be original and minimal.

Use AZWERKS/Radium-inspired colors:

```text
#202521
#ddecc4
#ceda4a
```

Keep it simple: a dark square/circle/surface with a small abstract terminal/editor mark is enough.

---

## Script Placeholders

### `scripts/dev-run.sh`

Create an executable script:

```zsh
#!/usr/bin/env zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHONPATH="$ROOT_DIR/src" python3 -m azwerks_nvim_shell.main "$@"
```

---

### `scripts/install-user.sh`

Create an executable placeholder script that prints what it would install.

Do not perform a full install yet unless all referenced files exist.

It may create directories, but it must not use sudo.

Expected user-local paths:

```text
~/.local/bin/azwerks-nvim-shell
~/.local/share/applications/com.azwerks.NvimShell.desktop
~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

---

### `scripts/uninstall-user.sh`

Create an executable placeholder script that prints what it would remove.

It must clearly refuse to remove:

```text
~/.config/nvim
~/.local/bin/nvim
~/.local/opt/nvim-linux-x86_64
```

---

## Test Placeholder

Create:

```text
tests/smoke.sh
```

It should be executable and run basic scaffolding checks:

```zsh
#!/usr/bin/env zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

python3 -m py_compile "$ROOT_DIR"/src/azwerks_nvim_shell/*.py

if command -v desktop-file-validate >/dev/null; then
  desktop-file-validate "$ROOT_DIR/data/com.azwerks.NvimShell.desktop"
else
  echo "desktop-file-validate not found; skipping desktop validation"
fi

test -x "$ROOT_DIR/scripts/dev-run.sh"
test -x "$ROOT_DIR/scripts/install-user.sh"
test -x "$ROOT_DIR/scripts/uninstall-user.sh"

echo "Scaffolding smoke test passed."
```

---

## Permissions

Make these files executable:

```text
scripts/dev-run.sh
scripts/install-user.sh
scripts/uninstall-user.sh
tests/smoke.sh
```

---

## Validation Commands

After creating the scaffold, run:

```zsh
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
find . -maxdepth 4 -type f | sort
python3 -m py_compile src/azwerks_nvim_shell/*.py
tests/smoke.sh
```

If `desktop-file-validate` exists, the smoke test should validate the desktop file.

---

## Constraints

Do not:

```text
implement the full GTK app yet
implement VTE spawning yet
implement full CLI parsing yet
install anything with apt
use sudo
modify the user's Neovim config
modify the user's Neovim binary
modify Black Box
modify system terminal alternatives
create files outside /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell except through placeholder install scripts
```

This pass is only about project shape, documentation, placeholders, and validation.

---

## Done When

The task is complete when:

```text
the target project folder exists
all scaffold files exist
all placeholder docs exist
all executable scripts are executable
Python placeholder files compile
desktop file validates if desktop-file-validate is installed
tests/smoke.sh passes
no external system files were modified
no Neovim config files were modified
```

---

## Final Report Format

When done, report:

```markdown
# AZWERKS Neovim Shell Scaffolding Report

## Summary

## Target Path

## Files Created

## Commands Run

## Validation Results

## Files Not Created / Skipped

## Notes / Risks

## Next Step
```
# Codex Prompt — AZWERKS Neovim Shell v0.1 Scaffolding Pass

## Goal

Create the initial project scaffolding for **AZWERKS Neovim Shell** under this exact path:

```text
/media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
```

This is a **scaffolding-only pass**.

Do not implement the full application logic yet.

Do not build the GTK/VTE app yet.

Do not install system packages.

Do not modify the existing Neovim config.

Do not modify:

```text
/home/blndsft/.config/nvim
/home/blndsft/.local/bin/nvim
/home/blndsft/.local/opt/nvim-linux-x86_64
```

The purpose of this pass is to create a clean, documented, implementation-ready project structure for the future AZWERKS Neovim Shell build.

---

## Product Definition

Project name:

```text
AZWERKS Neovim Shell
```

Executable name:

```text
azwerks-nvim-shell
```

Version:

```text
0.1.0
```

Application ID:

```text
com.azwerks.NvimShell
```

Desktop file:

```text
com.azwerks.NvimShell.desktop
```

Target purpose:

```text
A native Linux GTK/VTE application shell that launches terminal Neovim with AZWERKS desktop identity and Radium-inspired defaults.
```

Important boundary:

```text
This is not a true Neovim GUI frontend.
This does not use nvim --embed.
This does not implement the Neovim UI protocol.
This is a GTK/VTE wrapper around terminal Neovim.
```

---

## Working Directory

Start by checking the parent folder:

```zsh
cd /media/blndsft/SLP-ARCH-01/azwerks
pwd
ls -la
```

Then create the project folder only if it does not already contain unrelated work:

```text
/media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
```

If the target folder already exists, inspect it first and report its contents before modifying anything.

Do not delete an existing folder.

Do not overwrite existing non-placeholder files without reporting first.

---

## Required Scaffolding

Create this structure:

```text
azwerks-nvim-shell/
├── README.md
├── CHANGELOG.md
├── LICENSE.md
├── pyproject.toml
├── .gitignore
├── docs/
│   ├── architecture.md
│   ├── implementation-plan.md
│   ├── dependency-notes.md
│   ├── argument-parsing-rules.md
│   ├── desktop-integration.md
│   └── radium-visual-defaults.md
├── src/
│   └── azwerks_nvim_shell/
│       ├── __init__.py
│       ├── main.py
│       ├── app.py
│       ├── config.py
│       └── radium.py
├── data/
│   ├── com.azwerks.NvimShell.desktop
│   └── icons/
│       └── hicolor/
│           └── scalable/
│               └── apps/
│                   └── com.azwerks.NvimShell.svg
├── scripts/
│   ├── dev-run.sh
│   ├── install-user.sh
│   └── uninstall-user.sh
└── tests/
    └── smoke.sh
```

---

## File Content Requirements

### `README.md`

Create a clear README with these sections:

```markdown
# AZWERKS Neovim Shell

## Purpose

## What This Is

## What This Is Not

## Target Platform

## Expected Neovim Path

## Dependencies

## Development Run

## User Install

## User Uninstall

## Known Limitations

## Project Status
```

The README must explicitly state:

```text
AZWERKS Neovim Shell is a GTK/VTE wrapper around terminal Neovim.
It is not a true Neovim GUI frontend.
It does not use nvim --embed.
It does not implement the Neovim UI protocol.
It does not modify the user's Neovim config.
```

---

### `CHANGELOG.md`

Create:

```markdown
# Changelog

## 0.1.0

- Created initial project scaffolding.
- Added source package structure.
- Added documentation placeholders.
- Added desktop-entry placeholder.
- Added user-local install/uninstall script placeholders.
- Added smoke-test placeholder.
```

---

### `LICENSE.md`

Create a placeholder license file with this text:

```markdown
# License

License not selected yet.

This project is currently private/internal unless a license is explicitly added.
```

Do not invent a license.

---

### `.gitignore`

Create a Python/GTK-friendly `.gitignore`:

```gitignore
__pycache__/
*.py[cod]
*.pyo
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.venv/
venv/
dist/
build/
*.log
.DS_Store
.cache/
```

---

### `pyproject.toml`

Create a minimal packaging placeholder.

It should define:

```toml
[project]
name = "azwerks-nvim-shell"
version = "0.1.0"
description = "A native Linux GTK/VTE application shell for launching terminal Neovim with AZWERKS desktop identity."
readme = "README.md"
requires-python = ">=3.10"

[project.scripts]
azwerks-nvim-shell = "azwerks_nvim_shell.main:main"
```

Do not add dependency claims that may be wrong.

Do not add package dependencies for GTK/VTE through pip unless verified. GTK/VTE should be documented as system dependencies.

---

## Source File Placeholders

### `src/azwerks_nvim_shell/__init__.py`

Create:

```python
"""AZWERKS Neovim Shell."""

__version__ = "0.1.0"
```

---

### `src/azwerks_nvim_shell/main.py`

Create a placeholder CLI entry point.

It should include:

```python
def main() -> int:
    """CLI entry point placeholder."""
    print("AZWERKS Neovim Shell scaffolding placeholder.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Do not implement full argument parsing yet.

---

### `src/azwerks_nvim_shell/app.py`

Create a placeholder with a module docstring explaining that this file will contain GTK application/window logic.

Do not implement GTK yet.

---

### `src/azwerks_nvim_shell/config.py`

Create a placeholder with constants:

```python
APP_ID = "com.azwerks.NvimShell"
APP_NAME = "AZWERKS Neovim"
EXECUTABLE_NAME = "azwerks-nvim-shell"
DEFAULT_NVIM_PATH = "/home/blndsft/.local/bin/nvim"
VERSION = "0.1.0"
```

Do not implement detection logic yet.

---

### `src/azwerks_nvim_shell/radium.py`

Create a placeholder with Radium color constants:

```python
RADIUM_BACKGROUND = "#202521"
RADIUM_FOREGROUND = "#ddecc4"
RADIUM_SURFACE = "#23282b"
RADIUM_ACCENT = "#ceda4a"
RADIUM_MUTED = "#94a87a"
RADIUM_FAINT = "#8e9290"
```

Do not implement GTK color application yet.

---

## Documentation Files

### `docs/architecture.md`

Include:

```markdown
# Architecture

AZWERKS Neovim Shell v0.1 is planned as a GTK/VTE wrapper.

It will launch terminal Neovim inside a VTE terminal widget.

It will not implement Neovim's external UI protocol in v0.1.
```

Add an architecture diagram in text:

```text
AZWERKS Neovim Shell
  └── GTK Application Window
      └── VTE Terminal Widget
          └── nvim
```

---

### `docs/implementation-plan.md`

Create a phased plan:

```markdown
# Implementation Plan

## Phase 0 — Scaffolding

## Phase 1 — CLI Parsing

## Phase 2 — GTK/VTE Window

## Phase 3 — Desktop Integration

## Phase 4 — Radium Visual Defaults

## Phase 5 — Smoke Tests

## Phase 6 — Hardening
```

---

### `docs/dependency-notes.md`

Document expected system dependencies but do not install them:

````markdown
# Dependency Notes

Expected Linux Mint / Ubuntu-style packages:

```zsh
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-vte-3.91 desktop-file-utils
````

These should be verified before implementation.

Do not install dependencies automatically from this project.

````

---

### `docs/argument-parsing-rules.md`

Create a document containing the locked argument parsing rules.

Include this summary:

```markdown
# Argument Parsing Rules

## Overview

- Arguments are processed strictly left-to-right.
- Flags and positional arguments may be interleaved.
- Later occurrences of the same flag override earlier ones.
- Flags that require values consume the next token.

## Early Exit Flags

- `--help` and `--version` have absolute precedence.
- They immediately stop parsing.
- They print output and exit without launching GTK or Neovim.

## Supported Flags

- `--help`
- `--version`
- `--cwd <path>`
- `--nvim-bin <path>`

## Working Directory Resolution

1. Use `--cwd` if provided.
2. Else if exactly one positional argument is a directory, use it.
3. Else use the current process working directory.
4. If multiple directory arguments exist, do not infer cwd.

## Neovim Invocation

- Final argv is `[nvim_binary, *positional_args]`.
- Do not pass `--cwd` to Neovim.
- Set working directory through the process spawn call.

## Error Handling

- Missing values produce: `error: missing value for flag '<flag>'`
- Unknown flags produce: `error: unknown flag '<flag>'`
- Invalid nvim binary path produces: `error: invalid nvim binary path '<path>'`
- Invalid working directory produces: `error: invalid working directory '<path>'`
- CLI errors print to stderr, exit non-zero, and do not launch GTK or Neovim.
````

---

### `docs/desktop-integration.md`

Document the planned desktop integration:

````markdown
# Desktop Integration

The app should install a user-local desktop entry to:

```text
~/.local/share/applications/com.azwerks.NvimShell.desktop
````

The app icon should install to:

```text
~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

The executable should be available as:

```text
~/.local/bin/azwerks-nvim-shell
```

The desktop entry must use:

```ini
Terminal=false
Exec=azwerks-nvim-shell %F
Icon=com.azwerks.NvimShell
```

````

---

### `docs/radium-visual-defaults.md`

Document the Radium visual defaults:

```markdown
# Radium Visual Defaults

Planned terminal shell defaults:

| Role | Hex |
|---|---|
| Background | `#202521` |
| Foreground | `#ddecc4` |
| Surface | `#23282b` |
| Accent | `#ceda4a` |
| Muted | `#94a87a` |
| Faint | `#8e9290` |

No glow, CRT, scanlines, cyberpunk styling, or decorative terminal cosplay.
````

---

## Desktop File Placeholder

Create:

```text
data/com.azwerks.NvimShell.desktop
```

With:

```ini
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

Do not claim it is installed yet.

---

## Icon Placeholder

Create:

```text
data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

Use a simple valid SVG placeholder.

It should not copy the official Neovim logo.

It should be original and minimal.

Use AZWERKS/Radium-inspired colors:

```text
#202521
#ddecc4
#ceda4a
```

Keep it simple: a dark square/circle/surface with a small abstract terminal/editor mark is enough.

---

## Script Placeholders

### `scripts/dev-run.sh`

Create an executable script:

```zsh
#!/usr/bin/env zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PYTHONPATH="$ROOT_DIR/src" python3 -m azwerks_nvim_shell.main "$@"
```

---

### `scripts/install-user.sh`

Create an executable placeholder script that prints what it would install.

Do not perform a full install yet unless all referenced files exist.

It may create directories, but it must not use sudo.

Expected user-local paths:

```text
~/.local/bin/azwerks-nvim-shell
~/.local/share/applications/com.azwerks.NvimShell.desktop
~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

---

### `scripts/uninstall-user.sh`

Create an executable placeholder script that prints what it would remove.

It must clearly refuse to remove:

```text
~/.config/nvim
~/.local/bin/nvim
~/.local/opt/nvim-linux-x86_64
```

---

## Test Placeholder

Create:

```text
tests/smoke.sh
```

It should be executable and run basic scaffolding checks:

```zsh
#!/usr/bin/env zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

python3 -m py_compile "$ROOT_DIR"/src/azwerks_nvim_shell/*.py

if command -v desktop-file-validate >/dev/null; then
  desktop-file-validate "$ROOT_DIR/data/com.azwerks.NvimShell.desktop"
else
  echo "desktop-file-validate not found; skipping desktop validation"
fi

test -x "$ROOT_DIR/scripts/dev-run.sh"
test -x "$ROOT_DIR/scripts/install-user.sh"
test -x "$ROOT_DIR/scripts/uninstall-user.sh"

echo "Scaffolding smoke test passed."
```

---

## Permissions

Make these files executable:

```text
scripts/dev-run.sh
scripts/install-user.sh
scripts/uninstall-user.sh
tests/smoke.sh
```

---

## Validation Commands

After creating the scaffold, run:

```zsh
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
find . -maxdepth 4 -type f | sort
python3 -m py_compile src/azwerks_nvim_shell/*.py
tests/smoke.sh
```

If `desktop-file-validate` exists, the smoke test should validate the desktop file.

---

## Constraints

Do not:

```text
implement the full GTK app yet
implement VTE spawning yet
implement full CLI parsing yet
install anything with apt
use sudo
modify the user's Neovim config
modify the user's Neovim binary
modify Black Box
modify system terminal alternatives
create files outside /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell except through placeholder install scripts
```

This pass is only about project shape, documentation, placeholders, and validation.

---

## Done When

The task is complete when:

```text
the target project folder exists
all scaffold files exist
all placeholder docs exist
all executable scripts are executable
Python placeholder files compile
desktop file validates if desktop-file-validate is installed
tests/smoke.sh passes
no external system files were modified
no Neovim config files were modified
```

---

## Final Report Format

When done, report:

```markdown
# AZWERKS Neovim Shell Scaffolding Report

## Summary

## Target Path

## Files Created

## Commands Run

## Validation Results

## Files Not Created / Skipped

## Notes / Risks

## Next Step
```
