import pytest
from pathlib import Path
from unittest.mock import MagicMock

import git_alert.traverse as traverse


class DummyRepositories:
    def __init__(self):
        self.repos = {}

    def add_repo(self, repo):
        self.repos[repo["path"]] = repo


@pytest.fixture
def repos():
    r = DummyRepositories()
    r.repos = {
        Path("/repo/clean"): {"path": Path("/repo/clean"), "status": None},
        Path("/repo/dirty"): {"path": Path("/repo/dirty"), "status": None},
    }
    return r


def test_check_sets_clean_when_status_empty_dict(monkeypatch, repos):
    def mock_repository(path):
        mock = MagicMock()
        mock.status.return_value = {}
        return mock

    monkeypatch.setattr(traverse.pygit2, "Repository", mock_repository)

    alert = traverse.GitAlert(Path("."), repos)
    alert.check()

    assert repos.repos[Path("/repo/clean")]["status"] == "clean"
    assert repos.repos[Path("/repo/dirty")]["status"] == "clean"


def test_check_sets_dirty_when_status_not_empty(monkeypatch, repos):
    def mock_repository(path):
        mock = MagicMock()
        mock.status.return_value = {"file.txt": "modified"}
        return mock

    monkeypatch.setattr(traverse.pygit2, "Repository", mock_repository)

    alert = traverse.GitAlert(Path("."), repos)
    alert.check()

    assert repos.repos[Path("/repo/clean")]["status"] == "dirty"
    assert repos.repos[Path("/repo/dirty")]["status"] == "dirty"


def test_check_handles_mixed_clean_and_dirty(monkeypatch):
    repos = DummyRepositories()
    repos.repos = {
        Path("/repo/clean"): {"path": Path("/repo/clean"), "status": None},
        Path("/repo/dirty"): {"path": Path("/repo/dirty"), "status": None},
    }

    def mock_repository(path):
        mock = MagicMock()
        if "clean" in str(path):
            mock.status.return_value = {}
        else:
            mock.status.return_value = {"file.txt": "modified"}
        return mock

    monkeypatch.setattr(traverse.pygit2, "Repository", mock_repository)

    alert = traverse.GitAlert(Path("."), repos)
    alert.check()

    assert repos.repos[Path("/repo/clean")]["status"] == "clean"
    assert repos.repos[Path("/repo/dirty")]["status"] == "dirty"
