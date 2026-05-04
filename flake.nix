{
  description = "Sebastian SRS app";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, uv2nix, pyproject-nix, pyproject-build-systems, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (pkgs) lib;

        # Load workspace
        workspace = uv2nix.lib.workspace.loadWorkspace {
          workspaceRoot = ./.;
        };

        # Create the package set builder
        packageSet = pkgs.callPackage pyproject-nix.build.packages {
          python = pkgs.python312;
        };

        # Render the workspace to an overlay
        overlay = workspace.mkPyprojectOverlay {
          sourcePreference = "wheel";
        };

        # Apply overlays to the package set
        overriddenSet = packageSet.overrideScope (
          lib.composeManyExtensions [
            pyproject-build-systems.overlays.wheel
            overlay
            (final: prev: {
              # django-debug-toolbar 6.3.0 patch from original flake
              django-debug-toolbar = prev.django-debug-toolbar.overrideAttrs (old: {
                postPatch = (old.postPatch or "") + ''
                  if [ -f pyproject.toml ]; then
                    sed -i "/Framework :: Django :: 6.0/d" pyproject.toml
                  fi
                '';
              });
            })
          ]
        );

        # Create virtual environments
        pythonRuntime = overriddenSet.mkVirtualEnv "sebastian-runtime" workspace.deps.default;
        pythonDev = overriddenSet.mkVirtualEnv "sebastian-dev" workspace.deps.all;

        # Static files derivation
        staticfiles = pkgs.stdenv.mkDerivation {
          name = "sebastian-staticfiles";
          src = pkgs.lib.cleanSource ./.;
          buildInputs = [ pythonRuntime ];
          buildPhase = ''
            export SECRET_KEY=dummy
            export DJANGO_SETTINGS_MODULE=sebastian.settings_docker
            python manage.py collectstatic --noinput
          '';
          installPhase = ''
            mkdir -p $out
            cp -r staticfiles/* $out/
          '';
        };

        # App directory with source and static files
        appDir = pkgs.runCommand "sebastian-app" {} ''
          mkdir -p $out/app
          cp -r ${pkgs.lib.cleanSource ./.}/* $out/app/
          chmod -R +w $out/app
          chmod +x $out/app/entry-point.sh
          rm -rf $out/app/staticfiles
          cp -r ${staticfiles} $out/app/staticfiles
        '';

        container = pkgs.dockerTools.buildLayeredImage {
          name = "sebastian";
          tag = "latest";
          contents = [
            pythonRuntime
            pkgs.bash
            pkgs.postgresql
            pkgs.coreutils
            appDir
          ];
          fakeRootCommands = ''
            mkdir -p usr/bin
            ln -s ${pkgs.coreutils}/bin/env usr/bin/env
          '';
          config = {
            Entrypoint = [ "/app/entry-point.sh" ];
            Cmd = [ "run" ];
            WorkingDir = "/app";
            ExposedPorts = {
              "8000/tcp" = {};
            };
            Env = [
              "PYTHONUNBUFFERED=1"
              "DJANGO_SETTINGS_MODULE=sebastian.settings_docker"
              "APP=sebastian"
              "PATH=${pythonRuntime}/bin:${pkgs.bash}/bin:${pkgs.postgresql}/bin:${pkgs.coreutils}/bin"
            ];
          };
        };
      in
      {
        packages = {
          default = container;
          container = container;
          staticfiles = staticfiles;
        };

        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.flyctl
            pkgs.nodejs
            pkgs.gemini-cli
            pkgs.postgresql
            pkgs.uv
            pythonDev
          ];
          shellHook = ''
            export DJANGO_SETTINGS_MODULE=sebastian.settings
          '';
        };
      });
}
