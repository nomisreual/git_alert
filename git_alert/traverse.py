# traverse.py
import subprocess
import sys
from pathlib import Path

from git_alert.repositories import Repositories


class GitAlert:
    def __init__(self, pth: Path, repos: Repositories):
        self._pth = pth
        self._repos = repos

    def traverse(self, pth: Path) -> None:
        """
        Traverse the directory and its subdirectories and check if it is a git repository.
        args:
            pth: Path
        """
        try:
            files = pth.glob("*")
            for file in files:
                if file.is_dir() and file.name == ".git":
                    repo = {}
                    repo[file.parent] = None
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
            for pth, status in repo.items():
                output = subprocess.run(
                    ["git", "status"], cwd=pth, stdout=subprocess.PIPE
                )
                if "working tree clean" in output.stdout.decode():
                    repo[pth] = "clean"
                else:
                    repo[pth] = "dirty"

    @property
    def repos(self) -> Repositories:
        return self._repos
