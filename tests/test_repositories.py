import unittest
from unittest.mock import call, patch

from git_alert.repositories import Repositories


class TestGitAlertRepositories(unittest.TestCase):
    def test_git_alert_repositories_add_repo_clean(self):
        repositories = Repositories()
        repo = {"path": "/path/to/repo", "status": "clean"}
        repositories.add_repo(repo)

        self.assertEqual(repositories.repos, {"/path/to/repo": {"status": "clean"}})

    def test_git_alert_repositories_add_repo_dirty(self):
        repositories = Repositories()
        repo = {"path": "/path/to/repo", "status": "dirty"}
        repositories.add_repo(repo)

        self.assertEqual(repositories.repos, {"/path/to/repo": {"status": "dirty"}})


# class TestGitAlertRepositoriesDisplayOnlyDirty(unittest.TestCase):
#     @patch("git_alert.repositories.print")
#     def test_git_alert_repositories_display_only_dirty(self, mock_print):
#         repositories = Repositories()
#         repo_1 = {"path": "/path/to/repo_1", "status": "clean"}
#         repo_2 = {"path": "/path/to/repo_2", "status": "dirty"}
#         repositories.add_repo(repo_1)
#         repositories.add_repo(repo_2)
#         repositories.display(only_dirty=True)
#         mock_print.assert_called_once_with("Repository: /path/to/repo_2 is dirty")
#
#     @patch("git_alert.repositories.print")
#     def test_git_alert_repositories_display_all(self, mock_print):
#         repositories = Repositories()
#         repo_1 = {"path": "/path/to/repo_1", "status": "clean"}
#         repo_2 = {"path": "/path/to/repo_2", "status": "dirty"}
#         repositories.add_repo(repo_1)
#         repositories.add_repo(repo_2)
#         repositories.display(only_dirty=False)
#         call_1 = call("Repository: /path/to/repo_2 is dirty")
#         call_2 = call("Repository: /path/to/repo_1 is clean")
#         expected_print_calls = [call_1, call_2]
#         mock_print.assert_has_calls(expected_print_calls, any_order=True)
#
#     @patch("git_alert.repositories.print")
#     def test_git_alert_repositories_summary(self, mock_print):
#         repositories = Repositories()
#         repo_1 = {"path": "/path/to/repo_1", "status": "clean"}
#         repo_2 = {"path": "/path/to/repo_2", "status": "dirty"}
#         repositories.add_repo(repo_1)
#         repositories.add_repo(repo_2)
#         repositories.summary()
#         expected_print_calls = [
#             call("Number of repositories found: 2"),
#             call("Number of dirty repositories: 1"),
#         ]
#         mock_print.assert_has_calls(expected_print_calls, any_order=True)
