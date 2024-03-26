from argument_parser import argument_parser
from repositories import Repositories
from traverse import traverse_directory


def main() -> None:
    repos = Repositories()

    args = argument_parser()

    traverse_directory(args.path, repos, args.verbose, args.only_dirty)

    repos.display(only_dirty=args.only_dirty)


if __name__ == "__main__":
    main()
