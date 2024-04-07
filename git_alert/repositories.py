from pathlib import Path


class Repositories:
    def __init__(self) -> None:
        self.repos: list[dict[Path, str]] = []

    def add_repo(self, repo: dict[Path, str]) -> None:
        """
        Add a repository to the list of repositories.
        args:
            repo: dict[Path, str]
        """
        self.repos.append(repo)

    def display(self, only_dirty: bool) -> None:
        """
        Display the repositories.
        args:
            only_dirty: bool
        """
        for repo in self.repos:
            for key, value in repo.items():
                if only_dirty and value == "clean":
                    continue
                print(f"Repository: {key} is {value}")
