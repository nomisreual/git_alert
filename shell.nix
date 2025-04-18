{pkgs ? import <nixpkgs> {}}:
with pkgs.python311Packages; let
  # possibly easier to do a local build
  # manifest = (pkgs.lib.importTOML ./pyproject.toml).project;
  # local = pkgs.callPackage ./default.nix {};
  # local = buildPythonPackage {
  #   name = manifest.name;
  #   src = ./.;
  #   propagatedBuildInputs = [rich];
  #   build-system = [
  #     hatchling
  #   ];
  #   pyproject = true;
  # };
in
  pkgs.mkShell {
    packages =
      [
        (pkgs.python311.withPackages (python-pkgs:
          with python-pkgs; [
            # additional development python packages
            pytest
            pytest-cov
            flake8
            black
          ]))
      ]
      ++ (with pkgs; [
        # additional development dependencies outside python
        pre-commit
      ]);

    # Grab build inputs from package:
    inputsFrom = [(pkgs.callPackage ./default.nix {})];
  }
