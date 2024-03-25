from argparse import ArgumentParser, Namespace
from pathlib import Path

from repositories import Repositories
from traverse import traverse_directory


def main(args: Namespace) -> None:
    repos = Repositories()

    if args.path.is_dir():
        traverse_directory(args.path, repos, args.verbose, args.only_dirty)
    else:
        wd = Path.cwd()
        print(f"Traversing directory {wd}")
        traverse_directory(wd, repos, args.verbose, args.only_dirty)

    repos.display(only_dirty=args.only_dirty)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--path", type=Path, default=Path.cwd())
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--only_dirty", action="store_true")
    args = parser.parse_args()
    main(args)
