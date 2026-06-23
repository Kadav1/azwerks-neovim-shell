"""CLI parsing and launch-contract generation for AZWERKS Neovim Shell."""

from __future__ import annotations

from dataclasses import dataclass
import os
import shutil
from collections.abc import Mapping, Sequence

from .config import DEFAULT_NVIM_PATH, VERSION


class CliError(Exception):
    """A user-facing CLI error."""


@dataclass
class EarlyExit(Exception):
    """A successful early CLI exit such as --help or --version."""

    output: str
    code: int = 0


@dataclass
class LaunchContract:
    """Resolved values needed by the future GTK/VTE launch layer."""

    nvim_binary: str
    cwd: str
    positional_args: list[str]
    nvim_argv: list[str]


def format_help() -> str:
    """Return CLI help text."""
    return "\n".join(
        [
            "AZWERKS Neovim Shell",
            "",
            "Usage:",
            "  azwerks-nvim-shell [--cwd <path>] [--nvim-bin <path>] [file-or-dir ...]",
            "  azwerks-nvim-shell --help",
            "  azwerks-nvim-shell --version",
            "",
            "Options:",
            "  --help             Show this help and exit.",
            "  --version          Show version and exit.",
            "  --cwd <path>       Set the launch working directory.",
            "  --nvim-bin <path>  Use a specific executable Neovim binary.",
            "",
            "Valid invocations start a GTK/VTE window and spawn terminal Neovim.",
        ]
    )


def format_version() -> str:
    """Return CLI version text."""
    return f"AZWERKS Neovim Shell {VERSION}"


def find_nvim_binary(
    override: str | None = None,
    *,
    env: Mapping[str, str] | None = None,
) -> str:
    """Resolve the Neovim binary without launching it."""
    if override is not None:
        if _is_executable_file(override):
            return override
        raise CliError(f"error: invalid nvim binary path '{override}'")

    if _is_executable_file(DEFAULT_NVIM_PATH):
        return DEFAULT_NVIM_PATH

    search_env = os.environ if env is None else env
    path_value = search_env.get("PATH", "")
    path_binary = shutil.which("nvim", path=path_value)
    if path_binary is not None and _is_executable_file(path_binary):
        return path_binary

    raise CliError("error: could not find executable nvim binary")


def parse_argv(
    argv: Sequence[str],
    *,
    cwd: str | None = None,
    env: Mapping[str, str] | None = None,
) -> LaunchContract:
    """Parse argv into a launch contract.

    This function does not launch GTK, VTE, or Neovim.
    """
    process_cwd = os.getcwd() if cwd is None else os.path.abspath(cwd)
    positional_args: list[str] = []
    cwd_override: str | None = None
    nvim_override: str | None = None

    index = 0
    argv_list = list(argv)
    while index < len(argv_list):
        token = argv_list[index]

        if token == "--help":
            raise EarlyExit(format_help())
        if token == "--version":
            raise EarlyExit(format_version())
        if token == "--cwd":
            value = _consume_flag_value(argv_list, index, token)
            cwd_override = value
            index += 2
            continue
        if token == "--nvim-bin":
            value = _consume_flag_value(argv_list, index, token)
            nvim_override = value
            index += 2
            continue
        if token.startswith("--"):
            raise CliError(f"error: unknown flag '{token}'")

        positional_args.append(token)
        index += 1

    launch_cwd = _resolve_working_directory(
        cwd_override=cwd_override,
        positional_args=positional_args,
        process_cwd=process_cwd,
    )
    nvim_binary = find_nvim_binary(nvim_override, env=env)
    nvim_argv = [nvim_binary, *positional_args]

    return LaunchContract(
        nvim_binary=nvim_binary,
        cwd=launch_cwd,
        positional_args=positional_args,
        nvim_argv=nvim_argv,
    )


def _consume_flag_value(argv: Sequence[str], index: int, flag: str) -> str:
    value_index = index + 1
    if value_index >= len(argv) or argv[value_index].startswith("--"):
        raise CliError(f"error: missing value for flag '{flag}'")
    return argv[value_index]


def _resolve_working_directory(
    *,
    cwd_override: str | None,
    positional_args: Sequence[str],
    process_cwd: str,
) -> str:
    if cwd_override is not None:
        resolved_override = _resolve_path(cwd_override, process_cwd)
        if os.path.isdir(resolved_override):
            return resolved_override
        raise CliError(f"error: invalid working directory '{cwd_override}'")

    existing_directories = [
        _resolve_path(argument, process_cwd)
        for argument in positional_args
        if os.path.isdir(_resolve_path(argument, process_cwd))
    ]
    if len(existing_directories) == 1 and len(positional_args) == 1:
        return existing_directories[0]

    return process_cwd


def _resolve_path(path: str, process_cwd: str) -> str:
    if os.path.isabs(path):
        return os.path.abspath(path)
    return os.path.abspath(os.path.join(process_cwd, path))


def _is_executable_file(path: str) -> bool:
    return os.path.isfile(path) and os.access(path, os.X_OK)
