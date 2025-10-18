# traverse.py
import pygit2

# import sys
from pathlib import Path

from git_alert.repositories import Repositories


class GitAlert:
    def __init__(self, pth: Path, repos: Repositories, ignore: list[str] = []) -> None:
        self._pth = pth
        self._repos = repos
        self._ignore = {pth: True for pth in ignore}

    def traverse(self, pth: Path) -> None:
        """
        Traverse the directory and its subdirectories and check if it is a git repository.
        args:
            pth: Path
        """

        for file in pth.rglob("*.git"):
            ignore_file = False
            for ign in self._ignore.keys():
                if ign in file.parents:
                    ignore_file = True
            if ignore_file:
                continue
            repo = {}
            repo["path"] = file.parent
            repo["status"] = None
            self._repos.add_repo(repo)

    def check(self) -> None:
        """
        Check if the git repositories found are clean or dirty.
        """
        for pth, repo in self._repos.repos.items():
            repoobject = pygit2.Repository(pth)
            repostatus = repoobject.status()
            if repostatus == {}:
                repo["status"] = "clean"
            else:
                repo["status"] = "dirty"

    @property
    def repos(self) -> Repositories:
        return self._repos
