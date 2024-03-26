from argparse import ArgumentParser, Namespace
from pathlib import Path


def argument_parser() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.cwd(),
        help="Top level directory to start the search in",
    )
    parser.add_argument(
        "--only_dirty",
        action="store_true",
        help="In the final report only show dirty repositories",
    )
    return parser.parse_args()
