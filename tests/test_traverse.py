import sys
import unittest
from unittest.mock import MagicMock, Mock, patch

from git_alert.traverse import GitAlert


class TestGitAlertTraverse(unittest.TestCase):
    def test_traverse_ignored_path(self):
        # Mock pth, repos and ignore:
        pth = MagicMock()
        ignore = [pth]

        # Create a GitAlert instance:
        alert = GitAlert(pth, Mock(), ignore)

        # Call the .traverse method:
        alert.traverse(pth)

        # Check if the .traverse method returned early:
        pth.glob.assert_not_called()

    def test_traverse_git_present(self):
        # Mock pth, repos and ignore:
        pth = MagicMock()

        # Mock path's content,
        # containing two files:

        # Mock git directory:
        file_1 = MagicMock()
        file_1.is_dir.return_value = True

        # Mock text file:
        file_2 = MagicMock()
        file_2.is_dir.return_value = False

        files = [file_1, file_2]

        # Mock the glob method of the path object,
        # note: glob returns a generator of Path objects:
        pth.glob.return_value = (file for file in files)

        # Mock the joinpath method of the path object:
        git_dir = MagicMock()
        pth.joinpath.return_value = git_dir

        # Make sure pth contains a .git directory:
        git_dir.__eq__.return_value = True

        # Mock the repositories object:
        repos = Mock()
        repos.add_repo = MagicMock(name="add_repo")

        # Mock the ignore list:
        ignore = []

        # Create a GitAlert instance:
        alert = GitAlert(pth, repos, ignore)

        # Call the .traverse method:
        alert.traverse(pth)

        # Check if the glob method was called correctly:
        pth.glob.assert_called_once_with("*")

        # Check if the add_repo method was called correctly:
        repos.add_repo.assert_called_once_with({"path": pth, "status": None})

    def test_traverse_git_not_present(self):
        # Mock pth, repos and ignore:
        pth = MagicMock()

        # Mock path's content,
        # containing two files:

        # Mock directory:
        file_1 = MagicMock()
        file_1.is_dir.return_value = True

        sub_file_1 = MagicMock()
        sub_file_1.is_dir.return_value = False
        sub_file_2 = MagicMock()
        sub_file_2.is_dir.return_value = False

        # Mock .glob of file_1:
        sub_files = [sub_file_1, sub_file_2]
        file_1.glob.return_value = (file for file in sub_files)

        # Mock text file:
        file_2 = MagicMock()
        file_2.is_dir.return_value = False

        # Mock the glob method of the path object,
        # note: glob returns a generator of Path objects:
        files = [file_1, file_2]
        pth.glob.return_value = (file for file in files)

        # Mock the joinpath method of the path object:
        git_dir = MagicMock()
        pth.joinpath.return_value = git_dir

        # Make sure pth does not contain a .git directory:
        git_dir.__eq__.return_value = False

        # Mock the repositories object:
        repos = Mock()
        repos.add_repo = MagicMock(name="add_repo")

        # Mock the ignore list:
        ignore = []

        # Create a GitAlert instance:
        alert = GitAlert(pth, repos, ignore)

        # Call the .traverse method:
        alert.traverse(pth)

        # Check if the glob method was called correctly:
        pth.glob.assert_called_once_with("*")

        # Check if the glob method was called on the subdirectory:
        file_1.glob.assert_called_once_with("*")

        # Check if the add_repo method was not called:
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

        # Dicttionary of one repository:
        repos = Mock()
        repos.repos = {"/directory": {"status": None}}

        # Create GitAlert instance:
        alert = GitAlert(Mock(), repos)

        # Call the .check method:
        alert.check()

        # Verify that the list of repositories was updated correctly:
        self.assertEqual(repos.repos, {"/directory": {"status": "clean"}})

    @patch("git_alert.traverse.subprocess")
    def test_git_alert_check_dirty(self, mock_subprocess):
        # Mock the return value of the subprocess.run method:
        output = Mock()
        output.stdout.decode.return_value = "Changes not staged for commit"
        mock_subprocess.run.return_value = output

        # Dicttionary of one repository:
        repos = Mock()
        repos.repos = {"/directory": {"status": None}}

        # Create GitAlert instance:
        alert = GitAlert(Mock(), repos)

        # Call the .check method:
        alert.check()

        # Verify that the list of repositories was updated correctly:
        self.assertEqual(repos.repos, {"/directory": {"status": "dirty"}})


class TestGitAlertRepos(unittest.TestCase):
    def test_git_alert_repos(self):
        # Create GitAlert instance
        repos = Mock()
        alert = GitAlert(Mock(), repos)

        # Assert whether the repos property returns the correct value:
        repos_call = alert.repos
        self.assertEqual(repos_call, repos)
