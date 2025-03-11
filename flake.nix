{
  description = "Git Alert";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    system-linux = "x86_64-linux";
    system-darwin = "x86_64-darwin";
    pkgs-linux = nixpkgs.legacyPackages.${system-linux};
    pkgs-darwin = nixpkgs.legacyPackages.${system-darwin};
  in {
    packages.${system-linux}.default = import ./default.nix {pkgs = pkgs-linux;};
    packages.${system-darwin}.default = import ./default.nix {pkgs = pkgs-darwin;};
  };
}
