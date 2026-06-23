"""GTK/VTE runtime layer for AZWERKS Neovim Shell.

This module builds the GTK application/window, creates a VTE terminal widget,
and spawns terminal Neovim through the launch contract produced by the CLI
parser.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import os
import sys
from typing import Any

from .cli import LaunchContract
from .config import (
    APP_ID,
    APP_NAME,
    DEBUG_ENV_VAR,
    QUIT_ON_CHILD_EXIT,
    WINDOW_DEFAULT_HEIGHT,
    WINDOW_DEFAULT_WIDTH,
)
from .radium import RADIUM_ACCENT, RADIUM_BACKGROUND, RADIUM_FOREGROUND


class GtkUnavailableError(Exception):
    """Raised when GTK/VTE bindings are unavailable."""


class SpawnError(Exception):
    """Raised when VTE cannot spawn Neovim."""


@dataclass(frozen=True)
class GtkModules:
    """Lazy-loaded GTK/VTE modules."""

    Gtk: Any
    Vte: Any
    GLib: Any
    Gio: Any
    Gdk: Any
    Pango: Any


def load_gtk_modules() -> GtkModules:
    """Load GTK/VTE modules only when the GUI is actually requested."""
    try:
        import gi  # type: ignore[import-not-found]

        gi.require_version("Gtk", "4.0")
        gi.require_version("Vte", "3.91")
        gi.require_version("Gdk", "4.0")
        gi.require_version("Pango", "1.0")
        from gi.repository import Gdk, Gio, GLib, Gtk, Pango, Vte  # type: ignore[import-not-found]
    except (ImportError, ValueError) as error:
        raise GtkUnavailableError(str(error)) from error

    return GtkModules(Gtk=Gtk, Vte=Vte, GLib=GLib, Gio=Gio, Gdk=Gdk, Pango=Pango)


def create_application(
    contract: LaunchContract,
    *,
    modules: GtkModules | None = None,
) -> Any:
    """Create a GTK application for the launch contract."""
    loaded = load_gtk_modules() if modules is None else modules
    Gtk = loaded.Gtk

    application = Gtk.Application(application_id=APP_ID)
    application.connect(
        "activate",
        lambda app: present_window(app, contract, modules=loaded),
    )
    return application


def present_window(
    application: Any,
    contract: LaunchContract,
    *,
    modules: GtkModules | None = None,
) -> Any:
    """Create and present the main window."""
    loaded = load_gtk_modules() if modules is None else modules
    Gtk = loaded.Gtk

    window = Gtk.ApplicationWindow(application=application)
    window.set_title(APP_NAME)
    window.set_default_size(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)
    window.set_child(create_terminal_widget(contract, modules=loaded, application=application))
    window.present()
    return window


def create_terminal_widget(
    contract: LaunchContract,
    *,
    modules: GtkModules | None = None,
    application: Any | None = None,
) -> Any:
    """Create the VTE terminal widget and spawn Neovim."""
    loaded = load_gtk_modules() if modules is None else modules
    terminal = create_lifecycle_terminal(modules=loaded, application=application)

    _call_if_available(terminal, "set_hexpand", True)
    _call_if_available(terminal, "set_vexpand", True)
    apply_visual_defaults(terminal, modules=loaded)

    try:
        spawn_neovim(terminal, contract, modules=loaded)
    except SpawnError as error:
        print(str(error), file=sys.stderr)
        _feed_terminal(terminal, f"\r\n{error}\r\n")

    return terminal


def create_terminal_placeholder(
    contract: LaunchContract,
    *,
    modules: GtkModules | None = None,
) -> Any:
    """Backward-compatible alias for the runtime terminal widget."""
    return create_terminal_widget(contract, modules=modules)


def create_lifecycle_terminal(
    *,
    modules: GtkModules,
    application: Any | None,
) -> Any:
    """Create a VTE terminal class with locally verified child-exit handling."""
    if application is None or not QUIT_ON_CHILD_EXIT:
        return modules.Vte.Terminal()

    class LifecycleTerminal(modules.Vte.Terminal):  # type: ignore[misc, valid-type]
        def do_child_exited(self, status: int) -> None:
            handle_child_exit(application, status)

    return LifecycleTerminal()


def spawn_neovim(
    terminal: Any,
    contract: LaunchContract,
    *,
    modules: GtkModules | None = None,
    env: dict[str, str] | None = None,
) -> None:
    """Spawn Neovim through VTE using the parsed launch contract."""
    loaded = load_gtk_modules() if modules is None else modules
    pty_flags = loaded.Vte.PtyFlags.DEFAULT
    spawn_flags = loaded.GLib.SpawnFlags.DEFAULT
    envv = prepare_child_environment(env)
    debug_log(f"resolved nvim_binary={contract.nvim_binary!r}")
    debug_log(f"resolved cwd={contract.cwd!r}")
    debug_log(f"final argv={list(contract.nvim_argv)!r}")

    try:
        terminal.spawn_async(
            pty_flags,
            contract.cwd,
            list(contract.nvim_argv),
            envv,
            spawn_flags,
            None,
            None,
            -1,
            loaded.Gio.Cancellable(),
            _spawn_async_callback,
            None,
        )
    except Exception as error:
        raise SpawnError(f"error: failed to spawn Neovim: {error}") from error


def prepare_child_environment(base_env: dict[str, str] | None = None) -> list[str]:
    """Prepare a preserved process environment for VTE child spawning."""
    child_env = dict(os.environ if base_env is None else base_env)
    child_env["TERM"] = "xterm-256color"
    child_env["COLORTERM"] = "truecolor"
    return [f"{key}={value}" for key, value in child_env.items()]


def debug_enabled(env: dict[str, str] | None = None) -> bool:
    """Return whether optional runtime diagnostics are enabled."""
    debug_env = os.environ if env is None else env
    return debug_env.get(DEBUG_ENV_VAR) == "1"


def debug_log(
    message: str,
    *,
    env: dict[str, str] | None = None,
    stream: Any | None = None,
) -> None:
    """Print an optional debug diagnostic without logging the full environment."""
    if not debug_enabled(env):
        return

    output = sys.stderr if stream is None else stream
    print(f"AZWERKS Neovim Shell debug: {message}", file=output)


def extract_child_pid(callback_args: tuple[object, ...]) -> int | None:
    """Extract a positive child pid from the local spawn callback arguments."""
    for arg in callback_args:
        if isinstance(arg, int) and arg > 0:
            return arg
    return None


def watch_spawned_child(callback_args: tuple[object, ...]) -> int | None:
    """Call VTE watch_child for the spawned child pid when available."""
    if not callback_args:
        return None

    terminal = callback_args[0]
    pid = extract_child_pid(callback_args)
    watch_child = getattr(terminal, "watch_child", None)
    if pid is None or watch_child is None:
        return None

    watch_child(pid)
    return pid


def format_child_exit_status(status: int) -> str:
    """Format the raw VTE child-exit status with decoded exit details."""
    if os.WIFEXITED(status):
        return f"status={status} exit_code={os.WEXITSTATUS(status)}"
    if os.WIFSIGNALED(status):
        return f"status={status} signal={os.WTERMSIG(status)}"
    return f"status={status}"


def handle_child_exit(
    application: Any | None,
    status: int,
    *,
    stream: Any = sys.stderr,
) -> None:
    """Log child exit and quit the GTK application when possible."""
    debug_log(f"child-exited observed {format_child_exit_status(status)}")
    print(f"AZWERKS Neovim Shell child exited: {format_child_exit_status(status)}", file=stream)
    quit_application = getattr(application, "quit", None)
    if quit_application is None:
        return
    try:
        quit_application()
    except RuntimeError as error:
        print(f"warning: application quit failed after child exit: {error}", file=stream)


def apply_visual_defaults(
    terminal: Any,
    *,
    modules: GtkModules | None = None,
) -> None:
    """Apply supported Radium-inspired VTE visual defaults."""
    loaded = load_gtk_modules() if modules is None else modules

    foreground = _parse_rgba(loaded, RADIUM_FOREGROUND)
    background = _parse_rgba(loaded, RADIUM_BACKGROUND)
    cursor = _parse_rgba(loaded, RADIUM_ACCENT)

    _call_if_available(terminal, "set_color_foreground", foreground)
    _call_if_available(terminal, "set_color_background", background)
    _call_if_available(terminal, "set_color_cursor", cursor)

    font = loaded.Pango.FontDescription.from_string("Monospace 11")
    _call_if_available(terminal, "set_font", font)


def run_app(contract: LaunchContract) -> int:
    """Run the GTK application without forwarding CLI args to GTK."""
    application = create_application(contract)
    return int(application.run([]))


def _feed_terminal(terminal: Any, text: str) -> None:
    feed = getattr(terminal, "feed", None)
    if feed is None:
        return

    try:
        feed(text.encode("utf-8"))
    except TypeError:
        feed(text, len(text))


def _call_if_available(target: Any, method_name: str, *args: Any) -> None:
    method: Callable[..., Any] | None = getattr(target, method_name, None)
    if method is not None:
        method(*args)


def _parse_rgba(modules: GtkModules, color: str) -> Any:
    rgba = modules.Gdk.RGBA()
    if not rgba.parse(color):
        raise ValueError(f"invalid RGBA color '{color}'")
    return rgba


def _spawn_async_callback(*args: Any) -> None:
    """Report spawn callback errors and keep lifecycle handling with VTE."""
    error = args[2] if len(args) >= 3 else None
    pid = extract_child_pid(args)
    debug_log(f"VTE spawn callback fired argc={len(args)} pid={pid!r} watch_child_used=False")
    if error is not None:
        print(f"error: VTE spawn callback reported: {error}", file=sys.stderr)
        return

    if pid is None:
        print("warning: VTE spawn callback did not expose a watchable child pid", file=sys.stderr)
