{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  packages = [
    (pkgs.python311.withPackages (python-pkgs:
      with python-pkgs; [
        rich
        pygit2
        flake8
      ]))
    pkgs.pre-commit
  ];
}
