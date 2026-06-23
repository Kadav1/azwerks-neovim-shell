
# Build Prompt — AZWERKS Neovim Shell v0.1

## Purpose

Build **AZWERKS Neovim Shell v0.1** as a small native Linux desktop shell for launching terminal Neovim inside a GTK/VTE window.

This prompt must be treated as an implementation prompt with a strict documentation gate.

Do not invent API behavior.

Do not assume GTK, VTE, PyGObject, Neovim, or desktop-entry behavior without validating it through the installed environment and relevant documentation.

---

## Core Product Definition

### Project Name

```text
AZWERKS Neovim Shell
```

### Executable Name

```text
azwerks-nvim-shell
```

### Version

```text
0.1.0
```

### Application ID

```text
com.azwerks.NvimShell
```

### Desktop Entry ID

```text
com.azwerks.NvimShell.desktop
```

### Project Root

Work under:

```text
/media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
```

### Product Description

AZWERKS Neovim Shell is a GTK/VTE wrapper around terminal Neovim.

It gives terminal Neovim its own desktop application identity:

```text
custom app name
custom icon
custom .desktop entry
native GTK window
embedded terminal widget
controlled Neovim launch command
controlled working-directory behavior
Radium-inspired terminal defaults where supported
```

---

## Critical Boundary

This project is **not** a true Neovim GUI frontend.

Do not implement:

```text
nvim --embed
nvim_ui_attach()
Neovim UI protocol rendering
MessagePack-RPC client behavior
manual editor-grid rendering
custom Neovim popup/menu/cmdline rendering
```

This app must run normal terminal Neovim inside a terminal widget.

Architecture:

```text
AZWERKS Neovim Shell
  └── GTK Application
      └── GTK Application Window
          └── VTE Terminal Widget
              └── nvim
```

The Neovim process keeps responsibility for:

```text
editing
modes
buffers
plugins
Tree-sitter
LSP
syntax highlighting
terminal UI behavior
user config
```

The shell app is responsible only for:

```text
desktop identity
window creation
terminal widget hosting
safe argument parsing
safe Neovim process launch
user-local desktop integration
basic visual defaults where supported
```

---

## Documentation Gate

Before implementing or changing code, inspect the relevant installed documentation and APIs.

Do not rely only on memory.

At minimum, verify:

```text
PyGObject import pattern for Gtk 4
PyGObject import pattern for Vte 3.91
Gtk.Application availability
Gtk.ApplicationWindow availability
Vte.Terminal availability
the supported Vte.Terminal process-spawn API in the installed version
the supported Vte.Terminal color/font APIs in the installed version
freedesktop desktop-entry syntax for Exec, Icon, Terminal, Categories, MimeType
```

Run an environment/API probe before coding:

```zsh
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell

python3 - <<'PY'
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Vte", "3.91")

from gi.repository import Gtk, Vte, GLib, Gio

print("Gtk.Application:", Gtk.Application)
print("Gtk.ApplicationWindow:", Gtk.ApplicationWindow)
print("Vte.Terminal:", Vte.Terminal)

terminal_methods = dir(Vte.Terminal)
for name in [
    "spawn_async",
    "set_color_foreground",
    "set_color_background",
    "set_color_cursor",
    "set_font",
]:
    print(f"Vte.Terminal.{name}:", name in terminal_methods)
PY
```

Also check packages:

```zsh
dpkg -s python3-gi gir1.2-gtk-4.0 gir1.2-vte-3.91 desktop-file-utils >/dev/null
```

If required GTK/VTE imports fail, stop and report the missing dependency.

Do not silently downgrade to GTK3.

Do not silently switch to another toolkit.

---

## Current Known System Assumptions

The user has Neovim installed outside the Linux Mint package manager.

Expected preferred Neovim path:

```text
/home/blndsft/.local/bin/nvim
```

Existing Neovim config:

```text
/home/blndsft/.config/nvim
```

Do not modify the existing Neovim config.

Do not modify the existing Neovim binary.

---

## Project State Requirement

This build prompt assumes the scaffolding already exists.

Start by checking:

```zsh
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
pwd
find . -maxdepth 4 -type f | sort
```

Expected scaffold files include at least:

```text
README.md
CHANGELOG.md
pyproject.toml
src/azwerks_nvim_shell/main.py
src/azwerks_nvim_shell/app.py
src/azwerks_nvim_shell/config.py
src/azwerks_nvim_shell/radium.py
data/com.azwerks.NvimShell.desktop
scripts/dev-run.sh
scripts/install-user.sh
scripts/uninstall-user.sh
tests/smoke.sh
docs/argument-parsing-rules.md
```

If the scaffold is missing, stop and report that the scaffolding pass must be run first.

---

## Implementation Scope

Implement v0.1 as a working GTK/VTE application.

Allowed files to modify or create:

```text
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
tests/test_cli.py
README.md
CHANGELOG.md
docs/argument-parsing-rules.md
docs/architecture.md
docs/dependency-notes.md
docs/desktop-integration.md
docs/radium-visual-defaults.md
```

Do not modify files outside:

```text
/media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
```

except when the user explicitly runs the install script after review.

---

## CLI Contract

Implement the CLI contract exactly.

### CLI Grammar

```ebnf
command        ::= "azwerks-nvim-shell" { argument }

argument       ::= flag | positional

flag           ::= help_flag
                 | version_flag
                 | cwd_flag
                 | nvim_bin_flag

help_flag      ::= "--help"
version_flag   ::= "--version"

cwd_flag       ::= "--cwd" value
nvim_bin_flag  ::= "--nvim-bin" value

value          ::= token

positional     ::= token

token          ::= any non-empty string not interpreted as a flag
```

### Overview

* Arguments are processed strictly left-to-right.
* Flags and positional arguments may be interleaved.
* Later occurrences of the same flag override earlier ones.
* Flags that require values consume the next token.

### Early Exit Flags

`--help` and `--version`:

* Have absolute precedence.
* Immediately stop parsing when encountered.
* Ignore all other flags and positional arguments.
* Print output and exit without launching GTK or Neovim.

Examples:

```zsh
azwerks-nvim-shell --help
azwerks-nvim-shell file.txt --version
azwerks-nvim-shell --cwd /project --help file.txt
```

### Supported Flags

```text
--help
--version
--cwd <path>
--nvim-bin <path>
```

### `--nvim-bin <path>`

Behavior:

* Overrides binary detection.
* Must be a valid executable path.
* Later occurrences override earlier ones.

Invalid path error format:

```text
error: invalid nvim binary path '<path>'
```

### `--cwd <path>`

Behavior:

* Overrides working directory inference.
* Must exist.
* Must be a directory.
* Later occurrences override earlier ones.

Invalid cwd error format:

```text
error: invalid working directory '<path>'
```

### Missing Flag Values

For flags requiring values:

```text
--cwd
--nvim-bin
```

If the next token is missing or is another flag, report:

```text
error: missing value for flag '<flag>'
```

Examples:

```zsh
azwerks-nvim-shell --cwd
azwerks-nvim-shell --nvim-bin
azwerks-nvim-shell --cwd --nvim-bin /usr/bin/nvim
azwerks-nvim-shell --nvim-bin --cwd /project
```

### Unknown Flags

Unknown flags must error.

Example:

```zsh
azwerks-nvim-shell --foo
```

Expected stderr:

```text
error: unknown flag '--foo'
```

Exit non-zero.

Do not launch GTK or Neovim.

### Positional Arguments

* Non-flag tokens are treated as file or directory paths.
* Order is preserved.
* Shell expressions are not expanded.
* Nonexistent paths are passed through unchanged.
* Paths with spaces remain single arguments if passed as a single shell argument.

### Working Directory Resolution

Resolve working directory in this order:

1. Use `--cwd` if provided.
2. Else if exactly one positional argument is an existing directory, use that directory.
3. Else use the current process working directory.

Important:

* If multiple directory arguments exist, do not infer cwd.
* If mixed file and directory arguments exist, do not infer cwd.
* Nonexistent paths are not directories and must not be used for cwd inference.

### Neovim Invocation Contract

The parser must produce a launch contract containing:

```text
nvim_binary
cwd
positional_args
nvim_argv
```

Final Neovim argv:

```text
[nvim_binary, *positional_args]
```

Do not pass `--cwd` to Neovim.

Set working directory through the later process-spawn call, not through Neovim flags.

---

## Neovim Binary Detection

Use this detection order:

1. `--nvim-bin <path>` if provided and executable.
2. `/home/blndsft/.local/bin/nvim` if executable.
3. `nvim` discovered from `PATH`.

If no executable Neovim binary can be found, print:

```text
error: could not find executable nvim binary
```

Exit non-zero.

Do not install Neovim.

Do not modify PATH.

---

## Application Implementation

### `main.py`

Responsibilities:

```text
entry point
call CLI parser
handle --help
handle --version
handle CLI errors
start GTK app only for valid launch contracts
return correct process exit code
```

Do not let invalid CLI input create a GTK window.

### `cli.py`

Responsibilities:

```text
manual parser or fully verified parser
LaunchContract dataclass
CliError exception
EarlyExit handling
binary detection
cwd resolution
help text
version text
```

Use Python standard library only.

Do not use `shell=True`.

Do not use `os.system()`.

### `app.py`

Responsibilities:

```text
Gtk.Application subclass or functionally equivalent Gtk.Application structure
Gtk.ApplicationWindow creation
Vte.Terminal widget creation
spawn Neovim using validated VTE process-spawn API
close app cleanly when Neovim exits if supported by documented VTE signal/API
surface a clear error if spawn fails
```

Before using any VTE spawn method, confirm the method exists in the installed GI API.

Do not invent the signature.

If the installed API differs from examples, adapt to the installed API and document the difference in the build report.

### `config.py`

Responsibilities:

```text
app constants
default nvim path
version
application id
default window title
default window size
```

Use:

```text
APP_ID = "com.azwerks.NvimShell"
APP_NAME = "AZWERKS Neovim"
EXECUTABLE_NAME = "azwerks-nvim-shell"
DEFAULT_NVIM_PATH = "/home/blndsft/.local/bin/nvim"
VERSION = "0.1.0"
```

### `radium.py`

Responsibilities:

```text
Radium color constants
helper functions for Gdk.RGBA conversion if required by installed API
terminal color setup helpers if supported by installed VTE API
```

Use these color constants:

```text
background: #202521
foreground: #ddecc4
surface:    #23282b
accent:     #ceda4a
muted:      #94a87a
faint:      #8e9290
```

Only apply colors using documented GTK/VTE APIs confirmed in the installed environment.

If a specific color API is unavailable, do not fake it.

Report what was skipped.

---

## Desktop Entry

Implement or update:

```text
data/com.azwerks.NvimShell.desktop
```

Required content:

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

Validate with:

```zsh
desktop-file-validate data/com.azwerks.NvimShell.desktop
```

If validation fails, fix the desktop file according to the validator output.

Do not claim desktop integration works unless validated.

---

## Icon

Create or update:

```text
data/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

Rules:

```text
valid SVG
original placeholder mark
do not copy official Neovim logo
use simple AZWERKS/Radium-inspired visual treatment
no trademarked icon copying
no embedded raster images
```

Allowed colors:

```text
#202521
#ddecc4
#ceda4a
#23282b
```

---

## User-Local Install Script

Implement:

```text
scripts/install-user.sh
```

Rules:

```text
must use zsh
must use set -euo pipefail
must not use sudo
must install only into the user home
must not modify /usr
must not modify /home/blndsft/.config/nvim
must not modify /home/blndsft/.local/bin/nvim
must not modify /home/blndsft/.local/opt/nvim-linux-x86_64
```

Expected install targets:

```text
~/.local/bin/azwerks-nvim-shell
~/.local/share/applications/com.azwerks.NvimShell.desktop
~/.local/share/icons/hicolor/scalable/apps/com.azwerks.NvimShell.svg
```

The installed executable may be a small wrapper that sets `PYTHONPATH` to the installed project source location, or the script may copy the package into a user-local application directory.

Choose the simplest reliable user-local approach.

Document the chosen approach.

If using a wrapper script, ensure it handles paths with spaces.

---

## User-Local Uninstall Script

Implement:

```text
scripts/uninstall-user.sh
```

Rules:

```text
must use zsh
must use set -euo pipefail
must remove only files installed by install-user.sh
must not remove Neovim
must not remove the user's Neovim config
must not remove unrelated icons or desktop entries
```

It must explicitly avoid deleting:

```text
~/.config/nvim
~/.local/bin/nvim
~/.local/opt/nvim-linux-x86_64
```

---

## Development Run Script

Implement:

```text
scripts/dev-run.sh
```

Rules:

```text
must use zsh
must use set -euo pipefail
must run app from source tree
must forward all arguments
```

Expected behavior:

```zsh
scripts/dev-run.sh
scripts/dev-run.sh --help
scripts/dev-run.sh --version
scripts/dev-run.sh /path/to/file
```

---

## Tests

### Unit Tests

Create or update:

```text
tests/test_cli.py
```

Use Python stdlib `unittest`.

Test at minimum:

```text
--help early exit
--version early exit
--help ignores later invalid args
--version ignores earlier positional args
unknown flag errors
missing --cwd value errors
missing --nvim-bin value errors
--cwd followed by --nvim-bin produces missing --cwd error
--nvim-bin followed by --cwd produces missing --nvim-bin error
invalid cwd errors
invalid nvim binary errors
duplicate --cwd uses last value
duplicate --nvim-bin uses last value
positional order preserved
nonexistent positional path passed through
single directory positional infers cwd
multiple directories do not infer cwd
mixed file and directory does not infer cwd
empty invocation produces nvim argv with only binary
paths with spaces stay as one argument
```

Use `tempfile` for temporary files/directories.

Do not require a GUI display for parser tests.

### Smoke Test

Update:

```text
tests/smoke.sh
```

It must run:

```zsh
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

It should validate the desktop file if `desktop-file-validate` exists:

```zsh
if command -v desktop-file-validate >/dev/null; then
  desktop-file-validate data/com.azwerks.NvimShell.desktop
fi
```

It should probe GTK/VTE imports but should not require launching a GUI window in headless environments.

---

## README Requirements

Update `README.md` with:

```text
purpose
scope
what this is
what this is not
dependencies
development run instructions
user install instructions
user uninstall instructions
CLI usage
known limitations
troubleshooting
```

The README must explicitly say:

```text
AZWERKS Neovim Shell is a GTK/VTE wrapper around terminal Neovim.
It is not a true Neovim GUI frontend.
It does not use nvim --embed.
It does not implement the Neovim UI protocol.
```

---

## CHANGELOG Requirements

Update `CHANGELOG.md` under `0.1.0` with the real implemented changes.

Do not claim features that were not implemented and tested.

---

## Validation Commands

Run these after implementation:

```zsh
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell

python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/smoke.sh
```

Run CLI checks:

```zsh
PYTHONPATH=src python3 -m azwerks_nvim_shell.main --help
PYTHONPATH=src python3 -m azwerks_nvim_shell.main --version
PYTHONPATH=src python3 -m azwerks_nvim_shell.main --foo
PYTHONPATH=src python3 -m azwerks_nvim_shell.main --cwd
PYTHONPATH=src python3 -m azwerks_nvim_shell.main missing.txt
```

Run GUI manually only if a display session is available:

```zsh
scripts/dev-run.sh
```

Do not claim GUI launch success unless actually tested.

---

## Hard Constraints

Do not:

```text
use sudo
install packages automatically
modify /usr
modify system alternatives
modify Black Box
modify the user's Neovim config
modify the user's Neovim binary
delete user files
copy official Neovim logo
use Electron
use a webview
silently switch toolkit
silently switch to GTK3
claim API behavior without validating it
claim desktop integration without validating the desktop file
claim GUI launch success unless actually launched
```

---

## Done When

The build is complete only when:

```text
CLI parser works and is tested
GTK/VTE imports are verified
GTK app window implementation exists
VTE terminal widget implementation exists
Neovim spawn is implemented through documented VTE API
desktop file validates
icon file exists and is valid SVG
dev-run script works
install-user script exists and is safe
uninstall-user script exists and is safe
unit tests pass
smoke test passes
README truthfully describes the app
CHANGELOG only claims real work
no existing Neovim config was modified
no system files were modified
```

If any item cannot be completed, report it honestly.

---

## Final Report Format

When finished, report:

```markdown
# AZWERKS Neovim Shell v0.1 Build Report

## Summary

## Documentation / API Checks Performed

## Files Changed

## Implementation Details

## CLI Behavior

## GTK/VTE Behavior

## Desktop Integration

## Tests Run

## Validation Results

## Known Limitations

## What Was Not Done

## Next Recommended Prompt
```
