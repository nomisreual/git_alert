class Repositories:
    def __init__(self) -> None:
        self.repos: dict[dict[str, str]] = {}
        self.number_of_repositories = 0

    def add_repo(self, repo: dict[str, str]) -> None:
        """
        Add a repository to the list of repositories.
        args:
            repo: dict[str, str]
        """
        pth = repo.get("path")
        status = repo.get("status")
        self.repos[pth] = {"status": status}
        self.number_of_repositories += 1

    @property
    def number_of_dirty_repositories(self):
        dirty = [1 for repo in self.repos.values() if repo.get("status") == "dirty"]
        return sum(dirty)
