import sqlite3
import subprocess
import sys
import zlib
from pathlib import Path


class RepositoriesDB:
    def __init__(self, db: Path) -> None:
        self.db = db

    @staticmethod
    def compress_path(path: Path) -> bytes:
        return zlib.compress(str(path).encode("utf-8"))

    @staticmethod
    def decompress_path(compressed_path: bytes) -> str:
        return zlib.decompress(compressed_path).decode("utf-8")

    def add_repo(self, repo: dict[str, str]):
        pth = repo.get("path")
        compressed_path = self.compress_path(pth)
        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("BEGIN")
                cursor.execute(
                    "INSERT INTO paths (path) VALUES (?)",
                    (compressed_path,),
                )
                path_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO projects (path_id, name) VALUES (?, ?)",
                    (path_id, pth.name),
                )
                connection.commit()
                print("Added successfully")
            except sqlite3.Error:
                connection.rollback()
                print("An error occured")

    def update_status(self):
        with sqlite3.connect(self.db) as connection:
            cursor = connection.cursor()
            try:

                cursor.execute("SELECT id, path FROM paths")
                pths = cursor.fetchall()

                for pth in pths:
                    id, pth = pth
                    pth = self.decompress_path(pth)
                    status = git_status.check(pth)
                    cursor.execute(
                        "SELECT id, desc FROM status WHERE desc = ?", (status,)
                    )
                    status_id, status = cursor.fetchone()
                    connection.execute(
                        "UPDATE projects SET status_id = ? WHERE path_id = ?",
                        (status_id, id),
                    )
            except sqlite3.Error:
                print("An error occured")


class GitAlertDB:
    def __init__(
        self, pth: Path, repos: RepositoriesDB, ignore: list[str] = []
    ) -> None:
        self._pth = pth
        self._repos = repos
        self._ignore = {pth: True for pth in ignore}

    def traverse(self, pth: Path) -> None:
        """
        Traverse the directory and its subdirectories and check if it is a git repository.
        args:
            pth: Path
        """
        if pth in self._ignore:
            return

        try:
            files = list(pth.glob("*"))

            if pth.joinpath(".git") in files:
                repo = {}
                repo["path"] = pth
                repo["status"] = None
                self._repos.add_repo(repo)
            else:
                for file in files:
                    if file.is_dir():
                        self.traverse(file)
        except PermissionError:
            print(f"Warning: no access to: {pth}", file=sys.stderr)

    @property
    def repos(self) -> RepositoriesDB:
        return self._repos


class GitStatus:

    @staticmethod
    def check(pth: Path) -> None:
        """
        Check if the git repositories found are clean or dirty.
        """
        output = subprocess.run(["git", "status"], cwd=pth, stdout=subprocess.PIPE)
        if "working tree clean" in output.stdout.decode():
            return "clean"
        else:
            return "dirty"


DB = Path("/home/simon/Projects/git_alert/git_alert/app.db")
ROOT = Path("/home/simon")

git_status = GitStatus()

repository = RepositoriesDB(DB)

git_alert = GitAlertDB(pth=Path(ROOT), repos=repository)
git_alert.traverse(ROOT)

repository.update_status()
