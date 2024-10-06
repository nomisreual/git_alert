{ pkgs ? import <nixpkgs> { } }:
with pkgs.python311Packages;
let
  manifest = (pkgs.lib.importTOML ./pyproject.toml).tool.poetry;
  local = buildPythonPackage {
    name = manifest.name;
    src = ./.;
    propagatedBuildInputs = [ rich ];
    build-system = [
      poetry-core
    ];
    pyproject = true;
  };
in
pkgs.mkShell {
  packages = [
    (pkgs.python311.withPackages (python-pkgs: with python-pkgs; [
      rich
      local
    ]))

    (pkgs.poetry.override { python3 = pkgs.python311; })
  ];
}
