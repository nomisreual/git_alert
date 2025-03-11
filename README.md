# Git Alert

<hr>

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
![Codecov](https://img.shields.io/codecov/c/github/nomisreual/git_alert)

This is a Python application that checks in the given directory and all its subdirectories
for any dirty repositories.

The source code is available on [GitHub](https://github.com/nomisreual/git_alert).

This application aims to ease the frequent use of git as it makes it easy to check for any untracked changes in any of your repositories.

## Installation:

The application is now available on **PyPI**, so you can install it using _pip_:

```
pip install git_alert
```

Alternatively, you can use _pipx_ to make it globally available:

```
pipx install git_alert
```

Of course you can also clone the repository and install it manually. The package is built using poetry, so the easiest way to build it locally would be
to use poetry:

```
git clone https://github.com/nomisreual/git_alert.git
cd git_alert
poetry build
```

After the build, you can install it either using pip or pipx:

```
pip install -e .
```

or

```
pipx install .
```

If you are using flakes to manage your NixOS installation, you can add the provided flake to your
inputs:

```nix
{
  description = "Configuration";

  inputs = {
    ...
    git_alert = {
      url = "github:nomisreual/git_alert";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    ...
  };
  outputs = {
    self,
    nixpkgs,
    ...
  } @ inputs: {
    # your configuration
  };
}
```

You can then add `git_alert` to your packages (don't forget to add `inputs` to the respective module):

```nix
# configuration.nix
{
  environment.systemPackages = with pkgs; [
    ...

    inputs.git_alert.packages."x86_64-linux".default
    ...
  ];
}
# home.nix
{
  home.packages = with pkgs; [
    ...

    inputs.git_alert.packages."x86_64-linux".default
    ...
  ];
}
```

After rebuilding, you have git_alert at your fingertips and it gets updated whenever you update your flake.

## Usage:

You can use _git_alert_ by either calling it as a module (`python -m git_alert`) or by directly using the installed package:

```
usage: git_alert [-h] [-p PATH] [--only_dirty] [-i IGNORE] [-v] [-c CONFIG]

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  top level directory to start the search in
  --only_dirty          only show dirty repositories in the final report
  -i IGNORE, --ignore IGNORE
                        colon separated list of paths to ignore
  -v, --version         show program's version number and exit
  -c CONFIG, --config CONFIG
                        path to the configuration file

Warning: adding a path to ignore will also ignore all subdirectories of that
path.
```

It should be noted that all options that require a path require an absolute path. The `-i` option can take multiple paths separated by a colon.

## Configuration:

Git Alert can be configured using a configuration file. The configuration file is expected to be in:

```
$XDG_CONFIG_HOME/git_alert/config.toml (usually ~/.config/git_alert/config.toml)
```

This behaviour can be overridden by specifying a path to a configuration file with the `-c` option. The configuration file is in TOML format and can contain the following options:

```toml
path = "/path/to/start/search/in"

only_dirty = true # only show dirty repositories in the final report

[ignore]
one_directory = '/path/to/one_directory'
another_directory = '/path/to/another_directory'
```

Hence, the configuration file closely resembles the command line options. The command line options will always override the configuration file. However,
_only_dirty_ is a special case. If it is set to true in the configuration file, it will be applied. The command line flag can only turn it on, not off. For reference, an example configuration file can be found in _docs_.

## Development:

The tool is aimed to be improved and extended going forward. If you have any ideas or want to contribute, feel free to open an issue or a pull request.

## Goals:

- [ ] more detailed checks (currently it distinguishes only between a repository being clean or not)
- [ ] speed up the lookup process
- [ ] enable caching found repositories for faster checking after the first run (maybe utilizing a database)
- [ ] GUI/ TUI interface
- [x] enable configuration with a configuration file
- [x] override default configuration file location with command line option

## Contributing:

This project is under active development, so any contributions are welcome. Feel free to open an issue or submit a pull request.

In case you want to submit a pull request, please:

- make sure to run the tests before submission
- use black (or similar tools) for code formatting

The project uses pre-commit hooks to ensure code quality, so feel free to use them as well.
