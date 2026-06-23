# Runtime Diagnostics

## Scope

AZWERKS Neovim Shell keeps default runtime output quiet except for actionable
errors and child-exit status.

## Debug Mode

Set:

```zsh
AZWERKS_NVIM_SHELL_DEBUG=1
```

When enabled, the app prints debug diagnostics to stderr.

Diagnostics include:

- resolved Neovim binary
- resolved working directory
- final argv
- VTE spawn callback PID
- whether explicit `watch_child` was used
- child-exit status

Diagnostics do not include the full process environment.

## Manual Verification

Phase 8 verified debug mode with:

```zsh
AZWERKS_NVIM_SHELL_DEBUG=1 timeout 8s scripts/dev-run.sh --nvim-bin /bin/sh -lc 'printf "azwerks phase 8 debug lifecycle test\n"; exit 7'
```

Observed debug lines included the resolved binary, cwd, final argv, spawn
callback PID, `watch_child_used=False`, and decoded child exit code.

## Automated Tests

`tests/test_runtime_diagnostics.py` covers the pure diagnostic helpers without
opening a GUI or spawning Neovim.
