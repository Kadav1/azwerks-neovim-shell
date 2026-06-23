#!/usr/bin/env python3
"""Compare local VTE child lifecycle variants with a short-lived child."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Vte", "3.91")
from gi.repository import Gio, GLib, GObject, Gtk, Vte


TIMEOUT_SECONDS = 8
CHILD_ARGV = ["/bin/sh", "-lc", 'printf "azwerks lifecycle variant probe\\n"; exit 7']
SUPPORTED_VARIANTS = ("current_watch", "no_explicit_watch")
BASE_CHILD_EXITED_SIGNAL_ID = GObject.signal_lookup("child-exited", Vte.Terminal)


class VariantTerminal(Vte.Terminal):
    def __init__(self, application: Gtk.Application) -> None:
        super().__init__()
        self.application = application
        self.child_exited_status: int | None = None

    def do_child_exited(self, status: int) -> None:
        self.child_exited_status = status
        print(f"child-exited status={status}")
        self.application.quit()


class VariantProbe:
    def __init__(self, variant: str) -> None:
        self.variant = variant
        self.application = Gtk.Application(
            application_id=f"com.azwerks.NvimShell.LifecycleVariant.{variant}"
        )
        self.application.connect("activate", self.on_activate)
        self.terminal: VariantTerminal | None = None
        self.spawn_pid: int | None = None
        self.watch_child_used = False

    def on_activate(self, application: Gtk.Application) -> None:
        window = Gtk.ApplicationWindow(application=application)
        window.set_title(f"AZWERKS VTE Lifecycle Variant: {self.variant}")
        window.set_default_size(640, 240)

        terminal = VariantTerminal(application)
        self.terminal = terminal
        window.set_child(terminal)
        window.present()

        env = dict(os.environ)
        env["TERM"] = "xterm-256color"
        env["COLORTERM"] = "truecolor"
        envv = [f"{key}={value}" for key, value in env.items()]

        print(f"variant={self.variant}")
        print("spawning lifecycle variant child")
        terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,
            os.getcwd(),
            CHILD_ARGV,
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
        print(f"spawn callback argc={len(args)}")
        for index, arg in enumerate(args):
            print(f"spawn callback arg{index}={arg!r} type={type(arg).__name__}")
            if isinstance(arg, int) and arg > 0:
                self.spawn_pid = arg

        error = args[2] if len(args) >= 3 else None
        if error is not None:
            print(f"error: spawn callback reported {error}", file=sys.stderr)
            self.application.quit()
            return

        if self.variant == "current_watch":
            self.call_watch_child()
        elif self.variant == "no_explicit_watch":
            print("watch_child not called by variant")
        else:
            print(f"error: unsupported variant {self.variant}", file=sys.stderr)
            self.application.quit()

    def call_watch_child(self) -> None:
        if self.spawn_pid is None or self.terminal is None or not hasattr(self.terminal, "watch_child"):
            print("watch_child not called; no child pid observed")
            return

        print(f"watch_child pid={self.spawn_pid}")
        self.terminal.watch_child(self.spawn_pid)
        self.watch_child_used = True

    def on_timeout(self) -> bool:
        if self.terminal is not None and self.terminal.child_exited_status is not None:
            return False

        print("error: lifecycle variant timed out", file=sys.stderr)
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

        print(f"watch_child_used={self.watch_child_used}")
        print("lifecycle variant succeeded")
        return exit_code


def signal_supported(signal_name: str) -> bool:
    return bool(GObject.signal_lookup(signal_name, Vte.Terminal))


def run_parent() -> int:
    if not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
        print("error: no graphical session available for lifecycle variant probe", file=sys.stderr)
        return 5

    print("# VTE lifecycle variant probe")
    print(f"base child-exited signal id before subclass registration: {BASE_CHILD_EXITED_SIGNAL_ID}")
    print(f"child-exited signal id after subclass registration: {GObject.signal_lookup('child-exited', Vte.Terminal)}")
    print("signal_only variant skipped: the app uses the locally verified do_child_exited virtual method path")
    print()

    success_count = 0
    for variant in SUPPORTED_VARIANTS:
        command = [sys.executable, __file__, "--variant", variant]
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS + 6,
        )
        waitid_warning = "waitid(" in completed.stderr or "No child processes" in completed.stderr
        traceback = "Traceback" in completed.stderr
        observed = "child-exited status=" in completed.stdout
        if completed.returncode == 0 and observed:
            success_count += 1

        print(f"## {variant}")
        print(f"exit_code: {completed.returncode}")
        print(f"child_exited_observed: {observed}")
        print(f"waitid_warning: {waitid_warning}")
        print(f"traceback: {traceback}")
        print("--- stdout ---")
        print(completed.stdout.rstrip() or "(empty)")
        print("--- stderr ---")
        print(completed.stderr.rstrip() or "(empty)")
        print()

    return 0 if success_count else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=SUPPORTED_VARIANTS)
    args = parser.parse_args()

    if args.variant:
        return VariantProbe(args.variant).run()
    return run_parent()


if __name__ == "__main__":
    raise SystemExit(main())
