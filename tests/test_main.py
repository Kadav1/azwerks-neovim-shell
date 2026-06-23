from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from azwerks_nvim_shell.app import GtkUnavailableError  # noqa: E402
from azwerks_nvim_shell.main import main  # noqa: E402


class MainEntrypointTests(unittest.TestCase):
    def test_help_exits_before_app_run(self) -> None:
        stdout = StringIO()

        with patch("azwerks_nvim_shell.main.run_app") as run_app:
            with redirect_stdout(stdout):
                exit_code = main(["--help"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Usage:", stdout.getvalue())
        run_app.assert_not_called()

    def test_cli_error_exits_before_app_run(self) -> None:
        stderr = StringIO()

        with patch("azwerks_nvim_shell.main.run_app") as run_app:
            with redirect_stderr(stderr):
                exit_code = main(["--foo"])

        self.assertEqual(exit_code, 2)
        self.assertEqual(stderr.getvalue().strip(), "error: unknown flag '--foo'")
        run_app.assert_not_called()

    def test_valid_contract_runs_app(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            nvim = self._make_executable(Path(tmp) / "nvim")

            with patch("azwerks_nvim_shell.main.run_app", return_value=0) as run_app:
                exit_code = main(["--nvim-bin", str(nvim), "file.txt"])

        self.assertEqual(exit_code, 0)
        run_app.assert_called_once()
        contract = run_app.call_args.args[0]
        self.assertEqual(contract.nvim_binary, str(nvim))
        self.assertEqual(contract.positional_args, ["file.txt"])

    def test_gtk_unavailable_error_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            nvim = self._make_executable(Path(tmp) / "nvim")
            stderr = StringIO()

            with patch("azwerks_nvim_shell.main.run_app") as run_app:
                run_app.side_effect = GtkUnavailableError("missing GTK")
                with redirect_stderr(stderr):
                    exit_code = main(["--nvim-bin", str(nvim)])

        self.assertEqual(exit_code, 3)
        self.assertEqual(
            stderr.getvalue().strip(),
            "error: GTK/VTE dependencies unavailable: missing GTK",
        )

    @staticmethod
    def _make_executable(path: Path) -> Path:
        path.write_text("#!/usr/bin/env sh\nexit 0\n", encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return path
