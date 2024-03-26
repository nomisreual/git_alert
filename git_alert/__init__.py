from argparse import Namespace

from argument_parser import argument_parser
from repositories import Repositories
from traverse import traverse_directory


def main(args: Namespace) -> None:
    repos = Repositories()

    traverse_directory(args.path, repos, args.verbose, args.only_dirty)

    repos.display(only_dirty=args.only_dirty)


if __name__ == "__main__":
    main(argument_parser())
