import unittest
from pathlib import Path

from git_alert.argument_parser import argument_parser


class TestArgumentParser(unittest.TestCase):
    def test_argument_parser_only_dirty(self):
        args = argument_parser(["--path", "/path/to/repo", "--only_dirty"])
        self.assertEqual(args.path, Path("/path/to/repo"))
        self.assertEqual(args.only_dirty, True)

    def test_argument_parser(self):
        args = argument_parser(["--path", "/path/to/repo"])
        self.assertEqual(args.path, Path("/path/to/repo"))
        self.assertEqual(args.only_dirty, False)
