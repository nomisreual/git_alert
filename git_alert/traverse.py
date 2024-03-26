# main.py
import subprocess
from pathlib import Path

from repositories import Repositories


def traverse_directory(pth: Path, repos: Repositories, verbose: bool) -> None:
    files = pth.glob("*")
    for file in files:
        if file.is_dir() and file.name == ".git":
            repo = {}
            if verbose:
                print("Found .git directory at", file.parent)
                print("Running git status")
            output = subprocess.run(
                ["git", "status"], cwd=file.parent, stdout=subprocess.PIPE
            )
            if "working tree clean" in output.stdout.decode():
                if verbose:
                    print("Working tree clean")
                repo[file.parent] = "clean"
                repos.add_repo(repo)
            else:
                if verbose:
                    print("Working tree dirty")
                repo[file.parent] = "dirty"
                repos.add_repo(repo)

        elif file.is_dir():
            traverse_directory(file, repos, verbose)
