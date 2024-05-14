import os
import sys
import tomllib
from pathlib import Path


class System:
    def __init__(self):
        self.user = os.environ.get("USER")
        self.platform = sys.platform

    @property
    def config_root(self):
        if self.platform == "darwin":
            return Path("/Users") / str(self.user) / ".config/git_alert"
        elif self.platform == "linux":
            return Path("/home") / str(self.user) / ".config/git_alert"

    @property
    def config_file(self):
        if self.config_root:
            return self.config_root / "config.toml"


class ReadConfig:

    def __init__(self, system: System, config=None):
        if config:
            self.CONFIG_FILE = config
        else:
            self.CONFIG_FILE = system.config_file

        try:
            with open(self.CONFIG_FILE, "rb") as f:
                self._config = tomllib.load(f)
        except FileNotFoundError:
            print(f"Config file not found: {self.CONFIG_FILE}", file=sys.stderr)
            self._config = {}
        except tomllib.TOMLDecodeError as err:
            print(f"Error decoding config file: {err}", file=sys.stderr)
            self._config = {}

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
