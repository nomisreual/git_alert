{pkgs ? import <nixpkgs> {}}:
with pkgs.python311Packages;
  buildPythonApplication rec {
    pname = "git_alert";
    version = "0.3.1";
    format = "pyproject";
    src = fetchPypi {
      inherit pname version;
      sha256 = "sha256-q0nZY/1LcUI1uJGTECA3/Nwdr4zJJVh6K/QNtuJcybc=";
    };
    build-system = [
      poetry-core
    ];
    meta = {
      changelog = "https://github.com/nomisreual/git_alert/releases/tag/v0.3.1";
      description = "Checks a given path and its sub-directories for dirty git repositories.";
      homepage = "https://github.com/nomisreual/git_alert";
      license = lib.licenses.mit;
    };
  }
