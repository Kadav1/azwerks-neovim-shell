# Architecture

AZWERKS Neovim Shell v0.1 is implemented as a GTK/VTE wrapper.

The current Phase 4 implementation creates a GTK application/window, creates a
VTE terminal widget, and spawns terminal Neovim through VTE.

It will not implement Neovim's external UI protocol in v0.1.

```text
AZWERKS Neovim Shell
  └── GTK Application Window
      └── VTE Terminal Widget
          └── nvim
```

The Neovim argv and cwd come from the CLI launch contract. The app does not use
`nvim --embed` and does not implement the Neovim external UI protocol.

Child-exit lifecycle handling is implemented through the locally verified
`Vte.Terminal.do_child_exited(status)` subclass path. The app does not connect
an invented `child-exited` signal name.
