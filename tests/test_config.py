import unittest
from configparser import Error
from unittest.mock import mock_open, patch

from djcompiler.management.command.buildfile import BuildFile
from djcompiler.management.command.compile import CompileProject


class ConfigTests(unittest.TestCase):
    def parse(self, text, command=None):
        if command is None:
            command = CompileProject()
        with patch("djcompiler.management.command.compile.open", mock_open(read_data=text)):
            command.intial_configs()
        return command.config

    def test_single_line_configuration(self):
        self.assertEqual(
            self.parse(
                "project_name=Example\n"
                "other_files_needed=manage.py .env\n"
                "other_dirs_needed=static templates\n"
                "ignored_files=manage.py models.py\n"
                "ignored_dirs=venv build\n"
            ),
            {
                "project_name": "Example",
                "other_files_needed": ["manage.py", ".env"],
                "other_dirs_needed": ["static", "templates"],
                "ignored_files": ["manage.py", "models.py"],
                "ignored_dirs": ["venv", "build"],
            },
        )

    def test_indented_lists_allow_comments_blank_lines_and_tabs(self):
        self.assertEqual(
            self.parse(
                "# Project settings\n\n"
                "project_name=Example\n"
                "other_files_needed=\n"
                "    manage.py\n"
                "    # Keep deployment settings\n"
                "\n"
                "    .env\n"
                "other_dirs_needed=static\n"
                "\ttemplates\n"
                "ignored_files=\n"
                "    models.py\n"
                "ignored_dirs=venv\n"
                "    build\n"
            ),
            {
                "project_name": "Example",
                "other_files_needed": ["manage.py", ".env"],
                "other_dirs_needed": ["static", "templates"],
                "ignored_files": ["models.py"],
                "ignored_dirs": ["venv", "build"],
            },
        )

    def test_single_and_empty_list_options_are_lists(self):
        for key in ("ignored_dirs", "ignored_files", "other_dirs_needed", "other_files_needed"):
            for value, expected in (("single", ["single"]), ("", [])):
                with self.subTest(key=key, value=value):
                    self.assertEqual(self.parse(key + "=" + value + "\n"), {key: expected})

    def test_scalar_values_preserve_spaces_percent_equals_and_hash(self):
        self.assertEqual(
            self.parse("project_name=100%Example#1\nproject_author=Alice = Example\n"),
            {"project_name": "100%Example#1", "project_author": "Alice = Example"},
        )

    def test_malformed_entries_raise_config_errors(self):
        for text in ("    manage.py\n", "other_files_needed\n    manage.py\n"):
            with self.subTest(text=text), self.assertRaises(Error):
                self.parse(text)

    def test_reloading_does_not_keep_old_configuration(self):
        command = CompileProject()
        self.parse("project_name=Old\nignored_dirs=build\n", command)
        self.assertEqual(self.parse("project_name=New\n", command), {"project_name": "New"})
        self.assertEqual(self.parse("project_author=Other\n"), {"project_author": "Other"})

    def test_generated_configuration_remains_supported(self):
        config = self.parse(BuildFile.compiler_config)
        self.assertEqual(config["other_files_needed"], ["manage.py", ".env", "__init__.py"])
        self.assertEqual(config["other_dirs_needed"], ["static", "media"])


if __name__ == "__main__":
    unittest.main()
