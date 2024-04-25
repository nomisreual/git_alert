import os
import sys
import tomllib
from pathlib import Path

PLATFORM = sys.platform
USER = os.environ.get("USER")
CONFIG_ROOT = Path("/home") / USER / ".config/git_alert"
CONFIG_FILE = CONFIG_ROOT / "config.toml"


class ReadConfig:

    USER = os.environ.get("USER")

    if sys.platform == "win32":
        CONFIG_ROOT = Path("C:/Users") / USER / "AppData/Roaming/git_alert"
    else:
        CONFIG_ROOT = Path("/home") / USER / ".config/git_alert"

    CONFIG_FILE = CONFIG_ROOT / "config.toml"

    def __init__(self):
        try:
            with open(CONFIG_FILE, "rb") as f:
                self.__config = tomllib.load(f)
        except FileNotFoundError:
            self.__config = None
        except tomllib.TOMLDecodeError as err:
            print(f"Error decoding config file: {err}", file=sys.stderr)
            self.__config = None

    @property
    def path(self):
        return Path(self.__config.get("path"))

    @property
    def only_dirty(self):
        return self.__config.get("only_dirty")

    @property
    def ignore(self):
        to_be_ignored = self.__config.get("ignore")
        if to_be_ignored is None:
            return []
        return [Path(path) for path in to_be_ignored.values()]
