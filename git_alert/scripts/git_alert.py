import sys

from git_alert.argument_parser import argument_parser
from git_alert.configuration import ReadConfig, System
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

    # Override the configuration file with the command line arguments:
    if args.path:
        path = args.path
    if args.only_dirty:
        only_dirty = args.only_dirty
    if args.ignore:
        ignore = args.ignore

    alert = GitAlert(pth=path, ignore=ignore, repos=repos)

    alert.traverse(path)
    alert.check()
    alert.repos.display(only_dirty=only_dirty)
    alert.repos.summary()
