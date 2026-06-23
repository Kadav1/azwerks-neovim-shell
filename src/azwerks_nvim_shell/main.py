from __future__ import annotations

import sys

from .app import GtkUnavailableError, run_app
from .cli import CliError, EarlyExit, parse_argv


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    args = sys.argv[1:] if argv is None else argv

    try:
        contract = parse_argv(args)
    except EarlyExit as early_exit:
        print(early_exit.output)
        return early_exit.code
    except CliError as error:
        print(str(error), file=sys.stderr)
        return 2

    try:
        return run_app(contract)
    except GtkUnavailableError as error:
        print(f"error: GTK/VTE dependencies unavailable: {error}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
