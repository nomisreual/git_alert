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
                    self.check(file)

                elif file.is_dir():
                    self.traverse(file)
        except PermissionError:
            print(f"Warning: no access to: {pth}", file=sys.stderr)

    def check(self, pth: Path) -> None:
        """
        Check if the git repository is clean or dirty.
        args:
            pth: Path
        """
        repo = {}
        output = subprocess.run(
            ["git", "status"], cwd=pth.parent, stdout=subprocess.PIPE
        )
        if "working tree clean" in output.stdout.decode():
            repo[pth.parent] = "clean"
            self._repos.add_repo(repo)
        else:
            repo[pth.parent] = "dirty"
            self._repos.add_repo(repo)

    @property
    def repos(self) -> Repositories:
        return self._repos
