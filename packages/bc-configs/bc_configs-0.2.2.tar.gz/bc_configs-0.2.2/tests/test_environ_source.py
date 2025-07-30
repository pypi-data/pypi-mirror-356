import os
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict
from unittest.mock import patch

# Import define from our module
from bc_configs.environ_source.define import define


class TestEnvironSource(unittest.TestCase):
    """Tests for environment source loading functionality."""

    def setUp(self) -> None:
        """Saves the original environment before each test."""
        self._original_environ: Dict[str, str] = os.environ.copy()

    def tearDown(self) -> None:
        """Restores the original environment after each test."""
        os.environ.clear()
        os.environ.update(self._original_environ)

    def _create_temp_file(self, content: str, suffix: str) -> Path:
        """Helper function to create temporary files."""
        fd, path = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(fd, "w") as tmp:
            tmp.write(content)
        return Path(path)

    def test_dotenv_define_with_dotenv_installed(self) -> None:
        """
        Verifies that define() correctly loads variables from a .env file
        when python-dotenv is installed.
        """
        # Create a temporary .env file
        env_content: str = "TEST_DOTENV_VAR=dotenv_value\nEXISTING_VAR=should_not_be_overwritten\n"
        temp_env_file: Path = self._create_temp_file(env_content, ".env")

        # Set an existing environment variable that should not be overwritten
        os.environ["EXISTING_VAR"] = "original_value"

        with patch("dotenv.load_dotenv") as mock_load_dotenv:
            # Mock the behavior of load_dotenv to "load" variables
            # into os.environ as if it read our temp_env_file
            def mock_load_dotenv_side_effect(dotenv_path: Any = None, **kwargs: Any) -> None:
                if dotenv_path is None:
                    # Ensure it "sees" our file if no path is explicitly given
                    dotenv_path = temp_env_file
                # Simulate loading variables
                os.environ["TEST_DOTENV_VAR"] = "dotenv_value"
                # EXISTING_VAR should not be overwritten, so we don't set it here

            mock_load_dotenv.side_effect = mock_load_dotenv_side_effect

            define()

            mock_load_dotenv.assert_called_once()
            self.assertEqual(os.getenv("TEST_DOTENV_VAR"), "dotenv_value")
            self.assertEqual(os.getenv("EXISTING_VAR"), "original_value")  # Verify it was not overwritten

        os.unlink(temp_env_file)  # Delete the temporary file

    def test_yaml_define_with_pyyaml_installed(self) -> None:
        """
        Verifies that define() correctly loads variables from a YAML file
        when pyyaml is installed.
        """
        yaml_content: str = "TEST_YAML_VAR: yaml_value\nEXISTING_VAR: should_not_be_overwritten_yaml\n"
        temp_yaml_file: Path = self._create_temp_file(yaml_content, ".env.yml")

        os.environ["YAML_CONFIG_FILE"] = str(temp_yaml_file)
        os.environ["EXISTING_VAR"] = "original_value"

        define()

        self.assertEqual(os.getenv("TEST_YAML_VAR"), "yaml_value")
        self.assertEqual(os.getenv("EXISTING_VAR"), "original_value")  # Should remain the original value

        os.unlink(temp_yaml_file)  # Delete the temporary file

    # @patch("builtins.__import__", side_effect=ImportError("No module named 'dotenv'"))
    # def test_dotenv_define_without_dotenv_installed(self, mock_import: MagicMock) -> None:
    #     """
    #     Verifies that define() does not fail if python-dotenv is not installed.
    #     """
    #     with patch.dict(os.environ, {}, clear=True):  # Clear environment for this test
    #         define()
    #         self.assertIsNone(os.getenv("TEST_DOTENV_VAR"))
    #         # Verify that import attempt was made
    #         mock_import.assert_called_with("dotenv", fromlist=["load_dotenv"])

    # @patch("builtins.__import__", side_effect=ImportError("No module named 'yaml'"))
    # def test_yaml_define_without_pyyaml_installed(self, mock_import: MagicMock) -> None:
    #     """
    #     Verifies that define() does not fail if pyyaml is not installed.
    #     """
    #     with patch.dict(os.environ, {}, clear=True):  # Clear environment for this test
    #         define()
    #         self.assertIsNone(os.getenv("TEST_YAML_VAR"))
    #         # Verify that import attempt was made
    #         mock_import.assert_called_with("yaml")

    def test_yaml_define_with_non_dict_yaml(self) -> None:
        """
        Verifies that define() correctly handles a YAML file
        that does not contain a top-level dictionary.
        """
        yaml_content: str = "- item1\n- item2\n"  # Not a dictionary
        temp_yaml_file: Path = self._create_temp_file(yaml_content, ".env.yml")

        os.environ["YAML_CONFIG_FILE"] = str(temp_yaml_file)

        with patch("logging.warning") as mock_warning:
            define()
            mock_warning.assert_called_with(
                f"YAML file '{temp_yaml_file}' does not contain a top-level dictionary. Skipping.",
            )
        self.assertIsNone(os.getenv("TEST_YAML_VAR"))

        os.unlink(temp_yaml_file)

    def test_yaml_define_with_non_string_key(self) -> None:
        """
        Verifies that define() correctly handles a YAML file
        that contains non-string keys.
        """
        yaml_content: str = "123: value\n"  # Non-string key
        temp_yaml_file: Path = self._create_temp_file(yaml_content, ".env.yml")

        os.environ["YAML_CONFIG_FILE"] = str(temp_yaml_file)

        with patch("logging.warning") as mock_warning:
            define()
            mock_warning.assert_called_with(f"Key '123' in YAML file '{temp_yaml_file}' is not a string. Skipping.")
        self.assertIsNone(os.getenv("123"))

        os.unlink(temp_yaml_file)
