from git_alert.argument_parser import argument_parser
from git_alert.repositories import Repositories
from git_alert.traverse import traverse_directory

repos = Repositories()

args = argument_parser()

traverse_directory(args.path, repos)

repos.display(only_dirty=args.only_dirty)
