class Repositories:
    def __init__(self) -> None:
        self.repos: list[dict[str, str]] = []
        self.number_of_repositories = 0

    def add_repo(self, repo: dict[str, str]) -> None:
        """
        Add a repository to the list of repositories.
        args:
            repo: dict[str, str]
        """
        self.repos.append(repo)
        self.number_of_repositories += 1

    def display(self, only_dirty: bool) -> None:
        """
        Display the repositories and their status.
        args:
            only_dirty: bool
        """
        for repo in self.repos:
            pth = repo.get("path")
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
        return sum(repo["status"] == "dirty" for repo in self.repos)
