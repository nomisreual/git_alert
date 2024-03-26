# main.py
import subprocess
from pathlib import Path

from git_alert.repositories import Repositories


def traverse_directory(pth: Path, repos: Repositories) -> None:
    files = pth.glob("*")
    for file in files:
        if file.is_dir() and file.name == ".git":
            repo = {}
            output = subprocess.run(
                ["git", "status"], cwd=file.parent, stdout=subprocess.PIPE
            )
            if "working tree clean" in output.stdout.decode():
                repo[file.parent] = "clean"
                repos.add_repo(repo)
            else:
                repo[file.parent] = "dirty"
                repos.add_repo(repo)

        elif file.is_dir():
            traverse_directory(file, repos)
