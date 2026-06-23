# Codex Prompt — AZWERKS Neovim Shell v0.1 CLI Parsing + Launch Contract Implementation

## Goal

Implement the CLI parsing and launch-contract layer for **AZWERKS Neovim Shell v0.1**.

This is the next step after the scaffolding pass.

Do **not** implement the GTK/VTE window yet.

Do **not** spawn Neovim yet from the real application path.

Do **not** install anything.

Do **not** modify the user’s existing Neovim config.

The purpose of this pass is to create a tested, deterministic CLI parser that resolves:

```text
nvim binary
working directory
positional file/directory arguments
help/version early exits
clear CLI error handling
```

This parser will later be used by the GTK/VTE implementation to spawn Neovim safely.

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

If the scaffold does not exist, stop and report that the scaffolding pass must be completed first.

---

## Scope

Allowed changes:

```text
src/azwerks_nvim_shell/main.py
src/azwerks_nvim_shell/config.py
src/azwerks_nvim_shell/cli.py
tests/test_cli.py
tests/smoke.sh
README.md
docs/argument-parsing-rules.md
CHANGELOG.md
```

If `src/azwerks_nvim_shell/cli.py` does not exist, create it.

If `tests/test_cli.py` does not exist, create it.

Do not modify:

```text
/home/blndsft/.config/nvim
/home/blndsft/.local/bin/nvim
/home/blndsft/.local/opt/nvim-linux-x86_64
```

Do not implement:

```text
GTK application window
VTE terminal widget
VTE spawn_async
desktop install behavior
icon generation
full user install logic
```

This pass is CLI/parser only.

---

## Required CLI Rules

Implement the following argument parsing contract exactly.

### Overview

* Arguments are processed strictly left-to-right.
* Flags and positional arguments may be interleaved.
* Later occurrences of the same flag override earlier ones.
* Flags that require values consume the next token.

### Early Exit Flags

`--help` and `--version`:

* Have absolute precedence.
* Immediately stop all parsing when encountered.
* Ignore all other flags and positional arguments.
* Print output and exit without launching GTK or Neovim.

Examples:

```zsh
azwerks-nvim-shell --help
azwerks-nvim-shell file.txt --version
azwerks-nvim-shell --cwd /project --help file.txt
```

All of these must exit cleanly without attempting to validate later arguments or launch anything.

### Supported Flags

```text
--help
--version
--cwd <path>
--nvim-bin <path>
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

### `--nvim-bin <path>`

Behavior:

* Overrides binary detection.
* Must be a valid executable path.
* Later occurrences override earlier ones.

Invalid path error format:

```text
error: invalid nvim binary path '<path>'
```

Examples:

```zsh
azwerks-nvim-shell --nvim-bin /usr/bin/nvim
azwerks-nvim-shell --nvim-bin /a --nvim-bin /b
azwerks-nvim-shell --nvim-bin /bad/path
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

Examples:

```zsh
azwerks-nvim-shell --cwd /project
azwerks-nvim-shell --cwd /a --cwd /b file.txt
azwerks-nvim-shell --cwd /tmp/missing-dir
```

### Missing Flag Values

Flags requiring values:

```text
--cwd
--nvim-bin
```

If a value is missing, error.

If the next token is another flag, treat this as a missing value error and do not consume the second flag.

Error format:

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

Expected errors:

```text
error: missing value for flag '--cwd'
error: missing value for flag '--nvim-bin'
```

### Positional Arguments

* Non-flag tokens are treated as file or directory paths.
* Order is preserved.
* Shell expressions are not expanded.
* Nonexistent paths are passed through unchanged.
* Paths with spaces remain single arguments if passed as a single shell argument.

Examples:

```zsh
azwerks-nvim-shell file.txt
azwerks-nvim-shell file1.txt file2.txt
azwerks-nvim-shell "my file.txt"
azwerks-nvim-shell missing.txt
azwerks-nvim-shell ./file.txt
```

### Working Directory Resolution

Resolve working directory in this order:

1. Use `--cwd` if provided.
2. Else if exactly one positional argument is an existing directory, use that directory.
3. Else use the current process working directory.

Important:

* If multiple directory arguments exist, do not infer cwd.
* If mixed file and directory arguments exist, do not infer cwd.
* Nonexistent paths are not directories and must not be used for cwd inference.

Examples:

```zsh
azwerks-nvim-shell dir1
```

If `dir1` exists and is a directory:

```text
cwd = dir1
```

Example:

```zsh
azwerks-nvim-shell dir1 dir2
```

If both are directories:

```text
cwd = current process working directory
```

Example:

```zsh
azwerks-nvim-shell dir1 file.txt
```

If `dir1` is a directory and `file.txt` is a file:

```text
cwd = current process working directory
```

### Neovim Invocation Contract

The parser must produce a launch contract object containing:

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

Set working directory through the later process spawn call, not through Neovim flags.

### Empty Invocation

```zsh
azwerks-nvim-shell
```

Expected behavior:

* Resolve nvim binary.
* Use current process working directory.
* Use no positional arguments.
* Produce:

```text
[nvim_binary]
```

Do not error.

---

## Binary Detection Rules

Default preferred Neovim path:

```text
/home/blndsft/.local/bin/nvim
```

If that path exists and is executable, use it.

Otherwise fall back to `nvim` from `PATH`.

If no executable Neovim binary can be found, error with:

```text
error: could not find executable nvim binary
```

Do not launch GTK or Neovim.

Do not install Neovim.

Do not modify PATH.

---

## Implementation Requirements

Create a pure parser module:

```text
src/azwerks_nvim_shell/cli.py
```

Recommended contents:

```text
CliError
EarlyExit
LaunchContract
parse_argv(argv, *, cwd=None, env=None)
find_nvim_binary(override=None)
format_help()
format_version()
```

Use Python stdlib only.

Use `dataclasses` where helpful.

Do not use argparse if it cannot satisfy the strict left-to-right early-exit/missing-value behavior exactly.

If using argparse, prove through tests that it matches the required contract. Otherwise implement a small manual parser.

The parser must be testable without launching GTK.

The parser must be testable without launching Neovim.

---

## `main.py` Behavior

Update `main.py` so it uses the parser.

For this pass, because GTK/VTE is not implemented yet:

* `--help` prints help and exits `0`.
* `--version` prints version and exits `0`.
* CLI errors print to stderr and exit non-zero.
* Valid launch contracts should print a clear placeholder summary and exit `0`.

Placeholder summary example:

```text
AZWERKS Neovim Shell launch contract
nvim_binary: /home/blndsft/.local/bin/nvim
cwd: /some/path
argv: ['/home/blndsft/.local/bin/nvim', 'file.txt']
GTK/VTE launch not implemented yet.
```

Do not launch GTK.

Do not launch Neovim.

---

## Required Tests

Create:

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

Use temporary directories and files from Python’s `tempfile` module.

Do not rely on the user’s real filesystem except where explicitly testing the default nvim binary detection. Prefer dependency injection or temporary executable files for tests.

---

## Update Smoke Test

Update:

```text
tests/smoke.sh
```

It should run:

```zsh
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

Keep existing desktop-file validation if present.

Do not require launching a GUI.

Do not require a display server.

---

## Documentation Updates

Update:

```text
docs/argument-parsing-rules.md
```

It must match the implemented parser behavior.

Update:

```text
README.md
```

Add a short section:

```markdown
## CLI Contract

The current implementation validates arguments and produces a launch contract.
GTK/VTE launch is not implemented yet.
```

Update:

```text
CHANGELOG.md
```

Add under `0.1.0`:

```markdown
- Implemented CLI parsing and launch-contract generation.
- Added parser unit tests.
- Updated smoke test to run CLI unit tests.
```

---

## Validation Commands

Run:

```zsh
cd /media/blndsft/SLP-ARCH-01/azwerks/azwerks-nvim-shell
python3 -m py_compile src/azwerks_nvim_shell/*.py
python3 -m unittest discover -s tests -p 'test_*.py'
tests/smoke.sh
```

Also test these commands manually:

```zsh
PYTHONPATH=src python3 -m azwerks_nvim_shell.main --help
PYTHONPATH=src python3 -m azwerks_nvim_shell.main --version
PYTHONPATH=src python3 -m azwerks_nvim_shell.main --foo
PYTHONPATH=src python3 -m azwerks_nvim_shell.main --cwd
PYTHONPATH=src python3 -m azwerks_nvim_shell.main missing.txt
```

---

## Constraints

Do not:

```text
implement GTK
implement VTE
spawn Neovim
modify Neovim config
install packages
use sudo
modify desktop entries outside the project
modify icons outside the project
create files outside the project
```

This is a CLI parsing and launch-contract pass only.

---

## Done When

The task is done when:

```text
cli.py exists
main.py uses cli.py
valid commands produce launch-contract summaries
--help exits cleanly
--version exits cleanly
CLI errors print exact required error formats
unit tests cover required parser behavior
tests/smoke.sh passes
docs match implementation
no GTK/VTE code is implemented yet
no Neovim process is spawned
```

---

## Final Report Format

When finished, report:

```markdown
# AZWERKS Neovim Shell CLI Parsing Implementation Report

## Summary

## Files Changed

## Parser Behavior Implemented

## Tests Added

## Validation Commands Run

## Results

## Known Limitations

## Next Recommended Prompt
```

