# traverse.py
import subprocess
import sys
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
        if pth in self._ignore:
            return
        try:
            files = pth.glob("*")
            for file in files:
                if file.is_dir() and file.name == ".git":
                    repo = {}
                    repo["path"] = file.parent
                    repo["status"] = None
                    self._repos.add_repo(repo)

                elif file.is_dir():
                    self.traverse(file)
        except PermissionError:
            print(f"Warning: no access to: {pth}", file=sys.stderr)

    def check(self) -> None:
        """
        Check if the git repositories found are clean or dirty.
        """
        for repo in self._repos.repos:
            pth = repo.get("path")
            output = subprocess.run(["git", "status"], cwd=pth, stdout=subprocess.PIPE)
            if "working tree clean" in output.stdout.decode():
                repo["status"] = "clean"
            else:
                repo["status"] = "dirty"

    @property
    def repos(self) -> Repositories:
        return self._repos
