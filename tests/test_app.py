from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any
from contextlib import redirect_stderr
from io import StringIO
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from azwerks_nvim_shell.app import (  # noqa: E402
    GtkModules,
    GtkUnavailableError,
    create_application,
    create_terminal_widget,
    prepare_child_environment,
    run_app,
    spawn_neovim,
)
from azwerks_nvim_shell.cli import LaunchContract  # noqa: E402
from azwerks_nvim_shell.config import APP_ID  # noqa: E402


class GtkAppRuntimeTests(unittest.TestCase):
    def test_create_terminal_widget_applies_visuals_and_spawns_contract(self) -> None:
        terminal = create_terminal_widget(self._contract(), modules=fake_modules())

        self.assertTrue(terminal.hexpand)
        self.assertTrue(terminal.vexpand)
        self.assertEqual(terminal.foreground.spec, "#ddecc4")
        self.assertEqual(terminal.background.spec, "#202521")
        self.assertEqual(terminal.cursor.spec, "#ceda4a")
        self.assertEqual(terminal.font.description, "Monospace 11")
        self.assertEqual(len(terminal.spawn_calls), 1)
        spawn_call = terminal.spawn_calls[0]
        self.assertEqual(spawn_call["working_directory"], "/tmp/project")
        self.assertEqual(spawn_call["argv"], ["/tmp/nvim", "file.txt"])
        self.assertIn("TERM=xterm-256color", spawn_call["envv"])
        self.assertIn("COLORTERM=truecolor", spawn_call["envv"])

    def test_create_application_registers_activate_handler(self) -> None:
        application = create_application(self._contract(), modules=fake_modules())

        self.assertEqual(application.application_id, APP_ID)
        self.assertIn("activate", application.handlers)

    def test_run_app_returns_gtk_exit_code(self) -> None:
        modules = fake_modules()

        with patch("azwerks_nvim_shell.app.create_application") as create:
            create.return_value = modules.Gtk.Application(application_id=APP_ID)

            self.assertEqual(run_app(self._contract()), 0)

    def test_load_failure_surfaces_as_gtk_unavailable(self) -> None:
        with patch("azwerks_nvim_shell.app.load_gtk_modules") as load:
            load.side_effect = GtkUnavailableError("missing GTK")

            with self.assertRaisesRegex(GtkUnavailableError, "missing GTK"):
                create_application(self._contract())

    def test_spawn_neovim_uses_documented_argument_order(self) -> None:
        modules = fake_modules()
        terminal = modules.Vte.Terminal()

        spawn_neovim(
            terminal,
            self._contract(),
            modules=modules,
            env={"EXISTING": "1"},
        )

        self.assertEqual(len(terminal.spawn_calls), 1)
        call = terminal.spawn_calls[0]
        self.assertEqual(call["pty_flags"], "PTY_DEFAULT")
        self.assertEqual(call["working_directory"], "/tmp/project")
        self.assertEqual(call["argv"], ["/tmp/nvim", "file.txt"])
        self.assertIn("EXISTING=1", call["envv"])
        self.assertIn("TERM=xterm-256color", call["envv"])
        self.assertIn("COLORTERM=truecolor", call["envv"])
        self.assertEqual(call["spawn_flags"], "SPAWN_DEFAULT")
        self.assertIsNone(call["child_setup"])
        self.assertIsNone(call["child_setup_data"])
        self.assertEqual(call["timeout"], -1)
        self.assertTrue(call["cancellable"])
        self.assertTrue(call["callback"])
        self.assertIsNone(call["user_data"])

    def test_prepare_child_environment_preserves_env_and_sets_terminal_colors(self) -> None:
        envv = prepare_child_environment(
            {
                "PATH": "/tmp/bin",
                "TERM": "dumb",
                "COLORTERM": "old",
            }
        )

        self.assertIn("PATH=/tmp/bin", envv)
        self.assertIn("TERM=xterm-256color", envv)
        self.assertIn("COLORTERM=truecolor", envv)

    def test_spawn_failure_is_written_to_terminal(self) -> None:
        modules = fake_modules(spawn_error=RuntimeError("no spawn"))
        stderr = StringIO()

        with redirect_stderr(stderr):
            terminal = create_terminal_widget(self._contract(), modules=modules)

        self.assertEqual(len(terminal.spawn_calls), 1)
        self.assertEqual(len(terminal.feed_calls), 1)
        self.assertIn(b"error: failed to spawn Neovim: no spawn", terminal.feed_calls[0])
        self.assertIn("error: failed to spawn Neovim: no spawn", stderr.getvalue())

    @staticmethod
    def _contract() -> LaunchContract:
        return LaunchContract(
            nvim_binary="/tmp/nvim",
            cwd="/tmp/project",
            positional_args=["file.txt"],
            nvim_argv=["/tmp/nvim", "file.txt"],
        )


class FakeApplication:
    def __init__(self, *, application_id: str) -> None:
        self.application_id = application_id
        self.handlers: dict[str, Any] = {}

    def connect(self, signal_name: str, handler: Any) -> None:
        self.handlers[signal_name] = handler

    def run(self, argv: list[str]) -> int:
        if "activate" in self.handlers:
            self.handlers["activate"](self)
        return 0


class FakeWindow:
    def __init__(self, *, application: Any) -> None:
        self.application = application
        self.title: str | None = None
        self.default_size: tuple[int, int] | None = None
        self.child: Any = None
        self.presented = False

    def set_title(self, title: str) -> None:
        self.title = title

    def set_default_size(self, width: int, height: int) -> None:
        self.default_size = (width, height)

    def set_child(self, child: Any) -> None:
        self.child = child

    def present(self) -> None:
        self.presented = True


class FakeTerminal:
    spawn_error: Exception | None = None

    def __init__(self) -> None:
        self.hexpand = False
        self.vexpand = False
        self.feed_calls: list[Any] = []
        self.spawn_calls: list[dict[str, Any]] = []
        self.foreground: Any = None
        self.background: Any = None
        self.cursor: Any = None
        self.font: Any = None

    def set_hexpand(self, value: bool) -> None:
        self.hexpand = value

    def set_vexpand(self, value: bool) -> None:
        self.vexpand = value

    def feed(self, value: Any) -> None:
        self.feed_calls.append(value)

    def set_color_foreground(self, value: Any) -> None:
        self.foreground = value

    def set_color_background(self, value: Any) -> None:
        self.background = value

    def set_color_cursor(self, value: Any) -> None:
        self.cursor = value

    def set_font(self, value: Any) -> None:
        self.font = value

    def spawn_async(
        self,
        pty_flags: Any,
        working_directory: str,
        argv: list[str],
        envv: list[str],
        spawn_flags: Any,
        child_setup: Any,
        child_setup_data: Any,
        timeout: int,
        cancellable: Any,
        callback: Any,
        user_data: Any,
    ) -> None:
        self.spawn_calls.append(
            {
                "pty_flags": pty_flags,
                "working_directory": working_directory,
                "argv": argv,
                "envv": envv,
                "spawn_flags": spawn_flags,
                "child_setup": child_setup,
                "child_setup_data": child_setup_data,
                "timeout": timeout,
                "cancellable": cancellable,
                "callback": callback,
                "user_data": user_data,
            }
        )
        if self.spawn_error is not None:
            raise self.spawn_error


class FakeRGBA:
    def __init__(self) -> None:
        self.spec: str | None = None

    def parse(self, spec: str) -> bool:
        self.spec = spec
        return spec.startswith("#")


class FakeFontDescription:
    def __init__(self, description: str) -> None:
        self.description = description

    @classmethod
    def from_string(cls, description: str) -> "FakeFontDescription":
        return cls(description)


def fake_modules(spawn_error: Exception | None = None) -> GtkModules:
    class Terminal(FakeTerminal):
        pass

    Terminal.spawn_error = spawn_error

    return GtkModules(
        Gtk=SimpleNamespace(
            Application=FakeApplication,
            ApplicationWindow=FakeWindow,
        ),
        Vte=SimpleNamespace(
            Terminal=Terminal,
            PtyFlags=SimpleNamespace(DEFAULT="PTY_DEFAULT"),
        ),
        GLib=SimpleNamespace(SpawnFlags=SimpleNamespace(DEFAULT="SPAWN_DEFAULT")),
        Gio=SimpleNamespace(Cancellable=lambda: "CANCELLABLE"),
        Gdk=SimpleNamespace(RGBA=FakeRGBA),
        Pango=SimpleNamespace(FontDescription=FakeFontDescription),
    )
