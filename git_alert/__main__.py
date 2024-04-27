import sys

from git_alert.argument_parser import argument_parser
from git_alert.display import Report
from git_alert.repositories import Repositories
from git_alert.traverse import GitAlert

repos = Repositories()

args = argument_parser(sys.argv[1:])

report = Report(repos=repos, only_dirty=args.only_dirty)

alert = GitAlert(pth=args.path, ignore=args.ignore, repos=repos)

with report.console.status("Indexing repositories...", spinner="bouncingBall"):
    alert.traverse(args.path)
print("✅ Successfully indexed.")

with report.console.status("Checking repositories...", spinner="bouncingBall"):
    alert.check()
print("✅ Successfully checked.")

report.create_long_report_table()
report.populate_long_report_table()
report.display_long_report()
