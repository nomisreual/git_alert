import unittest

from git_alert.repositories import Repositories


class TestGitAlertRepositories(unittest.TestCase):
    def test_git_alert_repositories_add_repo_clean(self):
        repositories = Repositories()
        repo = {"/path/to/repo": "clean"}
        repositories.add_repo(repo)
        self.assertEqual(repositories.repos, [repo])

    def test_git_alert_repositories_add_repo_dirty(self):
        repositories = Repositories()
        repo = {"/path/to/repo": "dirty"}
        repositories.add_repo(repo)
        self.assertEqual(repositories.repos, [repo])
