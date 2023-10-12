{
  inputs = {
    nixpkgs-python.url = "github:cachix/nixpkgs-python";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
  };

  outputs = { self, nixpkgs, nixpkgs-python }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
      };
    in {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          nixpkgs-python.packages.x86_64-linux."3.7"
        ];
      };
    };
}
