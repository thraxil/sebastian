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
              pkgs.gccStdenv
              pkgs.stdenv.cc.cc.lib
              pkgs.flyctl
	      pkgs.postgresql
              pkgs.ruff
              (pkgs.python310.withPackages (p: [
                p.tox
                p.pip-tools
                p.psycopg2
              ]))
            ];
	    shellHook = ''
              export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [
              pkgs.stdenv.cc.cc
              ]}
              '';
          };
    };
}
