{pkgs ? import <nixpkgs> {}}:
with pkgs.python311Packages; let
  manifest = (pkgs.lib.importTOML ./pyproject.toml).project;
in
  buildPythonApplication rec {
    pname = manifest.name;
    version = manifest.version;
    format = "pyproject";
    src = fetchPypi {
      inherit pname version;
      sha256 = "sha256-edGskDzNnzLOV2P2RKn88DtrwgYhx3f5WIHWfyxVJ80=";
    };
    propagatedBuildInputs = [
      rich
    ];
    build-system = [
      hatchling
    ];
    meta = {
      changelog = "https://github.com/nomisreual/git_alert/compare/v0.3.3...v0.4.0";
      description = "Checks a given path and its sub-directories for dirty git repositories.";
      homepage = "https://github.com/nomisreual/git_alert";
      license = lib.licenses.mit;
    };
  }
