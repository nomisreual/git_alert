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

    def display(self, only_dirty: bool) -> None:
        """
        Display the repositories and their status.
        args:
            only_dirty: bool
        """
        for pth, repo in self.repos.items():
            status = repo.get("status")
            if only_dirty and status == "clean":
                continue
            print(f"Repository: {pth} is {status}")

    def summary(self) -> None:
        """
        Display a summary of the repositories.
        """
        print(f"Number of repositories found: {self.number_of_repositories}")
        print(f"Number of dirty repositories: {self.number_of_dirty_repositories}")

    @property
    def number_of_dirty_repositories(self):
        dirty = [1 for repo in self.repos.values() if repo.get("status") == "dirty"]
        return sum(dirty)
