# Git Alert

<!-- BADGIE TIME -->

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

<!-- END BADGIE TIME -->

This is a Python application that checks in the given directory and all its subdirectories
for any dirty repositories.

This application aims to ease the frequent use of git as it makes it easy to check for any untracked changes in any of your repositories.

## Usage:

```
usage: __init__.py [-h] [--path PATH] [--only_dirty]

options:
  -h, --help    show this help message and exit
  --path PATH   top level directory to start the search in
  --only_dirty  only show dirty repositories in the final report
```

As an installed package:

```
python -m git_alert [--path PATH] [--only_dirty]
```

## Planned:

- [ ] speed up the lookup process
- [ ] enable caching found repositories for faster checking after the first run (maybe utilizing a database)
