# traverse.py
import pygit2

from pathlib import Path
import os

from git_alert.repositories import Repositories


class GitAlert:
    def __init__(
        self, pth: Path, repos: Repositories, ignore: list[str] | None = None
    ) -> None:
        self._pth = Path(pth).resolve()
        self._repos = repos
        self._ignore = {Path(p).resolve() for p in (ignore or [])}

    def _is_ignored(self, path: Path) -> bool:
        return any(path == ign or path.is_relative_to(ign) for ign in self._ignore)

    def traverse(self, pth: Path | None = None) -> None:

        start_path = Path(pth).resolve() if pth else self._pth

        for root, dirs, files in os.walk(start_path):
            root_path = Path(root)

            dirs[:] = [d for d in dirs if not self._is_ignored(root_path / d)]

            if ".git" in dirs or ".git" in files:
                self._repos.add_repo(
                    {
                        "path": root_path,
                        "status": None,
                    }
                )

                dirs[:] = [d for d in dirs if d != ".git"]

    def check(self) -> None:
        """
        Check if the git repositories found are clean or dirty.
        """
        for pth, repo in self._repos.repos.items():
            try:
                repoobject = pygit2.Repository(pth)
                repo["status"] = "clean" if not repoobject.status() else "dirty"
            except (pygit2.GitError, OSError):
                repo["status"] = "invalid"

    @property
    def repos(self) -> Repositories:
        return self._repos
