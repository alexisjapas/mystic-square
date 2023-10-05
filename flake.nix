{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
  };

  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs = { self, nixpkgs, devenv, systems, ... } @ inputs:
    let
      forEachSystem = nixpkgs.lib.genAttrs (import systems);
    in
    {
      devShells = forEachSystem
        (system:
          let
            pkgs = nixpkgs.legacyPackages.${system};
          in
          {
            default = devenv.lib.mkShell {
              inherit inputs pkgs;
              modules = [
                {
                  # https://devenv.sh/reference/options/
                  packages = with pkgs; [ 
                    hello
                    (python3.withPackages (ps: (with ps; [
                      pygame
                      black
                      (
                        buildPythonPackage rec {
                          pname = "pygame-menu";
                          version = "4.4.3";
                          src = fetchPypi {
                            inherit pname version;
                            sha256 = "AqmeVXYB81bOLMgqEOmLy1gdU5pBxmbE7mFPrjZsNkc=";
                          };
                          doCheck = false;
                          propagatedBuildInputs = [
                            # Specify dependencies
                            pygame
                            pyperclip
                            typing-extensions
                          ];
                        }
                      )
                    ])))
                  ];

                  enterShell = ''
                    hello
                  '';
                }
              ];
            };
          });
    };
}
