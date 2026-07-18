from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import app.services.safety as safety


class SafetyTest(unittest.TestCase):
    def setUp(self):
        safety.clear_pending_actions()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.allowed_dir = Path(self.temp_dir.name)

    def tearDown(self):
        safety.clear_pending_actions()
        self.temp_dir.cleanup()

    def test_write_requires_allowed_folder_and_confirmation(self):
        target = self.allowed_dir / "note.txt"

        with patch.object(safety, "ALLOWED_FILE_DIRS", [str(self.allowed_dir)]):
            action = safety.dry_run_write_file(str(target), "hello")
            self.assertFalse(target.exists())

            result = safety.confirm_action(action.token)

        self.assertEqual("hello", target.read_text(encoding="utf-8"))
        self.assertIn("file written", result)

    def test_delete_requires_confirmation(self):
        target = self.allowed_dir / "note.txt"
        target.write_text("hello", encoding="utf-8")

        with patch.object(safety, "ALLOWED_FILE_DIRS", [str(self.allowed_dir)]):
            action = safety.dry_run_delete_file(str(target))
            self.assertTrue(target.exists())

            result = safety.confirm_action(action.token)

        self.assertFalse(target.exists())
        self.assertIn("file deleted", result)

    def test_path_outside_allowed_folder_is_rejected(self):
        outside = self.allowed_dir.parent / "outside.txt"

        with patch.object(safety, "ALLOWED_FILE_DIRS", [str(self.allowed_dir)]):
            with self.assertRaises(safety.SafetyError):
                safety.dry_run_write_file(str(outside), "blocked")

    def test_shell_requires_whitelisted_command_and_confirmation(self):
        with patch.object(safety, "ALLOWED_FILE_DIRS", [str(self.allowed_dir)]):
            with patch.object(safety, "ALLOWED_SHELL_COMMANDS", ["python3"]):
                action = safety.dry_run_shell("python3 -c 'print(123)'")
                self.assertIn("DRY-RUN shell command", action.preview)

                result = safety.confirm_action(action.token)

        self.assertIn("exit_code: 0", result)
        self.assertIn("123", result)

    def test_shell_rejects_non_whitelisted_command(self):
        with patch.object(safety, "ALLOWED_SHELL_COMMANDS", ["python3"]):
            with self.assertRaises(safety.SafetyError):
                safety.dry_run_shell("rm file.txt")


if __name__ == "__main__":
    unittest.main()
