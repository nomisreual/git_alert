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

    @patch("git_alert.traverse.Path")
    def test_traverse_only_dir(self, mock_path):
        # Mock the return value of the glob method:
        glob_result = []

        # Mock one path that is a git repository:
        dir = Mock()
        dir.is_dir.return_value = True
        dir.name = "some_dir"

        # Add the mocked git directory to the glob result:
        glob_result.append(dir)
        # The return value of glob needs to be iterable:
        mock_path.glob.return_value = iter(glob_result)

        # Mock subdir
        glob_result_sub_dir = []

        # Mock one file:
        sub_dir = Mock()
        sub_dir.is_dir.return_value = False
        sub_dir.name = "some_file"

        glob_result_sub_dir.append(sub_dir)
        dir.glob.return_value = iter(glob_result_sub_dir)

        # Create GitAlert instance
        # Check is not really executed, hence a simple Mock as
        # repos argument suffices:
        alert = GitAlert(mock_path, Mock())
        # Mock the check method so its invocation can be tested:
        alert.check = MagicMock(name="check")

        alert.traverse(mock_path)

        # Test if glob is called correctly:
        mock_path.glob.assert_called_once_with("*")

        # Test if subdir is looked through:
        dir.glob.assert_called_once_with("*")
        # Test if check method is NOT called:
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
    @patch("git_alert.traverse.subprocess")
    def test_git_alert_check_clean(self, mock_subprocess):
        # Mock the return value of the subprocess.run method:
        output = Mock()
        output.stdout.decode.return_value = "working tree clean"
        mock_subprocess.run.return_value = output

        pth = Mock()
        pth.parent = "/parent"

        # Create GitAlert instance
        repos = Mock()
        alert = GitAlert(Mock(), repos)

        # Call the check method on the mocked path:
        alert.check(pth)
        # Assert whether the mocked repo's add_repo method was calles
        # appropriately:
        repos.add_repo.assert_called_once_with({"/parent": "clean"})

    @patch("git_alert.traverse.subprocess")
    def test_git_alert_check_dirty(self, mock_subprocess):
        # Mock the return value of the subprocess.run method:
        output = Mock()
        output.stdout.decode.return_value = "Changes not staged for commit"
        mock_subprocess.run.return_value = output

        pth = Mock()
        pth.parent = "/parent"

        # Create GitAlert instance
        repos = Mock()
        alert = GitAlert(Mock(), repos)

        # Call the check method on the mocked path:
        alert.check(pth)
        # Assert whether the mocked repo's add_repo method was calles
        # appropriately:
        repos.add_repo.assert_called_once_with({"/parent": "dirty"})


class TestGitAlertRepos(unittest.TestCase):
    def test_git_alert_repos(self):
        # Create GitAlert instance
        repos = Mock()
        alert = GitAlert(Mock(), repos)

        # Assert whether the repos property returns the correct value:
        repos_call = alert.repos
        self.assertEqual(repos_call, repos)
