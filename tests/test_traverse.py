import sys
import unittest
from unittest.mock import MagicMock, Mock, patch

from git_alert.traverse import GitAlert


class TestGitAlertTraverse(unittest.TestCase):
    @patch("git_alert.traverse.Path")
    def test_traverse_git_present(self, mock_path):
        # Mock the return value of the glob method:
        glob_result = []

        # Mock one path that is a git repository:
        dir = Mock()
        dir.is_dir.return_value = True
        dir.name = ".git"

        # Add the mocked git directory to the glob result:
        glob_result.append(dir)
        # The return value of glob needs to be iterable:
        mock_path.glob.return_value = iter(glob_result)

        # Create GitAlert instance
        # Check is not really executed, hence a simple Mock as
        # repos argument suffices:
        alert = GitAlert(mock_path, Mock())
        # Mock the check method so its invocation can be tested:
        alert.check = MagicMock(name="check")

        alert.traverse(mock_path)

        # Test if glob is called correctly:
        mock_path.glob.assert_called_once_with("*")
        # Test if check method is called correctly:
        alert.check.assert_called_once_with(dir)

    @patch("git_alert.traverse.Path")
    def test_traverse_git_not_present(self, mock_path):
        # Mock the return value of the glob method:
        glob_result = []

        # Mock one file:
        dir = Mock()
        dir.is_dir.return_value = False
        dir.name = "some_file"

        # Add the mocked file to the glob result:
        glob_result.append(dir)
        # The return value of glob needs to be iterable:
        mock_path.glob.return_value = iter(glob_result)

        # Create GitAlert instance
        # Check is not really executed, hence a simple Mock as
        # repos argument suffices:
        alert = GitAlert(mock_path, Mock())
        # Mock the check method so its invocation can be tested:
        alert.check = MagicMock(name="check")

        alert.traverse(mock_path)

        # Test if glob is called correctly:
        mock_path.glob.assert_called_once_with("*")
        # Test if check method is not called:
        alert.check.assert_not_called()


class TestGitAlertTraversePermissionDenied(unittest.TestCase):
    @patch("git_alert.traverse.print")
    @patch("git_alert.traverse.Path")
    def test_traverse_permission_denied(self, mock_path, mock_print):
        # Mock the glob method to raise a PermissionError:
        mock_path.glob.side_effect = PermissionError()

        # Create GitAlert instance
        # Check is not really executed, hence a simple Mock as
        # repos argument suffices:
        alert = GitAlert(mock_path, Mock())

        # Mocking check not required, as it will not get called.

        alert.traverse(mock_path)

        # Check whether the correct warning was emitted:
        mock_print.assert_called_once_with(
            f"Warning: no access to: {mock_path}", file=sys.stderr
        )


class TestGitAlertCheck(unittest.TestCase):
    pass
