# main.py
import subprocess
from pathlib import Path

from git_alert.repositories import Repositories


def traverse_directory(pth: Path, repos: Repositories) -> None:
    files = pth.glob("*")
    for file in files:
        if file.is_dir() and file.name == ".git":
            check_status(file, repos)

        elif file.is_dir():
            traverse_directory(file, repos)


def check_status(directory: Path, repos: Repositories) -> None:
    repo = {}
    output = subprocess.run(
        ["git", "status"], cwd=directory.parent, stdout=subprocess.PIPE
    )
    if "working tree clean" in output.stdout.decode():
        repo[directory.parent] = "clean"
        repos.add_repo(repo)
    else:
        repo[directory.parent] = "dirty"
        repos.add_repo(repo)
