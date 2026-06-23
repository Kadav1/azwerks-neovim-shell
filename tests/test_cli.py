from __future__ import annotations

import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from azwerks_nvim_shell.cli import CliError, EarlyExit, parse_argv


class CliParserTests(unittest.TestCase):
    def test_help_early_exit(self) -> None:
        with self.assertRaises(EarlyExit) as raised:
            parse_argv(["--help"], env={"PATH": ""})

        self.assertEqual(raised.exception.code, 0)
        self.assertIn("Usage:", raised.exception.output)

    def test_version_early_exit(self) -> None:
        with self.assertRaises(EarlyExit) as raised:
            parse_argv(["--version"], env={"PATH": ""})

        self.assertEqual(raised.exception.code, 0)
        self.assertIn("0.1.0", raised.exception.output)

    def test_help_ignores_later_invalid_args(self) -> None:
        with self.assertRaises(EarlyExit):
            parse_argv(["--help", "--cwd"], env={"PATH": ""})

    def test_version_ignores_earlier_positional_args(self) -> None:
        with self.assertRaises(EarlyExit):
            parse_argv(["file.txt", "--version", "--foo"], env={"PATH": ""})

    def test_unknown_flag_errors(self) -> None:
        with self.assertRaisesRegex(CliError, "error: unknown flag '--foo'"):
            parse_argv(["--foo"], env={"PATH": ""})

    def test_missing_cwd_value_errors(self) -> None:
        with self.assertRaisesRegex(CliError, "error: missing value for flag '--cwd'"):
            parse_argv(["--cwd"], env={"PATH": ""})

    def test_missing_nvim_bin_value_errors(self) -> None:
        with self.assertRaisesRegex(CliError, "error: missing value for flag '--nvim-bin'"):
            parse_argv(["--nvim-bin"], env={"PATH": ""})

    def test_cwd_followed_by_nvim_bin_produces_missing_cwd_error(self) -> None:
        with self.assertRaisesRegex(CliError, "error: missing value for flag '--cwd'"):
            parse_argv(["--cwd", "--nvim-bin", "/usr/bin/nvim"], env={"PATH": ""})

    def test_nvim_bin_followed_by_cwd_produces_missing_nvim_bin_error(self) -> None:
        with self.assertRaisesRegex(CliError, "error: missing value for flag '--nvim-bin'"):
            parse_argv(["--nvim-bin", "--cwd", "/project"], env={"PATH": ""})

    def test_invalid_cwd_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            nvim = self._make_executable(Path(tmp) / "nvim")
            missing = Path(tmp) / "missing"

            with self.assertRaisesRegex(CliError, f"error: invalid working directory '{missing}'"):
                parse_argv(["--nvim-bin", str(nvim), "--cwd", str(missing)], cwd=tmp)

    def test_invalid_nvim_binary_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad_path = Path(tmp) / "missing-nvim"

            with self.assertRaisesRegex(CliError, f"error: invalid nvim binary path '{bad_path}'"):
                parse_argv(["--nvim-bin", str(bad_path)], cwd=tmp)

    def test_duplicate_cwd_uses_last_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nvim = self._make_executable(root / "nvim")
            first = root / "first"
            second = root / "second"
            first.mkdir()
            second.mkdir()

            contract = parse_argv(
                ["--nvim-bin", str(nvim), "--cwd", str(first), "--cwd", str(second)],
                cwd=tmp,
            )

            self.assertEqual(contract.cwd, str(second))

    def test_duplicate_nvim_bin_uses_last_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = self._make_executable(root / "nvim-first")
            second = self._make_executable(root / "nvim-second")

            contract = parse_argv(
                ["--nvim-bin", str(first), "--nvim-bin", str(second)],
                cwd=tmp,
            )

            self.assertEqual(contract.nvim_binary, str(second))
            self.assertEqual(contract.nvim_argv, [str(second)])

    def test_positional_order_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            nvim = self._make_executable(Path(tmp) / "nvim")

            contract = parse_argv(
                ["--nvim-bin", str(nvim), "file1.txt", "file2.txt"],
                cwd=tmp,
            )

            self.assertEqual(contract.positional_args, ["file1.txt", "file2.txt"])
            self.assertEqual(contract.nvim_argv, [str(nvim), "file1.txt", "file2.txt"])

    def test_nonexistent_positional_path_passed_through(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            nvim = self._make_executable(Path(tmp) / "nvim")

            contract = parse_argv(["--nvim-bin", str(nvim), "missing.txt"], cwd=tmp)

            self.assertEqual(contract.positional_args, ["missing.txt"])
            self.assertEqual(contract.cwd, tmp)

    def test_single_directory_positional_infers_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nvim = self._make_executable(root / "nvim")
            directory = root / "project"
            directory.mkdir()

            contract = parse_argv(["--nvim-bin", str(nvim), "project"], cwd=tmp)

            self.assertEqual(contract.cwd, str(directory))
            self.assertEqual(contract.positional_args, ["project"])

    def test_multiple_directories_do_not_infer_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nvim = self._make_executable(root / "nvim")
            (root / "one").mkdir()
            (root / "two").mkdir()

            contract = parse_argv(["--nvim-bin", str(nvim), "one", "two"], cwd=tmp)

            self.assertEqual(contract.cwd, tmp)

    def test_mixed_file_and_directory_does_not_infer_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nvim = self._make_executable(root / "nvim")
            (root / "project").mkdir()
            (root / "file.txt").write_text("content", encoding="utf-8")

            contract = parse_argv(["--nvim-bin", str(nvim), "project", "file.txt"], cwd=tmp)

            self.assertEqual(contract.cwd, tmp)

    def test_empty_invocation_produces_nvim_argv_with_only_binary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            nvim = self._make_executable(bin_dir / "nvim")

            contract = parse_argv([], cwd=tmp, env={"PATH": str(bin_dir)})

            self.assertEqual(contract.nvim_argv, [contract.nvim_binary])
            self.assertTrue(os.path.isabs(contract.cwd))
            self.assertEqual(contract.cwd, tmp)
            self.assertTrue(contract.nvim_binary == str(nvim) or contract.nvim_binary.endswith("/nvim"))

    def test_missing_default_and_path_nvim_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing_default = str(Path(tmp) / "missing-default-nvim")

            with patch("azwerks_nvim_shell.cli.DEFAULT_NVIM_PATH", missing_default):
                with self.assertRaisesRegex(
                    CliError,
                    "error: could not find executable nvim binary",
                ):
                    parse_argv([], cwd=tmp, env={"PATH": ""})

    def test_paths_with_spaces_stay_as_one_argument(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            nvim = self._make_executable(Path(tmp) / "nvim")

            contract = parse_argv(["--nvim-bin", str(nvim), "my file.txt"], cwd=tmp)

            self.assertEqual(contract.positional_args, ["my file.txt"])
            self.assertEqual(contract.nvim_argv, [str(nvim), "my file.txt"])

    @staticmethod
    def _make_executable(path: Path) -> Path:
        path.write_text("#!/usr/bin/env sh\nexit 0\n", encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return path
