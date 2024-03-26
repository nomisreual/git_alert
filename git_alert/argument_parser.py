from argparse import ArgumentParser, Namespace
from pathlib import Path


def argument_parser() -> Namespace:
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
        help="report only show dirty repositories in the final",
    )
    return parser.parse_args()
