from rich.console import Console
from rich.table import Table

from git_alert.repositories import Repositories


class Display:
    def __init__(self, repos: Repositories, only_dirty: bool) -> None:
        self.console = Console()
        self.repos = repos.repos
        self.only_dirty = only_dirty

    def create_table(self) -> Table:
        self.table = Table(title="Full Report")
        self.table.add_column("Project", style="cyan", justify="left")
        self.table.add_column("Status", style="magenta", justify="center")
        self.table.add_column("Full Path", style="blue", justify="left")

    def populate_table(self) -> None:
        """
        Add project, status and full path of each found repository.
        """
        for pth, repo in self.repos.items():
            status = repo.get("status")
            if self.only_dirty and status == "clean":
                continue
            self.table.add_row(str(pth.name), status, str(pth))

    def display(self) -> None:
        self.console.print(self.table)


class Summary:
    def __init__(self, repos: Repositories, only_dirty: bool) -> None:
        self.console = Console()
        self.repos = repos
        self.only_dirty = only_dirty

    def create_table(self) -> Table:
        self.table = Table(title="Summary Report")
        self.table.add_column("Number of Repositories", style="cyan", justify="center")
        self.table.add_column(
            "Number of Dirty Repositories", style="magenta", justify="center"
        )

    def populate_table(self) -> None:
        self.table.add_row(
            str(self.repos.number_of_repositories),
            str(self.repos.number_of_dirty_repositories),
        )

    def display(self) -> None:
        self.console.print(self.table)
