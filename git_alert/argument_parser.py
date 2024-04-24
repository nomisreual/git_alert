from argparse import ArgumentParser, Namespace
from pathlib import Path


def argument_parser(args) -> Namespace:
    """
    Create argument parser providing two arguments:
    --path: Path, default: Path.cwd()
    --only_dirty: bool, default: False
    """

    # Define a custom argument type:
    def ignore_paths(paths: str) -> list[str]:
        paths_as_strings = paths.split(":")
        paths_as_pathlibPaths = [Path(path) for path in paths_as_strings]
        return paths_as_pathlibPaths

    parser = ArgumentParser(
        epilog="Warning: adding a path to ignore will also ignore all subdirectories of that path."
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.cwd(),
        help="top level directory to start the search in",
    )
    parser.add_argument(
        "--only_dirty",
        action="store_true",
        help="only show dirty repositories in the final report",
    )
    parser.add_argument(
        "--ignore",
        type=ignore_paths,
        default=[],
        help="colon separated list of paths to ignore",
    )
    return parser.parse_args(args)
