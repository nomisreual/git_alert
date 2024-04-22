class Repositories:
    def __init__(self) -> None:
        self.repos: list[dict[str, str]] = []

    def add_repo(self, repo: dict[str, str]) -> None:
        """
        Add a repository to the list of repositories.
        args:
            repo: dict[str, str]
        """
        self.repos.append(repo)

    def display(self, only_dirty: bool) -> None:
        """
        Display the repositories.
        args:
            only_dirty: bool
        """
        for repo in self.repos:
            pth = repo.get("path")
            status = repo.get("status")
            if only_dirty and status == "clean":
                continue
            print(f"Repository: {pth} is {status}")
