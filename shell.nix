{ pkgs ? import <nixpkgs> { } }:
with pkgs.python311Packages;
let
  local = buildPythonApplication {
    name = "git-alert-dev";
    src = ./.;
    propagatedBuildInputs = [ rich ];
    build-system = [
      poetry-core
    ];
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
