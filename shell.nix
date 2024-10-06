{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  packages = [
    (pkgs.python311.withPackages (python-pkgs: with python-pkgs; [
      rich
    ]))

    (pkgs.poetry.override { python3 = pkgs.python311; })
  ];
}
