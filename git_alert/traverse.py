# main.py
import subprocess
from pathlib import Path

from git_alert.repositories import Repositories


class GitAlert:
    def __init__(self, pth: Path, repos: Repositories):
        self._pth = pth
        self._repos = repos

    def traverse(self, pth: Path) -> None:
        files = pth.glob("*")
        for file in files:
            if file.is_dir() and file.name == ".git":
                self.check(file)

            elif file.is_dir():
                self.traverse(file)

    def check(self, pth: Path) -> None:
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
