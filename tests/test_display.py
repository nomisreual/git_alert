import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from git_alert.display import Report


class TestReport(unittest.TestCase):
    def test_init(self):
        report = Report(Mock(), Mock())
        self.assertIsInstance(report, Report)

    def test_style_status_dirty(self):
        report = Report(Mock(), Mock())
        style_status = report.style_status("dirty")
        style = style_status.style
        text = style_status._text
        self.assertEqual(text, ["dirty"])
        self.assertEqual(style, "bold red")

    def test_style_status_clean(self):
        report = Report(Mock(), Mock())
        style_status = report.style_status("clean")
        style = style_status.style
        text = style_status._text
        self.assertEqual(text, ["clean"])
        self.assertEqual(style, "bold green")

    def test_poplate_short_table(self):
        repo = Mock()
        repo.number_of_repositories = 3
        repo.number_of_dirty_repositories = 2
        report = Report(repo, False)

        report.create_summary_table()
        report.populate_short_table()

        self.assertEqual(list(report.summary_report.columns[0].cells), ["3"])
        self.assertEqual(list(report.summary_report.columns[1].cells), ["2"])

        self.assertEqual(
            report.summary_report.columns[0].header, "Number of Repositories"
        )
        self.assertEqual(
            report.summary_report.columns[1].header, "Number of Dirty Repositories"
        )

    def test_populate_long_report_table(self):
        repo = Mock()
        repo.repos = {
            Path("/some/project"): {"status": "dirty"},
            Path("/other/project"): {"status": "clean"},
        }
        report = Report(repo, False)

        report.create_long_report_table()
        report.populate_long_report_table()

        self.assertEqual(
            list(report.long_report.columns[0].cells),
            ["project", "project"],
        )
        self.assertEqual(
            [status._text for status in list(report.long_report.columns[1].cells)],
            [["dirty"], ["clean"]],
        )
        self.assertEqual(
            [pth._text for pth in list(report.long_report.columns[2].cells)],
            [["/some/project"], ["/other/project"]],
        )

        self.assertEqual(report.long_report.columns[0].header, "Project")
        self.assertEqual(report.long_report.columns[1].header, "Status")
        self.assertEqual(report.long_report.columns[2].header, "Full Path")

    def test_populate_long_report_table_only_dirty(self):
        repo = Mock()
        repo.repos = {
            Path("/some/project"): {"status": "dirty"},
            Path("/other/project"): {"status": "clean"},
        }
        report = Report(repo, True)

        report.create_long_report_table()
        report.populate_long_report_table()

        self.assertEqual(
            list(report.long_report.columns[0].cells),
            ["project"],
        )
        self.assertEqual(
            [status._text for status in list(report.long_report.columns[1].cells)],
            [["dirty"]],
        )
        self.assertEqual(
            [pth._text for pth in list(report.long_report.columns[2].cells)],
            [["/some/project"]],
        )

        self.assertEqual(report.long_report.columns[0].header, "Project")
        self.assertEqual(report.long_report.columns[1].header, "Status")
        self.assertEqual(report.long_report.columns[2].header, "Full Path")

    @patch("git_alert.display.Console")
    def test_display_long_report(self, mock_console):

        repo = Mock()
        report = Report(repo, Mock())

        report.create_long_report_table()
        report.display_long_report()

        mock_console.return_value.print.assert_called_once_with(report.long_report)

    @patch("git_alert.display.Console")
    def test_display_summary_report(self, mock_console):

        repo = Mock()
        report = Report(repo, Mock())

        report.create_summary_table()
        report.display_summary_report()

        mock_console.return_value.print.assert_called_once_with(report.summary_report)
