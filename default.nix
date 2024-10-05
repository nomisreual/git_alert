{ pkgs ? import <nixpkgs> { } }:
with pkgs.python311Packages;
buildPythonApplication rec {
  pname = "git_alert";
  version = "0.3.3";
  format = "pyproject";
  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-Dk4h4UZRes0QKHN5dd79wFEqXHC8Qn6LPtLXfKhr0FA=";
  };
  propagatedBuildInputs = [
    rich
  ];
  build-system = [
    poetry-core
  ];
  meta = {
    changelog = "https://github.com/nomisreual/git_alert/compare/v0.3.2...v0.3.3";
    description = "Checks a given path and its sub-directories for dirty git repositories.";
    homepage = "https://github.com/nomisreual/git_alert";
    license = lib.licenses.mit;
  };
}
