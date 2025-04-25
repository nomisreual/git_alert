{pkgs ? import <nixpkgs> {}}:
with pkgs.python311Packages; let
  manifest = (pkgs.lib.importTOML ./pyproject.toml).project;
  local = buildPythonPackage {
    name = manifest.name;
    src = ./.;
    dependencies = [rich];
    build-system = [
      hatchling
    ];
    pyproject = true;
  };
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

            local
          ]))
      ]
      ++ (with pkgs; [
        # additional development dependencies outside python
        pre-commit
        hatch # for building and publishing to pypi
      ]);

    # Grab build inputs from package:
    inputsFrom = [(pkgs.callPackage ./default.nix {})];
    shellHook = ''
      # set SHELL to current system shell, which points to
      # an interactive shell
      export SHELL=/run/current-system/sw/bin/bash
    '';
  }
