from __future__ import annotations

from io import StringIO
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from azwerks_nvim_shell.app import debug_enabled, debug_log  # noqa: E402
from azwerks_nvim_shell.config import DEBUG_ENV_VAR  # noqa: E402


class RuntimeDiagnosticsTests(unittest.TestCase):
    def test_debug_disabled_by_default_for_empty_env(self) -> None:
        self.assertFalse(debug_enabled({}))

    def test_debug_enabled_only_for_one(self) -> None:
        self.assertTrue(debug_enabled({DEBUG_ENV_VAR: "1"}))
        self.assertFalse(debug_enabled({DEBUG_ENV_VAR: "true"}))

    def test_debug_log_is_silent_when_disabled(self) -> None:
        stream = StringIO()

        debug_log("hidden", env={}, stream=stream)

        self.assertEqual(stream.getvalue(), "")

    def test_debug_log_writes_prefixed_message_when_enabled(self) -> None:
        stream = StringIO()

        debug_log("visible", env={DEBUG_ENV_VAR: "1"}, stream=stream)

        self.assertIn("AZWERKS Neovim Shell debug: visible", stream.getvalue())


if __name__ == "__main__":
    unittest.main()
