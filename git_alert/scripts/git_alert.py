import sys

from git_alert.argument_parser import argument_parser
from git_alert.repositories import Repositories
from git_alert.traverse import GitAlert


def run():
    repos = Repositories()

    args = argument_parser(sys.argv[1:])

    alert = GitAlert(pth=args.path, ignore=args.ignore, repos=repos)

    alert.traverse(args.path)
    alert.check()
    alert.repos.display(only_dirty=args.only_dirty)
    alert.repos.summary()
