from pathlib import Path


class Repositories:
    def __init__(self) -> None:
        self.repos: list[dict[Path, str]] = []

    def add_repo(self, repo: dict[Path, str]) -> None:
        self.repos.append(repo)

    def display(self, only_dirty: bool) -> None:
        for repo in self.repos:
            for key, value in repo.items():
                if only_dirty and value == "clean":
                    continue
                print(f"Repository: {key} is {value}")
