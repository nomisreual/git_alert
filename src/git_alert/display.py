from rich.console import Console
from rich.table import Table
from rich.text import Text

from git_alert.repositories import Repositories


class Report:
    def __init__(self, repos: Repositories, only_dirty: bool) -> None:
        self.console = Console()
        self.repos = repos
        self.only_dirty = only_dirty

    @staticmethod
    def style_status(status: str) -> Text:
        if status == "dirty":
            return Text(status, style="bold red")
        else:
            return Text(status, style="bold green")

    def create_long_report_table(self) -> None:
        self.long_report = Table(title="Full Report")
        self.long_report.add_column("Project", style="cyan", justify="left")
        self.long_report.add_column("Status", style="magenta", justify="center")
        self.long_report.add_column("Full Path", style="blue", justify="left")

    def create_summary_table(self) -> None:
        self.summary_report = Table(title="Summary Report")
        self.summary_report.add_column(
            "Number of Repositories", style="cyan", justify="center"
        )
        self.summary_report.add_column(
            "Number of Dirty Repositories", style="magenta", justify="center"
        )

    def populate_long_report_table(self) -> None:
        """
        Add project, status and full path of each found repository.
        """
        for pth, repo in self.repos.repos.items():
            status = repo.get("status")
            if self.only_dirty and status == "clean":
                continue
            self.long_report.add_row(
                str(pth.name),
                self.style_status(status),
                Text(str(pth), style="bold cyan"),
            )

    def populate_short_table(self) -> None:
        self.summary_report.add_row(
            str(self.repos.number_of_repositories),
            str(self.repos.number_of_dirty_repositories),
        )

    def display_long_report(self) -> None:
        self.console.print(self.long_report)

    def display_summary_report(self) -> None:
        self.console.print(self.summary_report)
