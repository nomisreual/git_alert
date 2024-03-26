from argparse import ArgumentParser, Namespace
from pathlib import Path


def argument_parser() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--path", type=Path, default=Path.cwd())
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--only_dirty", action="store_true")
    return parser.parse_args()
