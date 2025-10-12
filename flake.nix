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
              pkgs.postgresql
              pkgs.uv
              (pkgs.python312.withPackages (p: [
                p.psycopg2
              ]))
            ];
          };
    };
}
