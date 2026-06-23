# Argument Parsing Rules

## Overview

- Arguments are processed strictly left-to-right.
- Flags and positional arguments may be interleaved.
- Later occurrences of the same flag override earlier ones.
- Flags that require values consume the next token.

## Early Exit Flags

- `--help` and `--version` have absolute precedence.
- They immediately stop parsing.
- They ignore all earlier and later flags and positional arguments.
- They print output and exit `0` without launching GTK or Neovim.

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
5. If mixed file and directory arguments exist, do not infer cwd.

Resolved launch working directories are absolute paths. Positional arguments
are preserved exactly as passed.

## Binary Detection

1. Use `--nvim-bin` if provided.
2. Else use `/home/blndsft/.local/bin/nvim` if it exists and is executable.
3. Else use `nvim` from `PATH` if found and executable.

If no executable Neovim binary can be found, produce:

```text
error: could not find executable nvim binary
```

## Neovim Invocation

- Final argv is `[nvim_binary, *positional_args]`.
- Do not pass `--cwd` to Neovim.
- Set working directory through the process spawn call.
- The parser only produces a launch contract; it does not spawn Neovim.

## Error Handling

- Missing values produce: `error: missing value for flag '<flag>'`
- Unknown flags produce: `error: unknown flag '<flag>'`
- Invalid nvim binary path produces: `error: invalid nvim binary path '<path>'`
- Invalid working directory produces: `error: invalid working directory '<path>'`
- CLI errors print to stderr, exit non-zero, and do not launch GTK or Neovim.
