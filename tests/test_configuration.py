import tomllib
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

from git_alert.configuration import ReadConfig, System


class TestSystemLinux(unittest.TestCase):
    @patch("sys.platform", "linux")
    def test_system(self):
        system = System()
        self.assertEqual(
            system.config_root, Path("/home") / "simon" / ".config/git_alert"
        )
        self.assertEqual(
            system.config_file,
            Path("/home") / "simon" / ".config/git_alert" / "config.toml",
        )


class TestReadConfig(unittest.TestCase):
    def test_read_config_file_not_found(self):
        with patch("builtins.open", mock_open()) as mock_file:
            # Add side effect to the mock_file object to raise a FileNotFoundError
            mock_file.side_effect = FileNotFoundError()

            # Call the ReadConfig init method:
            config = ReadConfig(System())

            # Make assertions:
            self.assertEqual(config._config, {})
            mock_file.assert_called_once_with(config.CONFIG_FILE, "rb")

    @patch("git_alert.configuration.tomllib.load")
    def test_read_success_with_path(self, mock_load):
        mock_load.return_value = {"path": "/some/path"}
        config = ReadConfig(System())
        mock_load.assert_called_once()
        self.assertEqual(config.path, Path("/some/path"))

    @patch("git_alert.configuration.Path.cwd")
    @patch("git_alert.configuration.tomllib.load")
    def test_read_success_without_path(self, mock_load, mock_cwd):
        mock_load.return_value = {}
        mock_cwd.return_value = Path("/some/path")
        config = ReadConfig(System())
        mock_load.assert_called_once()
        self.assertEqual(config.path, Path("/some/path"))

    @patch("git_alert.configuration.tomllib.load")
    def test_read_success_without_ignore(self, mock_load):
        mock_load.return_value = {}
        config = ReadConfig(System())
        mock_load.assert_called_once()
        self.assertEqual(config.ignore, [])

    @patch("git_alert.configuration.tomllib.load")
    def test_read_success_with_ignore(self, mock_load):
        mock_load.return_value = {"ignore": {"local": "/some/path"}}
        config = ReadConfig(System())
        mock_load.assert_called_once()
        self.assertEqual(config.ignore, [Path("/some/path")])

    @patch("git_alert.configuration.tomllib.load")
    def test_read_success_with_only_dirty(self, mock_load):
        mock_load.return_value = {"only_dirty": True}
        config = ReadConfig(System())
        mock_load.assert_called_once()
        self.assertTrue(config.only_dirty)

    def test_read_config_decode_error(self):
        with patch("git_alert.configuration.tomllib.load") as mock_load:
            # Add side effect to the mock_file object to raise a FileNotFoundError
            mock_load.side_effect = tomllib.TOMLDecodeError()

            # Call the ReadConfig init method:
            config = ReadConfig(System())

            # Make assertions:
            self.assertEqual(config._config, {})
            mock_load.assert_called_once()
