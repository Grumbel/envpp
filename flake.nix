{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonPackages = pkgs.python3Packages;
      in rec {
        packages = rec {
          default = envpp;

          envpp = pythonPackages.buildPythonPackage rec {
            pname = "envpp";
            version = "0.1.0";

            src = ./.;

            pyproject = true;
            build-system = [ pythonPackages.setuptools ];

            propagatedBuildInputs = [
              pythonPackages.termcolor
            ];
          };
        };
      }
    );
}
