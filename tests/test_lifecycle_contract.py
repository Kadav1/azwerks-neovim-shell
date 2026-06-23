from __future__ import annotations

from io import StringIO
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from azwerks_nvim_shell.app import (  # noqa: E402
    extract_child_pid,
    format_child_exit_status,
    handle_child_exit,
    watch_spawned_child,
)
from azwerks_nvim_shell.config import QUIT_ON_CHILD_EXIT  # noqa: E402


class LifecycleContractTests(unittest.TestCase):
    def test_lifecycle_policy_defaults_to_close_on_child_exit(self) -> None:
        self.assertTrue(QUIT_ON_CHILD_EXIT)

    def test_extract_child_pid_finds_positive_integer(self) -> None:
        self.assertEqual(extract_child_pid((object(), 1234, None, None)), 1234)

    def test_extract_child_pid_returns_none_without_pid(self) -> None:
        self.assertIsNone(extract_child_pid((object(), None, None)))

    def test_watch_spawned_child_calls_terminal_watch_child(self) -> None:
        terminal = FakeTerminal()

        pid = watch_spawned_child((terminal, 4321, None, None))

        self.assertEqual(pid, 4321)
        self.assertEqual(terminal.watched_pids, [4321])

    def test_watch_spawned_child_refuses_unwatchable_callback(self) -> None:
        self.assertIsNone(watch_spawned_child((object(), None, None)))

    def test_child_exit_handler_quits_application(self) -> None:
        app = FakeApplication()
        stream = StringIO()

        handle_child_exit(app, 0, stream=stream)

        self.assertTrue(app.quit_called)
        self.assertIn("exit_code=0", stream.getvalue())

    def test_nonzero_child_status_is_logged_without_exception(self) -> None:
        app = FakeApplication()
        stream = StringIO()

        handle_child_exit(app, 7 << 8, stream=stream)

        self.assertTrue(app.quit_called)
        self.assertIn("exit_code=7", stream.getvalue())

    def test_child_exit_handler_is_safe_without_application(self) -> None:
        stream = StringIO()

        handle_child_exit(None, 0, stream=stream)

        self.assertIn("exit_code=0", stream.getvalue())

    def test_format_child_exit_status_decodes_signal_status(self) -> None:
        self.assertIn("signal=", format_child_exit_status(15))


class FakeTerminal:
    def __init__(self) -> None:
        self.watched_pids: list[int] = []

    def watch_child(self, pid: int) -> None:
        self.watched_pids.append(pid)


class FakeApplication:
    def __init__(self) -> None:
        self.quit_called = False

    def quit(self) -> None:
        self.quit_called = True
