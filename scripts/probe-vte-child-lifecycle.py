#!/usr/bin/env python3
"""Probe local VTE child lifecycle behavior with a short-lived child."""

from __future__ import annotations

import os
import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Vte", "3.91")
gi.require_version("Gdk", "4.0")
from gi.repository import Gio, GLib, Gtk, Vte


TIMEOUT_SECONDS = 8


class ProbeTerminal(Vte.Terminal):
    def __init__(self, application: Gtk.Application) -> None:
        super().__init__()
        self.application = application
        self.child_exited_status: int | None = None

    def do_child_exited(self, status: int) -> None:
        self.child_exited_status = status
        print(f"child-exited status={status}")
        self.application.quit()


class Probe:
    def __init__(self) -> None:
        self.application = Gtk.Application(application_id="com.azwerks.NvimShell.LifecycleProbe")
        self.application.connect("activate", self.on_activate)
        self.terminal: ProbeTerminal | None = None
        self.spawn_callback_args: tuple[object, ...] | None = None
        self.spawn_pid: int | None = None

    def on_activate(self, application: Gtk.Application) -> None:
        window = Gtk.ApplicationWindow(application=application)
        window.set_title("AZWERKS VTE Lifecycle Probe")
        window.set_default_size(640, 240)

        terminal = ProbeTerminal(application)
        self.terminal = terminal
        window.set_child(terminal)
        window.present()

        argv = ["/bin/sh", "-lc", 'printf "azwerks lifecycle probe\\n"; exit 7']
        env = dict(os.environ)
        env["TERM"] = "xterm-256color"
        env["COLORTERM"] = "truecolor"
        envv = [f"{key}={value}" for key, value in env.items()]

        print("spawning lifecycle probe child")
        terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,
            os.getcwd(),
            argv,
            envv,
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            -1,
            Gio.Cancellable(),
            self.on_spawn_ready,
            None,
        )
        GLib.timeout_add_seconds(TIMEOUT_SECONDS, self.on_timeout)

    def on_spawn_ready(self, *args: object) -> None:
        self.spawn_callback_args = args
        print(f"spawn callback argc={len(args)}")
        for index, arg in enumerate(args):
            print(f"spawn callback arg{index}={arg!r} type={type(arg).__name__}")
            if isinstance(arg, int) and arg > 0:
                self.spawn_pid = arg

        if self.spawn_pid is not None and self.terminal is not None and hasattr(self.terminal, "watch_child"):
            print(f"watch_child pid={self.spawn_pid}")
            self.terminal.watch_child(self.spawn_pid)
        else:
            print("watch_child not called; no child pid observed")

    def on_timeout(self) -> bool:
        if self.terminal is not None and self.terminal.child_exited_status is not None:
            return False

        print("error: lifecycle probe timed out", file=sys.stderr)
        self.application.quit()
        return False

    def run(self) -> int:
        exit_code = int(self.application.run([]))
        if self.terminal is None:
            print("error: terminal was not created", file=sys.stderr)
            return 2
        if self.spawn_pid is None:
            print("error: spawn callback did not expose a child pid", file=sys.stderr)
            return 3
        if self.terminal.child_exited_status is None:
            print("error: child exit was not observed", file=sys.stderr)
            return 4

        print("lifecycle probe succeeded")
        return exit_code


def main() -> int:
    if not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
        print("error: no graphical session available for lifecycle probe", file=sys.stderr)
        return 5
    return Probe().run()


if __name__ == "__main__":
    raise SystemExit(main())
