from argparse import ArgumentParser, Namespace
from pathlib import Path


def argument_parser(args) -> Namespace:
    """
    Create argument parser providing two arguments:
    --path: Path, default: Path.cwd()
    --only_dirty: bool, default: False
    """
    parser = ArgumentParser()
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
    return parser.parse_args(args)
