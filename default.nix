{pkgs ? import <nixpkgs> {}}:
with pkgs.python311Packages;
  buildPythonApplication rec {
    pname = "git_alert";
    version = "0.2.0";
    format = "pyproject";
    src = fetchPypi {
      inherit pname version;
      sha256 = "sha256-czDH7B5rmlhnIUdd6wosjQoI4dkBSmHC83syeWXD8Bk=";
    };
    build-system = [
      poetry-core
    ];
    meta = {
      changelog = "https://github.com/nomisreual/git_alert/releases/tag/v0.2.0";
      description = "Checks a given path and its sub-directories for dirty git repositories.";
      homepage = "https://github.com/nomisreual/git_alert";
      license = lib.licenses.mit;
    };
  }
