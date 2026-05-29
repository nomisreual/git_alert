import sys

from git_alert.argument_parser import argument_parser
from git_alert.configuration import ReadConfig, System
from git_alert.display import Report
from git_alert.repositories import Repositories
from git_alert.traverse import GitAlert


def run():
    args = argument_parser(sys.argv[1:])
    repos = Repositories()

    # Create System class
    system = System()

    # Read configuration file:
    config = ReadConfig(system, config=args.config)

    # Get the path, only_dirty and ignore from the configuration class:
    path = config.path
    only_dirty = config.only_dirty
    ignore = config.ignore
    simple = config.simple

    # Override the configuration file with the command line arguments:
    if args.path:
        path = args.path
    if args.only_dirty:
        only_dirty = args.only_dirty
    if args.ignore:
        ignore = args.ignore
    if args.simple:
        simple = args.simple

    # TODO: add simple to config parser
    # for now it's only cli argument
    simple = args.simple

    report = Report(repos=repos, only_dirty=only_dirty, simple=simple)

    alert = GitAlert(pth=path, ignore=ignore, repos=repos)

    def populate_tables():
        report.create_long_report_table()
        report.populate_long_report_table()
        report.display_long_report()

    def show_tables():
        report.create_summary_table()
        report.populate_short_table()
        report.display_summary_report()

    if report.simple:
        alert.traverse(path)
        alert.check()
        if report.is_all_clean():
            print("All good!")
        else:
            print("Work needed.")
    else:
        with report.console.status("Indexing repositories...", spinner="bouncingBall"):
            alert.traverse(path)
        print("✅ Successfully indexed.")

        with report.console.status("Checking repositories...", spinner="bouncingBall"):
            alert.check()
        print("✅ Successfully checked.")
        populate_tables()
        show_tables()
