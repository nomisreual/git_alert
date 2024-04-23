import sys
import unittest
from unittest.mock import MagicMock, Mock, patch

from git_alert.traverse import GitAlert


class TestGitAlertTraverse(unittest.TestCase):
    @patch("git_alert.traverse.Path")
    def test_traverse_git_present(self, mock_path):
        # Mock one path that is a git repository:
        dir = Mock()
        dir.is_dir.return_value = True
        dir.name = ".git"
        dir.parent = "/parent"

        # Add the mocked git directory to the glob result:
        glob_result = []
        glob_result.append(dir)
        # The return value of glob needs to be iterable:
        mock_path.glob.return_value = iter(glob_result)

        # Mock repos of GitAlert instance:
        repos = Mock()
        repos.add_repo = MagicMock(name="add_repo")

        # Create GitAlert instance
        alert = GitAlert(mock_path, repos)

        alert.traverse(mock_path)

        # Test if glob is called correctly:
        mock_path.glob.assert_called_once_with("*")

        # Check whether .add_repo was called with the correct argument:
        repos.add_repo.assert_called_once_with({"path": "/parent", "status": None})

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

        # Mock repos of GitAlert instance:
        repos = Mock()
        repos.add_repo = MagicMock(name="add_repo")

        # Create GitAlert instance
        alert = GitAlert(mock_path, repos)

        alert.traverse(mock_path)

        # Test if glob is called correctly:
        mock_path.glob.assert_called_once_with("*")

        # Make sure no 'repo' was added:
        repos.add_repo.assert_not_called()

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

        # Mock repos of GitAlert instance:
        repos = Mock()
        repos.add_repo = MagicMock(name="add_repo")

        # Create GitAlert instance
        alert = GitAlert(mock_path, repos)

        alert.traverse(mock_path)

        # Test if glob is called correctly:
        mock_path.glob.assert_called_once_with("*")
        # Test if subdir is looked through:
        dir.glob.assert_called_once_with("*")

        # Make sure no 'repo' was added:
        repos.add_repo.assert_not_called()


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

        # List of one repository:
        repos = Mock()
        repos.repos = [{"path": "/directory", "status": None}]

        # Create GitAlert instance:
        alert = GitAlert(Mock(), repos)

        # Call the .check method:
        alert.check()

        # Verify that the list of repositories was updated correctly:
        self.assertEqual(repos.repos, [{"path": "/directory", "status": "clean"}])

    @patch("git_alert.traverse.subprocess")
    def test_git_alert_check_dirty(self, mock_subprocess):
        # Mock the return value of the subprocess.run method:
        output = Mock()
        output.stdout.decode.return_value = "Changes not staged for commit"
        mock_subprocess.run.return_value = output

        # List of one repository:
        repos = Mock()
        repos.repos = [{"path": "/directory", "status": None}]

        # Create GitAlert instance:
        alert = GitAlert(Mock(), repos)

        # Call the .check method:
        alert.check()

        # Verify that the list of repositories was updated correctly:
        self.assertEqual(repos.repos, [{"path": "/directory", "status": "dirty"}])


class TestGitAlertRepos(unittest.TestCase):
    def test_git_alert_repos(self):
        # Create GitAlert instance
        repos = Mock()
        alert = GitAlert(Mock(), repos)

        # Assert whether the repos property returns the correct value:
        repos_call = alert.repos
        self.assertEqual(repos_call, repos)
