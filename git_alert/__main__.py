import sys

from git_alert.argument_parser import argument_parser
from git_alert.repositories import Repositories
from git_alert.traverse import GitAlert

repos = Repositories()

args = argument_parser(sys.argv[1:])

alert = GitAlert(args.path, repos)

alert.traverse(args.path)
alert.repos.display(only_dirty=args.only_dirty)
