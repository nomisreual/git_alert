import os
import sys
import tomllib
from pathlib import Path


class System:
    def __init__(self):
        self.user = os.environ.get("USER")

    @property
    def config_root(self):
        return Path("/home") / str(self.user) / ".config/git_alert"

    @property
    def config_file(self):
        return self.config_root / "config.toml"


class ReadConfig:

    def __init__(self, system: System):
        self.CONFIG_FILE = system.config_file

        try:
            with open(self.CONFIG_FILE, "rb") as f:
                self._config = tomllib.load(f)
        except FileNotFoundError:
            self._config = None
        except tomllib.TOMLDecodeError as err:
            print(f"Error decoding config file: {err}", file=sys.stderr)
            self._config = None

    @property
    def path(self):
        path = self._config.get("path", None)
        if path:
            return Path(path)
        return Path.cwd()

    @property
    def only_dirty(self):
        return self._config.get("only_dirty")

    @property
    def ignore(self):
        to_be_ignored = self._config.get("ignore")
        if to_be_ignored is None:
            return []
        return [Path(path) for path in to_be_ignored.values()]