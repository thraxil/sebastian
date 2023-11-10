{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };
  outputs = {self, nixpkgs, ...}:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.x86_64-linux.default =
        pkgs.mkShell
          {
            buildInputs = [
              pkgs.flyctl
              (pkgs.python310.withPackages (p: [
                p.tox
                p.psycopg2
              ]))
            ];
          };
    };
}
